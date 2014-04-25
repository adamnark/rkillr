#!/usr/bin/env python
# version 1.1 by adamn
# works for my weird-ass router, DGN2200v2

import re, sys, socket, json, requests
from bs4 import BeautifulSoup
from time import sleep
from datetime import datetime

router_url = 'http://10.0.0.138/'

def login():
    print 'setting up session. . .'
    s = requests.Session()
    with open("creds.txt","r") as f:
        json_data = open("creds.txt","r").read()
        data = json.loads(json_data)
        s.auth = (data['user'], data['pass'])
    return s

def reboot():
    s = login()
    print 'sending reboot. . . '
    params = {"Reboot":"Reboot"}
    resp = s.post(router_url + "reboot.cgi", data=params)
    print 'status code: ' + str(resp.status_code)
    if resp.status_code != 200:
        print 'retrying. . . '
        reboot()


def get_mac_addresses(logs):
    rmacs = re.compile('(([0-9A-F]{2}[:-]){5}([0-9A-F]{2}))').findall(logs)
    macs = list(set([rmac[0] for rmac in rmacs]))
     
def macs():
    s = login()
    print 'sending log request. . .'
    params = {
        "log_detail" : "1",
        "action_Refresh" : "Refresh",
        "log_bsites" : "log_bsites",
        "log_mg" : "log_mg",
        "log_op" : "log_op",
        "log_dos" : "log_dos",
        "syslog_type" : "disable",
        "lan_ipaddr0" : "10.0.0.138",
        "email_on" : "0",
        "log_refresh" : "1",
        "log_send" : "0",
        "log_clear" : "0",
        "h_log_bsites" : "1",
        "h_log_mg" : "1",
        "h_log_op" : "1",
        "h_log_dos" : "1",
        "h_syslog_type" : "0",
        "lan_ipaddr" : "0.0.0.0",
    }
    resp = s.post(router_url + 'fwLog.cgi',data=params)
    print 'status code: ' + str(resp.status_code)
    if resp.status_code != 200:
        exit()
    soup = BeautifulSoup(resp.text)
    logs = soup.find_all('textarea')[0].string
    
    macs = get_mac_addresses(logs)
    print 30*'=' + 'LOGs' + 30*'=' 
    print logs
    print 30*'=' + 'MACs' + 30*'=' 
    for mac in macs:
            print mac

def life(hostname, port):
    print 'checking for pulse for ' + str(hostname) + ':' + str(port) + '. . .'
    keep_going = True
    bars = ['|','/','-','\\',]
    i = 0
    while keep_going:
        try:
            sock = socket.socket()
            sock.connect((hostname,port))
            print '\n[*] Alive!'
            keep_going = False
        except socket.error as e:
            sys.stdout.write("\r[%c] still dead. . . " %bars[i % len(bars)])
            sys.stdout.flush()
            #print str(e)
            sleep(0.5)
            i = i + 1
        finally:
            sock.close()

def main():
    startTime = datetime.now()
    life('10.0.0.138', 80)
    reboot()
    print 'waiting a while. . . '
    sleep(5)
    life('10.0.0.138', 80)
    life('www.google.com', 80)
    print 'execution time: ' + str(datetime.now()-startTime)
    try:
        input("Press Enter to continue...")
    except:
        exit()

if __name__ == "__main__":
    main()
