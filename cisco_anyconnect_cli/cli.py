import logging
import sys
import click
from keepasshttp import keepasshttp
from cisco_anyconnect_cli.cisco_anyconnect import CiscoAnyConnect


@click.group()
@click.option("--path", "-p", type=click.Path(exists=True, file_okay=True, dir_okay=True, readable=True),
              help="Directory or path to vpncli.exe")
@click.help_option("-h", "--help")
@click.pass_context
def main(ctx, path):
    """
    Connect to Cisco AnyConnect VPN Gateway

    I need vpncli.exe and will search in:

    \b
    - Current working directory
    - C:\\Program Files (x86)\\Cisco\\Cisco AnyConnect Secure Mobility Client
    - C:\\Program Files\\Cisco\\Cisco AnyConnect Secure Mobility Client"
    - In -p/--path given to the command (as file or directory)
    - In CISCO_ANYCONNECT_HOME environment variable
    - Availability in PATH variable
    """
    logging.basicConfig(format="[%(levelname)-5s] %(message)s", stream=sys.stdout, level=logging.DEBUG)
    ctx.obj = path
    pass


@click.command(help="Endpoint address")
@click.argument("url")
@click.option("-u", "--user", help="Give username instead of KeePass lookup")
@click.option("-p", "--password", help="Give password instead of KeePass lookup")
@click.pass_context
def connect(ctx, url, user, password):
    try:
        if user is None:
            creds = get_credentials(url)
            user = creds.login
            password = creds.password

        client = CiscoAnyConnect(ctx.obj)
        client.connect(url, user, password)
        sys.exit(0)
    except Exception as e:
        logging.error(e)
        sys.exit(1)


@click.command(help="Disconnect")
@click.pass_context
def disconnect(ctx):
    try:
        client = CiscoAnyConnect(ctx.obj)
        client.disconnect()
        sys.exit(0)
    except Exception as e:
        logging.error(e)
        sys.exit(1)


main.add_command(connect)
main.add_command(disconnect)


def get_credentials(url):
    logging.info("Retrieve credentials for '" + url + "'")
    try:
        credentials = keepasshttp.get(url)
    except Exception as e:
        raise Exception("Could not connect to KeePassHTTP", e)

    if credentials is None:
        raise Exception(
            "KeePass entry for '" + url + "' not found! Please add an entry with '" + url + "' as name or url")

    logging.info(f"Credentials found (User: {credentials.login})")
    return credentials


if __name__ == '__main__':
    main()
