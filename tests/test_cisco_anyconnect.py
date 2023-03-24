import os
import unittest
from cisco_anyconnect_cli.cisco_anyconnect import CiscoAnyConnect
from unittest.mock import patch

if os.name == 'nt':
    executable = "vpncli.exe"
elif os.name == 'posix':
    executable = "vpn"


class CiscoAnyConnectTest(unittest.TestCase):

    @patch('os.path.exists')
    @patch('os.path.isfile')
    def test_detect_binary_throws_exception_when_not_found(self, mock_isfile, mock_exists):
        mock_exists.side_effect = lambda path: False
        mock_isfile.side_effect = lambda file: False

        self.assertRaises(Exception, CiscoAnyConnect)

    @patch('os.path.isfile')
    def test_detect_binary_cwd(self, mock_isfile):
        expected = os.path.join(os.getcwd(), executable)
        mock_isfile.side_effect = lambda file: os.path.normpath(file) == os.path.normpath(expected)

        cisco = CiscoAnyConnect(None)

        print("Actual: " + cisco.bin)
        print("Expected: " + expected)
        assert cisco.bin == expected

    @patch('os.path.isfile')
    def test_detect_binary_ProgramFiles(self, mock_isfile):
        expected = os.path.join("C:\\Program Files\\Cisco\\Cisco AnyConnect Secure Mobility Client", executable)
        mock_isfile.side_effect = lambda file: os.path.normpath(file) == os.path.normpath(expected)

        cisco = CiscoAnyConnect(None)

        print("Actual: " + cisco.bin)
        print("Expected: " + expected)
        assert cisco.bin == expected

    @patch('os.path.isfile')
    def test_detect_binary_ProgramFilesX86(self, mock_isfile):
        expected = os.path.join("C:\\Program Files (x86)\\Cisco\\Cisco AnyConnect Secure Mobility Client", executable)
        mock_isfile.side_effect = lambda file: os.path.normpath(file) == os.path.normpath(expected)

        cisco = CiscoAnyConnect(None)

        print("Actual: " + cisco.bin)
        print("Expected: " + expected)
        assert cisco.bin == expected

    @patch('os.path.isfile')
    def test_detect_binary_ProgramFilesX86(self, mock_isfile):
        expected = os.path.join("/opt/cisco/anyconnect/bin", executable)
        mock_isfile.side_effect = lambda file: os.path.normpath(file) == os.path.normpath(expected)

        cisco = CiscoAnyConnect(None)

        print("Actual: " + cisco.bin)
        print("Expected: " + expected)
        assert cisco.bin == expected

    @patch('os.path.isfile')
    def test_detect_binary_given_path(self, mock_isfile):
        expected_dir = "c:\\my\\custom\\path"
        expected = os.path.join(expected_dir, executable)
        mock_isfile.side_effect = lambda path: path is not None and os.path.normpath(path) == os.path.normpath(expected)

        cisco = CiscoAnyConnect(expected_dir)

        print("Actual: " + cisco.bin)
        print("Expected: " + expected)
        assert cisco.bin == expected

    @patch('os.path.isfile')
    def test_detect_binary_given_file(self, mock_isfile):
        expected = os.path.join("c:\\my\\custom\\path", executable)
        mock_isfile.side_effect = lambda file: os.path.normpath(file) == os.path.normpath(expected)

        cisco = CiscoAnyConnect(expected)

        print("Actual: " + cisco.bin)
        print("Expected: " + expected)
        assert cisco.bin == expected

    @patch('os.path.isfile')
    @patch('shutil.which')
    def test_detect_binary_given_path_variable(self, mock_which, mock_isfile):
        expected = os.path.join("c:\\path", executable)
        mock_isfile.side_effect = lambda file: os.path.normpath(file) == os.path.normpath(expected)
        mock_which.side_effect = lambda path: expected

        cisco = CiscoAnyConnect(None)

        print("Actual: " + cisco.bin)
        print("Expected: " + expected)
        assert cisco.bin == expected

    @patch('os.path.isfile')
    @patch.dict(os.environ, {"CISCO_ANYCONNECT_HOME": "c:\\path"})
    def test_detect_binary_given_environment_variable(self, mock_isfile):
        print(os.environ.get("CISCO_ANYCONNECT_HOME"))
        expected = os.path.join("c:\\path", executable)

        def isfile(file):
            print(file)
            print(os.path.normpath(file))
            print(os.path.normpath(expected))
            return os.path.normpath(file) == os.path.normpath(expected)

        mock_isfile.side_effect = isfile

        cisco = CiscoAnyConnect(None)

        print("Actual: " + cisco.bin)
        print("Expected: " + expected)
        assert cisco.bin == expected

    @patch('os.path.isfile')
    def test_with_insecure_connect(self, mock_isfile):
        expected = os.path.join("/opt/cisco/anyconnect/bin", executable)
        mock_isfile.side_effect = lambda file: os.path.normpath(file) == os.path.normpath(expected)
        expected_input = b"y\nUSER\nPASS\n"
        with patch('cisco_anyconnect_cli.cisco_anyconnect.Popen') as mock_popen:
            cisco = CiscoAnyConnect(None)
            cisco.connect("URL", "USER", "PASS", insecure=True)
            actual = mock_popen.return_value.communicate.call_args_list[0][1]['input']
            print("Actual: " + actual.decode())
            print("Expected: " + expected_input.decode())
            assert actual == expected_input

    @patch('os.path.isfile')
    def test_without_insecure_connect(self, mock_isfile):
        expected = os.path.join("/opt/cisco/anyconnect/bin", executable)
        mock_isfile.side_effect = lambda file: os.path.normpath(file) == os.path.normpath(expected)
        expected_input = b"USER\nPASS\n"
        with patch('cisco_anyconnect_cli.cisco_anyconnect.Popen') as mock_popen:
            cisco = CiscoAnyConnect(None)
            cisco.connect("URL", "USER", "PASS", insecure=False)
            actual = mock_popen.return_value.communicate.call_args_list[0][1]['input']
            print("Actual: " + actual.decode())
            print("Expected: " + expected_input.decode())
            assert actual == expected_input

    @patch('os.path.isfile')
    def test_with_banner_accept_connect(self, mock_isfile):
        expected = os.path.join("/opt/cisco/anyconnect/bin", executable)
        mock_isfile.side_effect = lambda file: os.path.normpath(file) == os.path.normpath(expected)
        expected_input = b"USER\nPASS\ny\n"
        with patch('cisco_anyconnect_cli.cisco_anyconnect.Popen') as mock_popen:
            cisco = CiscoAnyConnect(None)
            cisco.connect("URL", "USER", "PASS", autorespond=True)
            actual = mock_popen.return_value.communicate.call_args_list[0][1]['input']
            print("Actual: " + actual.decode())
            print("Expected: " + expected_input.decode())
            assert actual == expected_input

    @patch('os.path.isfile')
    def test_with_insecure_and_banner_accept_connect(self, mock_isfile):
        expected = os.path.join("/opt/cisco/anyconnect/bin", executable)
        mock_isfile.side_effect = lambda file: os.path.normpath(file) == os.path.normpath(expected)
        expected_input = b"y\nUSER\nPASS\ny\n"
        with patch('cisco_anyconnect_cli.cisco_anyconnect.Popen') as mock_popen:
            cisco = CiscoAnyConnect(None)
            cisco.connect("URL", "USER", "PASS", autorespond=True, insecure=True)
            actual = mock_popen.return_value.communicate.call_args_list[0][1]['input']
            print("Actual: " + actual.decode())
            print("Expected: " + expected_input.decode())
            assert actual == expected_input


if __name__ == '__main__':
    unittest.main()
