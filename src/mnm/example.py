from mnm import *

enable_socket_fragmentation()
enable_header_mocking()

import requests

r = requests.post('http://example.com/command.php', data={
    'cmd': 'ls'
})
print(r.text)
