import re
import os
from urllib.request import urlopen
from prettytable import PrettyTable
import time


IP = re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
AS = re.compile(".rigin\w{0,2}: *(AS[0-9]+)")
country = re.compile(".ountry: *(\w+)")
provider = re.compile("mnt-by: *([\w\d]+-[\w\d]+)")

th = ["№", "IP", "AS Name", "Country", "Provider"]

def get_IP_from_tracert(name: str):
    cmd = f"tracert {name}"
    founds_IP = IP.findall(os.popen(cmd).read())
    return founds_IP

def is_grey_IP(ip: str):
    try:
        oktet = int(ip.split('.')[1])
        return ip.startswith("10.") or (ip.startswith("100.") and (128 > oktet > 63)) or ip.startswith("192.168.") or (ip.startswith("172.") and (32 < oktet > 15))
    except:
        return True

def parser(site, pattern):
    try:
        found = pattern.findall(site)
        return found[len(found)-1]
    except:
        return ''

def get_info_from_IP(ip):
    if is_grey_IP(ip):
        return ip, 'grey', 'grey', 'grey'
    else:
        with urlopen(f'https://www.nic.ru/whois/?searchWord={ip}') as site:
            info = site.read().decode('utf-8')
            return ip, parser(info, AS), parser(info, country), parser(info, provider)

def traceroute(data):
    print("Ожидайте")
    data_table = []
    number = 0
    tracert = get_IP_from_tracert(data)
    print(tracert)
    columns = len(th)
    table = PrettyTable(th)
    for ip in tracert:
        number += 1
        data_table.append(number)
        data_table.extend(get_info_from_IP(ip))
        table.add_row(data_table[:columns])
        data_table = data_table[columns:]
        time.sleep(30)
    return table


print(traceroute(input()))