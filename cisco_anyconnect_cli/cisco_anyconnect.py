import logging
import shutil
from subprocess import Popen, PIPE, STDOUT
import os


class CiscoAnyConnect:

    def __init__(self, path):
        self.path = path
        self.bin = self.detect_binary()
        logging.info("Using " + self.bin)

    def connect(self, url, user, password):
        logging.info("Connecting to '" + url + "' as '" + user + "'")
        proc = Popen([self.bin, 'connect', url, '-s'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)

        stdout = proc.communicate(input=str(user + '\n' + password + '\n').encode())[0]
        logging.debug(stdout.decode())
        proc.wait()

    def disconnect(self):
        proc = Popen([self.bin, 'disconnect'])
        proc.communicate()

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

        raise Exception("Could not find " + executable)
