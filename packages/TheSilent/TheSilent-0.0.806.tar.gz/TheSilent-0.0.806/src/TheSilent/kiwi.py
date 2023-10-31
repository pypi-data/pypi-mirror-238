import random
import socket
import ssl
import time
from TheSilent.clear import clear

CYAN = "\033[1;36m"

def kiwi(host,delay=0):
    clear()
    hits = []
    init_hosts = []
    hosts = []

    subdomains = ["","adfs","aes","airwatch","aplus","apps","asg","atriuum","autodiscover","backup","barracuda","bbb","citrix","cl","destiny","dns1","docefill","documentservices","dsviewer","ees","eforms","es","ess","etcentral","etsts","exchange","filewave","filter","finance","forms","ftp","helpdesk","iboss","inow","inowhome","intranet","lib","library","lightspeed","lms","mail","mail2","maintenance","mdm","mealapps","media","mes","moodle","myfiles","mypay","newmail","ns","ns1","ns2","oldmail","parentportal","passwordreset","payroll","portal","proxy","registration","relay","rocket","scs","sets","sftp","sis","sms","smtp","sso","staffportal","sti","studentportal","support","technology","tes","transportation","utm","voip-expressway-e","vpn","web","webmail","websets","wiki","www","www2"]
    subdomains = random.sample(subdomains,len(subdomains))
    for _ in subdomains:
        # check reverse dns
        print(CYAN + f"checking for reverse dns on {_}.{host}")
        if _ == "":
            dns_host = host
        else:
            dns_host = f"{_}.{host}"
        time.sleep(delay)
        try:
            hits.append(f"reverse dns {dns_host}: {socket.gethostbyaddr(dns_host)}")
        except:
            pass
        # check if host is up
        print(CYAN + f"checking {dns_host}")
        try:
            my_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            my_socket.settimeout(1.25)
            my_socket.connect((dns_host,80))
            my_socket.close()
            hits.append(f"found {dns_host}")
        except ConnectionRefusedError:
            hits.append(f"found {dns_host}")
        except socket.timeout:
            hits.append(f"found {dns_host}")
        except:
            pass

        try:
            context = ssl.create_default_context()
            context.check_hostname = True
            ssl_socket = context.wrap_socket(socket.socket(socket.AF_INET),server_hostname=dns_host)
            ssl_socket.settimeout(1.25)
            ssl_socket.connect((dns_host,443))
            data = ssl_socket.getpeercert()
            ssl_socket.close()
            cert = data["serialNumber"]
            hits.append(f"ssl serial number {dns_host}: {data['serialNumber']}")
            hits.append(f"ssl expires {dns_host}: {data['notAfter']}")
        except:
            pass

    clear()
    hits.sort()
    for hit in hits:
        print(CYAN + hit)

    with open(f"{host}.txt","a") as file:
        for hit in hits:
            file.write(f"{hit}\n")

    print(CYAN + f"{len(hits)} results")
