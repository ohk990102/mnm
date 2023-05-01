# mnm

This is a simple python library for pentesting firewall protected webapp.

## Installation

```bash
pip install mnm
```

## Usage

```python
import mnm
mnm.enable_socket_fragmentation()
mnm.enable_header_mocking()

import requests
requests.get('http://example.com')

mnm.disable_socket_fragmentation()
mnm.disable_header_mocking()

requests.get('http://example.com')
```

## License

MIT License
