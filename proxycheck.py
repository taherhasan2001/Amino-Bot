from threading import Thread, Lock
from requests import get, post
import json

lock = Lock()
ipgeolocation_io_key = "" #PROVIDE OWN KEY, 1K REQUESTS FOR FREE PER DAY

#actually not working
def ipDetails(ip):
    info = get(f"https://api.ipgeolocation.io/ipgeo?apiKey={ipgeolocation_io_key}&ip={ip}").json()
    return f"{info['ipgeolocation_io_key']}; ISP: {info['isp']}; Organization: {info['organization']}"
    

def check(proxy, i, printException = True, print403 = True, printIpDetails = False):
    try:
        c = post("https://service.narvii.com/api/v1/x64546570/s/chat/thread", proxies=proxy)
        if c.status_code == 403 and print403: print(f"[!] Proxy {i+1} ({proxy['https']}) got {c.status_code}")
        elif c.status_code == 400:
            print(f"[V] Proxy {i+1} ({proxy['https']}) got usual {c.status_code}")
            with lock:
                with open('good-proxies.txt', 'a') as file:
                    file.write(f"{proxy['https']}\n")
        elif c.status_code != 403:
            print(f"[!] Proxy {i+1} ({proxy['https']}) got unusual {c.status_code}")
    except:
        if printException: print(f"[X] Cant connect to {i+1} ({proxy['https']})")
    
with open ("proxies.txt") as file:
    i = 1
    for line in file:
        line = line.rstrip().split(':')
        
        Thread(target=check, args=({"https": f"{line[0]}:{line[1]}"}, i, False, False, False, )).start()
        i+=1