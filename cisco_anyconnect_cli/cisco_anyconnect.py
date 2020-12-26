import logging
import shutil
from subprocess import Popen, PIPE, STDOUT
import os
import re


class CiscoAnyConnect:

    def __init__(self, path=None):
        self.path = path
        self.bin = self.detect_binary()
        logging.info(f"Using {self.bin}")

    def connect(self, url: str, user: str, password: str):
        logging.info(f"Connecting to '{url}' as '{user}'")
        proc = Popen([self.bin, "connect", url, "-s"], stdout=PIPE, stdin=PIPE, stderr=STDOUT)

        stdout = proc.communicate(input=f"{user}\n{password}\n".encode())[0]
        logging.debug(stdout.decode())
        proc.wait()

    def disconnect(self):
        proc = Popen([self.bin, "disconnect"])
        proc.communicate()

    def state(self) -> str:
        """
        Get connection state. Return actual state or Unknown if result was unexpected
        """
        proc = Popen([self.bin, "state"], stdout=PIPE, stderr=STDOUT)
        stdout = proc.communicate()[0].decode()
        patt = re.compile(r".*state: (\w+)", re.MULTILINE)
        res = re.findall(patt, stdout)

        state = res[-1] if res else "Unknown"

        logging.debug(state)
        return state

    def detect_binary(self):
        executable = "vpncli.exe"
        env_home = os.environ.get("CISCO_ANYCONNECT_HOME")
        env_path = shutil.which(executable)

        possible_paths = [
            os.path.join(os.getcwd(), executable),
            os.path.join("C:\\Program Files (x86)\\Cisco\\Cisco AnyConnect Secure Mobility Client", executable),
            os.path.join("C:\\Program Files\\Cisco\\Cisco AnyConnect Secure Mobility Client", executable),
            os.path.join(env_home, executable) if env_home is not None else None,
            self.path if self.path is not None else None,
            os.path.join(self.path, executable) if self.path is not None else None,
            os.path.join(env_path) if env_path is not None else None
        ]

        for path in possible_paths:
            if path is not None and os.path.isfile(path):
                return path

        raise Exception(f"Could not find  {executable}")
