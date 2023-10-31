import datetime
import os
import shlex
import subprocess
import time
from functools import wraps
from time import sleep

import yaml
from colorama import Fore
from github import Github

from webhook_server_container.utils.constants import FLASK_APP


def get_app_data_dir():
    return os.environ.get("WEBHOOK_SERVER_DATA_DIR", "/webhook_server")


def get_data_from_config():
    config_file = os.path.join(get_app_data_dir(), "config.yaml")
    with open(config_file) as fd:
        return yaml.safe_load(fd)


def extract_key_from_dict(key, _dict):
    if isinstance(_dict, dict):
        for _key, _val in _dict.items():
            if _key == key:
                yield _val
            if isinstance(_val, dict):
                for result in extract_key_from_dict(key, _val):
                    yield result
            elif isinstance(_val, list):
                for _item in _val:
                    for result in extract_key_from_dict(key, _item):
                        yield result


def ignore_exceptions(logger=None, retry=None):
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as ex:
                if retry:
                    for _ in range(0, retry):
                        try:
                            return func(*args, **kwargs)
                        except Exception:
                            sleep(1)

                if logger:
                    logger.error(f"{func.__name__}({args} {kwargs}). Error: {ex}")
                return None

        return inner

    return wrapper


@ignore_exceptions(logger=FLASK_APP.logger, retry=5)
def get_github_repo_api(github_api, repository):
    return github_api.get_repo(repository)


def run_command(
    command,
    log_prefix,
    verify_stderr=False,
    shell=False,
    timeout=None,
    capture_output=True,
    check=False,
    file_path=None,
    **kwargs,
):
    """
    Run command locally.

    Args:
        command (str): Command to run
        log_prefix (str): Prefix for log messages
        verify_stderr (bool, default True): Check command stderr
        shell (bool, default False): run subprocess with shell toggle
        timeout (int, optional): Command wait timeout
        capture_output (bool, default False): Capture command output
        check (boot, default True):  If check is True and the exit code was non-zero, it raises a
            CalledProcessError
        file_path (str, optional): Write command output and error to file

    Returns:
        tuple: True, out if command succeeded, False, err otherwise.
    """

    def _write_to_file(_file_path, _out_decoded, _err_decoded=None):
        try:
            with open(file_path, "w") as fd:
                fd.write(f"stdout: {out_decoded}")
                if _err_decoded:
                    fd.write(f"\nstderr: {err_decoded}")
        except Exception as ex:
            FLASK_APP.logger.error(
                f"{log_prefix} Failed to write to file: {file_path}. ex: {ex}"
            )

    out_decoded, err_decoded = "", ""
    try:
        FLASK_APP.logger.info(f"{log_prefix} Running '{command}' command")
        sub_process = subprocess.run(
            shlex.split(command),
            capture_output=capture_output,
            check=check,
            shell=shell,
            text=True,
            timeout=timeout,
            **kwargs,
        )
        out_decoded = sub_process.stdout
        err_decoded = sub_process.stderr

        error_msg = (
            f"{log_prefix} Failed to run '{command}'. "
            f"rc: {sub_process.returncode}, out: {out_decoded}, error: {err_decoded}"
        )

        if sub_process.returncode != 0:
            FLASK_APP.logger.error(error_msg)
            if file_path:
                _write_to_file(
                    _file_path=file_path,
                    _out_decoded=out_decoded,
                    _err_decoded=err_decoded,
                )

            return False, out_decoded, err_decoded

        # From this point and onwards we are guaranteed that sub_process.returncode == 0
        if err_decoded and verify_stderr:
            FLASK_APP.logger.error(error_msg)
            if file_path:
                _write_to_file(
                    _file_path=file_path,
                    _out_decoded=out_decoded,
                    _err_decoded=err_decoded,
                )

            return False, out_decoded, err_decoded

        if file_path:
            _write_to_file(_file_path=file_path, _out_decoded=out_decoded)

        return True, out_decoded, err_decoded
    except Exception as ex:
        FLASK_APP.logger.error(f"{log_prefix} Failed to run '{command}' command: {ex}")
        if file_path:
            _write_to_file(
                _file_path=file_path, _out_decoded=out_decoded, _err_decoded=err_decoded
            )

        return False, out_decoded, err_decoded


@ignore_exceptions(logger=FLASK_APP.logger, retry=5)
def check_rate_limit(github_api=None):
    if not github_api:
        config_data = get_data_from_config()
        github_api = Github(login_or_token=config_data["github-token"])

    minimum_limit = 200
    rate_limit = github_api.get_rate_limit()
    rate_limit_reset = rate_limit.core.reset
    rate_limit_remaining = rate_limit.core.remaining
    rate_limit_limit = rate_limit.core.limit
    time_for_limit_reset = (
        rate_limit_reset - datetime.datetime.now(tz=datetime.timezone.utc)
    ).seconds

    if rate_limit_remaining < 500:
        rate_limit_str = f"{Fore.RED}{rate_limit_remaining}{Fore.RESET}"
    elif rate_limit_remaining < 2000:
        rate_limit_str = f"{Fore.YELLOW}{rate_limit_remaining}{Fore.RESET}"
    else:
        rate_limit_str = f"{Fore.GREEN}{rate_limit_remaining}{Fore.RESET}"

    FLASK_APP.logger.info(
        f"{Fore.CYAN}API rate limit:{Fore.RESET} Current {rate_limit_str} of {rate_limit_limit}. "
        f"Reset in {rate_limit_reset} [{datetime.timedelta(seconds=time_for_limit_reset)}] "
        f"(UTC time is {datetime.datetime.now(tz=datetime.timezone.utc)})"
    )
    while (
        datetime.datetime.now(tz=datetime.timezone.utc) < rate_limit_reset
        and rate_limit_remaining < minimum_limit
    ):
        FLASK_APP.logger.warning(
            f"Rate limit is below {minimum_limit} waiting till {rate_limit_reset}"
        )
        FLASK_APP.logger.info(
            f"Sleeping {time_for_limit_reset} seconds [{datetime.timedelta(seconds=time_for_limit_reset)}]"
        )
        time.sleep(time_for_limit_reset + 1)
        rate_limit = github_api.get_rate_limit()
        rate_limit_reset = rate_limit.core.reset
        rate_limit_remaining = rate_limit.core.remaining
