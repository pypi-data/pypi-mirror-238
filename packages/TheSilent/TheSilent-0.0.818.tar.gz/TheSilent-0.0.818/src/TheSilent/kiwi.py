import ipaddress
import json
import os
import random
import re
import socket
import ssl
import time
from TheSilent.clear import clear

CYAN = "\033[1;36m"

def kiwi(host,delay=0):
    clear()
    init_host = host
    hits = []
    if re.search("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2}$",host):
        hosts = []
        for _ in ipaddress.ip_network(host,strict=False):
            hosts.append(str(_))
        hosts = random.sample(hosts,len(hosts))

    else:
        hosts = [host]

    if re.search("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",host):
        subnet = True

    else:
        subnet = False
    
    subdomains = ["","adfs","aes","airwatch","aplus","apps","asg","atriuum","autodiscover","backup","barracuda","bbb","citrix","cl","destiny","dns1","docefill","documentservices","dsviewer","ees","eforms","es","ess","etcentral","etsts","exchange","filewave","filter","finance","forms","ftp","helpdesk","iboss","inow","inowhome","intranet","lib","library","lightspeed","links","lms","mail","mail2","maintenance","mdm","mealapps","media","mes","moodle","myfiles","mypay","newmail","ns","ns1","ns2","oldmail","parentportal","passwordreset","payroll","pdexpress","portal","proxy","ps","registration","relay","rocket","router","scs","sets","sftp","sis","sms","smtp","sso","staffportal","sti","studentportal","support","technology","tes","transportation","utm","voip-expressway-e","vpn","web","webmail","websets","wiki","www","www2"]
    for host in hosts:
        if subnet:
            subdomains = [""]
        else:
            subdomains = random.sample(subdomains,len(subdomains))
        for _ in subdomains:
            success = False

            if _ == "":
                dns_host = host
            else:
                dns_host = f"{_}.{host}"

            # check reverse dns
            print(CYAN + f"checking for reverse dns on {dns_host}")
            time.sleep(delay)
            try:
                hits.append(f"reverse dns {dns_host}: {socket.gethostbyaddr(dns_host)}")
                success = True
            except:
                pass
            # check if host is up
            print(CYAN + f"checking {dns_host}")
            time.sleep(delay)
            try:
                my_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                my_socket.settimeout(1.25)
                my_socket.connect((dns_host,80))
                my_socket.close()
                hits.append(f"found {dns_host}")
                success = True
            except ConnectionRefusedError:
                hits.append(f"found {dns_host}")
                success = True
            except socket.timeout:
                hits.append(f"found {dns_host}")
                success = True
            except:
                pass

            if success:
                # check ssl cert info
                print(CYAN + f"checking ssl cert on: {dns_host}")
                time.sleep(delay)
                try:
                    context = ssl.create_default_context()
                    context.check_hostname = True
                    ssl_socket = context.wrap_socket(socket.socket(socket.AF_INET),server_hostname=dns_host)
                    ssl_socket.settimeout(10)
                    ssl_socket.connect((dns_host,443))
                    data = ssl_socket.getpeercert()
                    ssl_socket.close()
                    hits.append(f"ssl cert info {dns_host}: {json.dumps(data,sort_keys=True,indent=4)}")
                except:
                    pass
                time.sleep(delay)
                try:
                    context = ssl.create_default_context()
                    context.check_hostname = True
                    ssl_socket = context.wrap_socket(socket.socket(socket.AF_INET),server_hostname=dns_host)
                    ssl_socket.settimeout(10)
                    ssl_socket.connect((dns_host,8443))
                    data = ssl_socket.getpeercert()
                    ssl_socket.close()
                    hits.append(f"ssl cert info {dns_host}: {json.dumps(data,sort_keys=True,indent=4)}")
                except:
                    pass

    clear()
    hits = list(set(hits[:]))
    hits.sort()
    with open(f"{init_host.replace('/','[]')}.txt","a") as file:
        for hit in hits:
            file.write(f"{hit}\n")

    print(CYAN + f"{len(hits)} results written to {init_host.replace('/','[]')}.txt")
