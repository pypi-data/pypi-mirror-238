import logging
import subprocess  # nosec

logger = logging.getLogger(__name__)


def run_command(
    command: str,
    exit_on_error: bool = True,
    return_stdout: bool = False,
) -> str:
    """
    Run a command in the shell.

    :param command: The command to run.
    :param exit_on_error: Whether to exit the program if the command fails.
    :param return_stdout: Whether to return the stdout of the command.
    :return: The result of the command stdout or an empty string in case return_stdout is False.
    """
    logger.debug(f"Running command: {command}")

    stdout = ""
    process = subprocess.Popen(command.split(" "), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)  # nosec
    while process.poll() is None:
        if process.stdout:
            output = process.stdout.readline().decode("utf-8").strip()
            if return_stdout:
                stdout += output
            if output:
                logger.info(output)

    if process.returncode != 0 and exit_on_error:
        exit(1)

    return stdout


def escape_quotes(value: str) -> str:
    """
    Escape quotes ' and " in a string.

    :param value: The string to escape.
    :return: The string with escaped quotes
    """
    return value.replace("'", "\\'").replace('"', '\\"')
