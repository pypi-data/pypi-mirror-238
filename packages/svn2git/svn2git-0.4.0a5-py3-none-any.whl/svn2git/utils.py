import logging
import subprocess  # nosec
from typing import IO, AnyStr, Optional

logger = logging.getLogger(__name__)


def run_command(
    command: str | list[str],
    exit_on_error: bool = True,
    return_stdout: bool = False,
    stdin: Optional[IO[AnyStr]] = None,
) -> str:
    """
    Run a command in the shell.

    :param command: The command to run.
    :param exit_on_error: Whether to exit the program if the command fails.
    :param return_stdout: Whether to return the stdout of the command.
    :return: The result of the command stdout or an empty string in case return_stdout is False.
    """
    if stdin is None:
        logger.debug(f"Running command: {command if isinstance(command, str) else ' | '.join(command)}")

    if isinstance(command, list):
        # Pipe commands together
        commands = command.copy()
        current_command = commands.pop(0)
        process = subprocess.Popen(
            current_command.split(" "), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=stdin
        )  # nosec

        stdout = run_command(commands, exit_on_error, return_stdout, process.stdout)

        process.wait()
        return stdout
    else:
        # Deepest command run from the pipe
        stdout = ""
        process = subprocess.Popen(
            command.split(" "), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=stdin
        )  # nosec
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
