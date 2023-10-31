import time
from dataclasses import dataclass, field
from typing import List, Optional, Union

import paramiko

from guerrilla.connection.session import BaseSession
from guerrilla.logging import COLOR, logger

COMMAND_AWAIT = 0.5  # default: 5 seconds]
RECEIVE_AWAIT = 0.1  # default: 0.1 seconds


@dataclass
class SSHSession(BaseSession):
    """
    A class representing an SSH session.

    Attributes:
    -----------
    host : str
        The hostname or IP address of the remote server.
    username : str
        The username to use for authentication.
    password : str
        The password to use for authentication.
    name : str, optional
        A name for the session.
    os_type : str, optional
        The operating system type of the remote server.
    port : int, optional
        The port number to use for the SSH connection (default is 22).
    client : paramiko.SSHClient, optional
        The SSH client object to use for the session (default is a new instance of paramiko.SSHClient).
    channel : paramiko.Channel, optional
        The SSH channel object to use for the session.
    """

    host: str
    username: str
    password: str
    port: int = 22
    client: paramiko.SSHClient = field(default_factory=paramiko.SSHClient, init=False)
    channel: paramiko.Channel = field(init=False)

    def __post_init__(self):
        """
        Initializes the SSH client and sets the missing host key policy.
        """
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        logger.info(f"Created {self.name}'s SSH session to {self.host}:{self.port}")

    def __del__(self):
        """
        Closes the SSH connection when the object is deleted.
        """
        self.disconnect()

    def _is_alive(self) -> bool:
        """
        Checks if the SSH channel is still active.

        Returns:
        --------
        bool
            True if the channel is active, False otherwise.
        """
        transport = self.client.get_transport()
        return transport and transport.is_active()

    def connect(self):
        """
        Connects to the remote server using SSH.
        """
        try:
            self.client.connect(self.host, self.port, self.username, self.password)
            self.channel = self.client.invoke_shell()
            logger.success(f"Connected to {self.name} {self.host}:{self.port}")
            self.read_from_channel()
        except paramiko.AuthenticationException:
            logger.error(
                f"Authentication failed when connecting to {self.host}:{self.port}"
            )
            raise Exception("Authentication failed, please verify your credentials")

    def disconnect(self):
        """
        Closes the SSH connection.
        """
        try:
            self.client.get_transport().close()
            logger.info(f"Closed connection to {self.host}:{self.port}")
        except Exception:
            logger.error(f"Error when closing connection to {self.host}:{self.port}")
            raise ConnectionError("Could not close connection")

    def _recv_data(self, timeout: int, end_marks: Optional[List[str]] = None) -> str:
        """
        Receives data from the SSH channel.

        Parameters:
        -----------
        timeout : int
            The maximum amount of time to wait for data (in seconds).
        end_marks : List[str], optional
            A list of strings that indicate the end of the data.

        Returns:
        --------
        str
            The received data.
        """
        end_time = time.time() + timeout
        accumulated_output = ""

        while time.time() < end_time:
            if self.channel.recv_ready():
                result = self.channel.recv(32768).decode("utf-8")
                accumulated_output += result
                if end_marks and any(
                    end_mark in accumulated_output for end_mark in end_marks
                ):
                    return accumulated_output
                elif not end_marks:
                    return accumulated_output
            elif not self._is_alive():
                raise ConnectionError("SSH channel is not active anymore.")
            time.sleep(RECEIVE_AWAIT)
        return accumulated_output

    def read_from_channel(
        self,
        timeout: int = 5,
        end_marks: Optional[List[str]] = None,
        debug: bool = False,
    ) -> str:
        """
        Reads data from the SSH channel.

        Parameters:
        -----------
        timeout : int, optional
            The maximum amount of time to wait for data (in seconds).
        end_marks : List[str], optional
            A list of strings that indicate the end of the data.
        debug : bool, optional
            Whether to print debug information.

        Returns:
        --------
        str
            The received data.
        """
        output = self._recv_data(timeout, end_marks)
        if not output:
            logger.error(f"No data received from channel within {timeout} seconds.")
            raise TimeoutError(f"No response received after {timeout} seconds.")
        return output

    def _run_channel_command(
        self,
        command: str,
        timeout: int,
        expect_return: Optional[Union[str, List[str]]],
        debug: bool,
    ) -> str:
        """
        Runs a command on the SSH channel.

        Parameters:
        -----------
        command : str
            The command to run.
        timeout : int
            The maximum amount of time to wait for data (in seconds).
        expect_return : Union[str, List[str]], optional
            A string or list of strings that indicate the end of the data.
        debug : bool, optional
            Whether to print debug information.

        Returns:
        --------
        str
            The output of the command.
        """
        self.channel.send(command + "\n")
        time.sleep(COMMAND_AWAIT)
        if expect_return is not None:
            expect_return = (
                [expect_return] if isinstance(expect_return, str) else expect_return
            )
            return self.read_from_channel(
                timeout=timeout, end_marks=expect_return, debug=debug
            )
        else:
            return self.read_from_channel(timeout=timeout, debug=debug)

    def run(
        self,
        command: str,
        print_output: bool = False,
        expect_return: Union[str, List[str], None] = None,
        timeout: int = 5,
        debug: bool = False,
    ) -> str:
        """
        Runs a command on the SSH channel and returns the output.

        Parameters:
        -----------
        command : str
            The command to run.
        print_output : bool, optional
            Whether to print the output to the console.
        expect_return : Union[str, List[str], None], optional
            A string or list of strings that indicate the end of the data.
        timeout : int, optional
            The maximum amount of time to wait for data (in seconds).
        debug : bool, optional
            Whether to print debug information.

        Returns:
        --------
        str
            The output of the command.
        """
        log_message = f"From {COLOR.magenta(self.name):<{10}}     {COLOR.red('sent command:')} {command}"
        if expect_return:
            log_message += f" {COLOR.yellow('expecting:')} {expect_return}"
        logger.debug(log_message)

        full_output = self._run_channel_command(command, timeout, expect_return, debug)

        logger.debug(
            f"From {COLOR.magenta(self.name):<{10}} {COLOR.green('received  output:')} {full_output.strip()}"
        )
        if print_output:
            print(full_output)
        return full_output

    def find_prompt(self) -> str:
        """
        Finds the prompt of the remote server.

        Returns:
        --------
        str
            The prompt.
        """
        output = self.run("")
        prompt = output.strip()

        return prompt
