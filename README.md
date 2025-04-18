# SFOS Ground Control

An Automation tool for SFOS WebAdmin

## Setup Prerequisites

## Download from Github

```shell
git clone https://github.com/alantoewsio/sfos_ground_control.git
```

### uv: Recommended Install

- [Install using recommended instructions](https://docs.astral.sh/uv/getting-started/installation/) (On windows, requires running powershell scripts)
- follow installation instructions
- Test that uv is installed correctly by running `uv --version` from a new shell window
- or: run `. online_uv_setup` from the project rood directory

### uv: Alternate Install

- [Alternate: directly download binaries](https://github.com/astral-sh/uv/releases) (Choose the correct package for your OS)
- Extract binaries
- Open a powershell prompt
- Windows: navigate to the path where the extracted binaries are located, and run:

  - `. manual_uv_setup.ps1`

- Place exe in system path folder, or in the root of the project folder closed

## 3: Setup

- From project directory
  - On Windows powershell: run `. setup_environment.ps1`

## 4: Create firewall inventory

The first step in managing firewalls is creating an inventory of firewalls to access and manage. The inventory file must be in yaml format, and should contain access information for each firewall to be managed. A single firewall record must contain at least a hostname, but may contain more fields as desired. Any additional fields not listed below will be ignored.

### Firewall Inventory Settings

Firewall inventory may be stored in yaml, json, or csv formats. 
Each file format expects the same field names to be used and supports all fields except the hostname as optional.

#### Fields Per Firewall

| Field        | Description                                                                                         |                | Default |
| ------------ | --------------------------------------------------------------------------------------------------- | -------------- | ------- |
| `hostname`   | IP address or dns name of the firewall                                                              | _**Required**_ |         |
| `port`       | WebAdmin listening port                                                                             | Optional       | 4444    |
| `username`   | WebAdmin username                                                                                   | Optional       | admin   |
| `password`   | WebAdmin password NOT RECOMMENDED. IF USED, INVENTORY FILE ACCESS SHOULD BE HIGHLY RESTRICTED       | Optional       |         |
| `verify_tls` | Possible values: **True**, **False** - Must be **False** if firewall uses a self-signed certificate | Optional       | True    |

Default credentials and settings may be stored in environment variables, or in a hashicorp vault. If not provided in the inventory, the values loaded from the vault, environment variables, or from command line arguments will be preferred in that order.

#### Supported Environment Variables

| Name                | Description                          | Defaults                 |
| ------------------- | ------------------------------------ | ------------------------ |
| `fw_username`       | WebAdmin username                    |                          |
| `fw_password`       | WebAdmin password                    |                          |
| `VAULT_MOUNT_POINT` | Hashicorp secure store info          |                          |
| `VAULT_SECRET_PATH` | Hashicorp secure store info          |                          |
| `VAULT_SECRET_KEY`  | Hashicorp secure store info          |                          |
| `GC_DATABASE_FILE`  | Filename used for storing event data | ./ground_control.sqlite3 |
| `GC_OUTPUT_PATH` | Folder where csv output files will be written. | defaults to the current folder | 
| `GC_DEFAULT_TIMEOUT` | Default timeout value in seconds for all connections | 10 |

#### Supported Base Command Line Arguments

| Argument                | Description                       | Required   | Default |
| ----------------------- | --------------------------------- | ---------- | ------- |
| `-h`, `--help`          | Show console help                 | _Optional_ |         |
| `--hostname <address>`  | Hostname or ip                    | _Optional_ |         |
| `--port`                | WebAdmin port                     | _Optional_ | 4444    |
| `--self-signed-cert`    | Same as verify_tls: False         | _Optional_ | True    |
| `--username`            | WebAdmin user                     | _Optional_ | admin   |
| `--password`            | WebAdmin password                 | _Optional_ |         |
| `-i`,`--inventory-file` | Firewall inventory YAML file path | _Optional_ |         |
|                         |                                   | _Optional_ |         |

### Examples

#### YAML file example with various field combinations

Define only the hostname and any fields to be defined per host. Fields may be included or exclude per record, as needed.

> YAML files must have a '.yaml' or '.yml' file extension

```yaml
- hostname: example-host1.network.com
- hostname: example-host2.network.com
  verify_tls: false
- hostname: example-host3.network.com
  username: firewalladmin
  password: secret_value_def
- hostname: example-host4.network.com
  port: 4444
  verify_tls: false
  username: firewalluser
  password: secret_value_xyz
  timeout: 5

```

#### JSON file example with various field combinations

Define only the hostname and any fields to be defined per host. Fields may be included or exclude per record, as needed.

Field names, and string values must be quoted. integer and boolean values must not be quoted.

fields and firewall records must each be separated with a comma.

> JSON files must have a '.json' file extension

```json
[
  {
    "hostname": "example-host1.network.com"
  },
  {
    "hostname": "example-host2.network.com",   
    "verify_tls": false
  },
  {
    "hostname": "example-host3.network.com",
    "username": "firewalladmin",
    "password": "secret_value_def"
  },
  {
    "hostname": "example-host4.network.com",
    "port": 4444,
    "verify_tls": false,
    "username": "firewalluser",
    "password": "secret_value_xyz",
    "timeout": 5
  }
]
```

#### CSV file examples

Define only the hostname and any fields to be defined per host. Fields MUST be included or excluded in the header row, if theyu are to be included for any firewall records.

Field names and values do not need to be quoted unless the value contains a separator character ','

Columns defined in the header do not need to be included in each row, if no following columns will have theior values set.

> CSV files must have a '.csv' file extension

#### CSV file with all fields defined

```csv
"hostname", "port", "username", "password", "verify_tls", timeout
example-host.network.com
example-host2.network.com,,, secret_value_abc, false
example-host3.network.com,, firewalladmin, secret_value_def
example-host4.network.com, 4444, firewalluser, secret_value_xy, false, 5
```

#### CSV file with fewer columns

```csv
hostname, username, verify_tls
example-host.network.com, admin2, false
example-host2.network.com
example-host3.network.com
example-host4.network.com,,false
```

Each firewall to be monitored must be supplied a valid username and password to login. Credentials may be provided in several ways:

- Per firewall via yaml/json/csv file
- Defaults may be set as environment variables
- Defaults may be set with command line arguments

Username, port, and verify_tls each have system defauls set that will be used if no other values are given. For each connection field, default values will be used when available, unless they are supplied in the yaml file. Defaults set via environment variables or command line arguments will override system defaults and be used if no settings are present in the firewall inventory.

## Running gccli ('gccli.exe' or 'uv run gccli.py')

gccli.py's primary task is to collect and store firewall details. When run with no other actions set, it will attempt to contact each firewall and collect a snapshot of several core info fields.

### fwinfo table

The core information it collects is as follows:

| Field            | description                                                                          |
| ---------------- | ------------------------------------------------------------------------------------ |
| address          | WebAdmin address information was collected from                                      |
| Model            | Appliance model name                                                                 |
| displayVersion   | Firmware version in descriptive format                                               |
| Firmware Version | Firmware version in machine readable format                                          |
| serial_number    | Serial Number of the firewall                                                        |
| username         | User account used to collect the info                                                |
| verify_tls       | Was Certificate confirmed as valid when info was collected?                          |
| record_date      | The date recorded by the firewall, that it last received an updated license          |
| Message          | Error message if collection fails                                                    |
| timestamp        | System time that the information was stored in the database, as reported by gccli.py |

### fwsubs table

| Field         | description                                                                                                                             |
| ------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| serial_number | Serial Number of the firewall                                                                                                           |
| name          | Subscription name                                                                                                                       |
| start         | Starting date when the subscriptions coverage begins                                                                                    |
| end           | Ending date when the subscriptions coverage finishes                                                                                    |
| timeframe     | The interval from the record timestamp to the end date of the subscription simplified to the most significant unit (days, weeks, years) |
| timestamp     | System time that the information was stored in the database, as reported by gccli.py                                                    |

Each firewall will have one record per subscription per successful sync.

Usage Examples:

Simple update - assumes all credential information is supplied by environment variables or in firewalls.yaml.

```shell
gccli.exe -i firewalls.yaml
- or -
uv gccli.py -i firewalls.yaml
```

Results will be added to ground_control.sqlite3 database file.

```shell
gccli.exe -i firewalls.yaml --username gcuser -c refresh
- or -
uv gccli.py -i firewalls.yaml --username gcuser -c refresh
```


## Error Messages

### Firewall authentication errors

- Incorrect username or password

> May be caused by the Username or password being rejected by the firewall, or login attempts being blocked temporarily from previous repeated failures.

- Blocked by disclaimer

> Username and password were accepted, but login requires a user to accept a login disclaimer

- Unable to authenticate
  
> 

- Invalid Certificate

> The firewall is using an untrusted certificate. Can be caused by using a self-signed certificate, an expired or revooked certificate, or a certificate whose CA cannot be validated by the app. If this is expected, be sure to set verify_tls to false, or pass the --insecure argument when calling the agent

### Network Connectivity Errors

- Connection timed out

> The firewall did not respond in time to the connection attempt

- DNS Error

> DNS resolution has failed for the firewall's hostname. Can be caused by an invalid hostname entry, or a dns service failure

- Connection error 'additional description'

> A network connection error other than the ones mnetioned above was raised by the host OS, and any additional description from the OS will be provided in the message.


### Other Connectivity-Related Errors

Some errors will indicate that the firewall interaction was not fully as expected. This may be due to an application bug, the address pointing to another device that is respnding on the address and port, or from a firewall behavior change after major firewall firmware update. The correct troubleshooting steps in this case is to verify the address and port are correct, the firewall credentials are correct, and that the firewall address and port may be accessed in a browser from the system where the agent is being run.

- Not Authenticated
- Unexpected auth response
- Unable to authenticate
- Unexcpected result - Check ADMIN_LOGIN definition is correct
- No license data in response
- Missing keys {missing}\nFound keys:{v_keys}

> A firewall response did not contain all of the expected information.

### Application Errors

- No database

> The application was unable to initialize the database connection. May be caused by a bug or if the application does not have sufficient OS permissions.
