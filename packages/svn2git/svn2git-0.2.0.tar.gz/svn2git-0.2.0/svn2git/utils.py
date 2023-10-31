import logging
import subprocess  # nosec

logger = logging.getLogger(__name__)


def run_command(command: str, exit_on_error: bool = True) -> str:
    """
    Run a command in the shell.

    :param command: The command to run.
    :param exit_on_error: Whether to exit the program if the command fails.
    :return: The result of the command stdout.
    """
    logger.debug(f"Running command: {command}")
    stdout = ""
    process = subprocess.Popen(
        command.split(" "),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )  # nosec
    while process.poll() is None:
        if process.stdout:
            output = process.stdout.readline().decode("utf-8").strip()
            if output:
                stdout += output
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
