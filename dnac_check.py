#!/usr/bin/python3

import requests
import json 
import argparse
import getpass
import base64
import urllib3
import pandas as pd
from tabulate import tabulate

BASE_URL = 'https://localhost:9443'
#BASE_URL = 'https://sandboxdnac.cisco.com'
POPPED_TAGS = ['scoreList', 'starttime', 'endtime', 'maintenanceAffectedClientCount', 'duidCount', 'randomMacCount']
urllib3.disable_warnings()

def authentication(material):
    _url = f'{BASE_URL}/dna/system/api/v1/auth/token'
    _headers = {"Content-Type":"application/json", "Accept":"application/json", "Authorization":f"Basic {material}"}
    response = requests.post(_url, headers=_headers, verify=False)
    print(response)
    return response

def get_clients(token_header):
    _url = f'{BASE_URL}/dna/intent/api/v1/client-health' 
    response = requests.get(_url, headers=token_header, verify=False)
    return json.loads(response.text)

def get_client_health(token_header, host_macs): 
    print('Please wait.....')
    for mac in host_macs:
        _url = f'{BASE_URL}/dna/intent/api/v1/client-detail?macAddress={mac}'
        response = requests.get(_url, headers=token_header, verify=False)
        response = json.loads(response.text)
        if response['detail']['healthScore'][0]['score'] <=7:
            _pdresult = pd.json_normalize(response['detail']['healthScore'])
            print(f'\n\nClient Mac Address: {mac}')
            print(tabulate(_pdresult, headers='keys', tablefmt='heavy_grid'))
        else:
            print('.', end = " ", flush=True)
            pass 
    print('\nNo other clients with poor or fair scores')
            
def get_hosts(token_header):
    meta = 'host'
    host_macs = []
    _url = f'{BASE_URL}/api/v1/host'
    response = requests.get(_url, headers=token_header, verify=False)
    for items in json.loads(response.text)['response']:
        host_macs.append(items['hostMac'])
    return host_macs, meta

def parser():
    _parser = argparse.ArgumentParser()
    _parser.add_argument('--username', help='username for access', required=True)
    _parser.add_argument('--mac', help='Specific mac address to search for', required=False)
    _parser.add_argument('--interactive', help='Future Interactive mode', required=False)
    args = _parser.parse_args()
    return args

def printer(results, meta):
    _popped_tags = ['scoreList', 'starttime', 'endtime', 'maintenanceAffectedClientCount', 'duidCount', 'randomMacCount']
    _results = results['response'][0]['scoreDetail']
    _pdresult = pd.json_normalize(_results[0])
    _pdresult_specific = pd.json_normalize(_results[1]['scoreList']) 
    for items in _popped_tags:
        try:
            _pdresult_specific.pop(items)
            _pdresult.pop(items)
        except KeyError:
            pass
    print()
    print('\nGlobal Client Health Results')
    print('*'*64)
    print(tabulate(_pdresult, headers='keys', tablefmt='heavy_grid'))
    print('\nSpecific Health Results')
    print('*'*64)
    print(tabulate(_pdresult_specific, headers='keys', tablefmt='heavy_grid'))
    return

def main():
    print('*'*64)
    print('Welcome to the Catalyst Center Client Health Check Tool')
    print('*'*64)
    args = parser()
    _password = getpass.getpass() 
    material = base64.b64encode(f'{args.username}:{_password}'.encode())
    material = material.decode()
    token = authentication(material)
    token = token.json()['Token']
    token_header = {'X-Auth-Token': token, 'Content-Type': 'application/json'}
    host_macs, meta = get_hosts(token_header)
    if args.mac:
        host_macs = []
        host_macs.append(args.mac)
        get_client_health(token_header, host_macs)
    else:
        print('Please wait....')
        results =  get_clients(token_header)
        printer(results, meta)
        ans = input('Please press any key to print client details with Poor/Fair health...\n\n')
        get_client_health(token_header, host_macs)


if __name__ == '__main__': 
    main()
