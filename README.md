[![PyPi Version Alt](https://badge.fury.io/py/cisco-anyconnect-cli.svg)](https://pypi.org/project/cisco-anyconnect-cli/)  

# cisco-anyconnect-cli
Cisco AnyConnect client command line with KeePass support

# Installation
KeePassHTTP Plugin is required
vpncli.exe from Cisco AnyConnect Secure Mobility Client is required  
`pip install cisco_anyconnect_cli`

# Usage
```
Usage: anyconnect [OPTIONS] COMMAND [ARGS]...

  Connect to Cisco AnyConnect VPN Gateway

  I need vpncli.exe and will search in:

  - Current working directory
  - C:\Program Files (x86)\Cisco\Cisco AnyConnect Secure Mobility Client
  - C:\Program Files\Cisco\Cisco AnyConnect Secure Mobility Client"
  - /opt/cisco/anyconnect/bin
  - In -p/--path given to the command (as file or directory)
  - In CISCO_ANYCONNECT_HOME environment variable
  - Availability in PATH variable

Options:
  -p, --path PATH  Directory or path to vpncli.exe
  -h, --help       Show this message and exit.

Commands:
  connect     Connect to a cisco vpn server
  disconnect  Disconnect
  state       Get connection status
```

## Connect
User and password will be fetched from Keepass if no user is given
```
Usage: anyconnect connect [OPTIONS] URL

  Endpoint address

Options:
  -u, --user TEXT                 Give username instead of KeePass lookup
  -p, --password TEXT             Give password instead of KeePass lookup
  --autorespond / --noautorespond Defines whether connect will automatically
                                  respond to login banners
  -k, --insecure                  Allow insecure server connections
  --help                          Show this message and exit.
```

# Examples
```
Entry in KeePass must be named or have a configured URL equal vpn-server-url.
$ anyconnect connect vpn.example.com

Without KeePass 
$ anyconnect connect vpn.example.com -u user -p pass

$ anyconnect disconnect
```

# Changelog
## v0.6
- Added support for insecure connections

## v0.5
- Added linux support

## v0.4
- Added autorespond to login banners (thanks @ott-egs-plan)

## v0.2
- Added state command (thanks @GOST-UA)

## v0.1
- Initial version with basic features
