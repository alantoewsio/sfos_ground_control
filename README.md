# SFOS Ground Control

An Automation tool for SFOS WebAdmin

## Installation

## 1: Download from Github

``` shell
git clone https://github.com/alantoewsio/sfos_ground_control.git
```

## 2a: Install Using Anaconda 

### I: Install Anaconda

* Download from https://docs.anaconda.com/anaconda/install/
* follow installation instructions

### II: Create a python environment using conda

After installation, create the conda environment from the environment.yml stored in the root of the project:

``` shell
conda env create -f environment.yml
```
## 2b: Install using venv

### I: Create virtual environment

* Open a command prompt in the folder SGC is installed in, then run the following:

``` shell
python -m venv .
```

### II: Install requirements
* From a command prompt in the SFC install folder, and with the venv loaded, run:

``` shell
pip install -r requirements.txt
```

Respond to any prompts raised by pip install. 

## 3: Create firewall inventory

The first step in managing firewalls is creating an inventory of firewalls to access and manage. The inventory file must be  in yaml format, and should contain access information for each firewall to be managed. A single firewall record must contain at least a hostname, but may contain more fields as desired. Any additional fields not listed below will be ignored.

### Firewall Inventory Settings

#### YAML Fields Per Firewall

|Field|Description||Default|
|-----|----------|--|--|
|```hostname```| IP address or dns name of the firewall| _**Required**_||
|```port```| WebAdmin listening port|Optional|4444|
|```username```| WebAdmin username|Optional|admin|
|```password```| WebAdmin password NOT RECOMMENDED. IF USED, INVENTORY FILE ACCESS SHOULD BE HIGHLY RESTRICTED|Optional||
|```verify_tls```| Possible values: **True**, **False** - Must be **False** if firewall uses a self-signed certificate |Optional|True|

Default credentials and settings may be stored in environment variables, or in a hashicorp vault. If not provided in the inventory, the values loaded from the vault, environment variables, or from command line arguments will be preferred in that order.

#### Supported Environment Variables

|Name|Description|
|-|-|
|```fw_username```| WebAdmin username|
|```fw_password```| WebAdmin password|
|```VAULT_MOUNT_POINT```| Hashicorp secure store info|
|```VAULT_SECRET_PATH```| Hashicorp secure store info|
|```VAULT_SECRET_KEY```| Hashicorp secure store info|

#### Supported Base Command Line Arguments

|Argument|Description|Required|Default|
|-|-|-|-|
|```-h```, ```--help```| Show console help|_Optional_||
|```--hostname <address>```|Hostname or ip|_Optional_||
|```--port```|WebAdmin port|_Optional_|4444|
|```--self-signed-cert```|Same as verify_tls: False|_Optional_|True|
|```--username```|WebAdmin user|_Optional_|admin|
|```--password```|WebAdmin password|_Optional_||
|```-i```,```--inventory-file```|Firewall inventory YAML file path|_Optional_||
|||_Optional_||

### Examples

``` yaml
- hostname: 10.23.32.1
  port: 4444
- hostname: firewall-1.mydomain.com
  verify_tls: False
- hostname: firewall-2.mydomain.com
  port: 5555
  username: someuser
  password: mysecretpassword
  verify_tls: False
```

Each firewall to be monitored must be supplied a valid username and password to login. Credentials may be provided in several ways:

* Per firewall via yaml file
* Defaults may be set as environment variables
* Defaults may be set with command line arguments
  
Username, port, and verify_tls each have system defauls set that will be used if no other values are given. For each connection field, default values will be used when available, unless they are supplied in the yaml file. Defaults set via environment variables or command line arguments will override system defaults and be used if no settings are present in the firewall inventory.

## Running gccli.py

gccli.py's primary task is to collect and store firewall details. When run with no other actions set, it will attempt to contact each firewall and collect a snapshot of several core info fields.

### fwinfo table

The core information it collects is as follows:

|Field|description|
|-|-|
|address|WebAdmin address information was collected from|
|Model|Appliance model name|
|displayVersion|Firmware version in descriptive format|
|Firmware Version|Firmware version in machine readable format|
|serial_number|Serial Number of the firewall|
|username|User account used to collect the info|
|verify_tls|Was Certificate confirmed as valid when info was collected?|
|record_date|The date recorded by the firewall, that it last received an updated license|
|Message|Error message if collection fails|
|timestamp|System time that the information was stored in the database, as reported by gccli.py|

### fwsubs table

|Field|description|
|-|-|
|serial_number|Serial Number of the firewall|
|name|Subscription name|
|start|Starting date when the subscriptions coverage begins|
|end|Ending date when the subscriptions coverage finishes|
|timeframe|The interval from the record timestamp to the end date of the subscription simplified to the most significant unit (days, weeks, years)|
|timestamp|System time that the information was stored in the database, as reported by gccli.py|

Each firewall will have one record per subscription per successful sync.

Usage Examples:

Simple update - assumes all credential information is supplied by environment variables or in firewalls.yaml.

``` shell
python gccli.py -i firewalls.yaml
```

Results will be added to grond_control.sqlite3 database file.

``` shell
python gccli.py -i firewalls.yaml --username gcuser -c refresh
```

Launching the web user interface:
``` shell
streamlit run ground_control.py
```