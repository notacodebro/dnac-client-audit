#!/usr/bin/python3

import requests
import json 
import argparse
import getpass
import base64
import urllib3


BASE_URL = 'https://sandboxdnac.cisco.com'
urllib3.disable_warnings()

def authentication(material):
    url = f'{BASE_URL}/dna/system/api/v1/auth/token'
    headers = {"Content-Type":"application/json", "Accept":"application/json", "Authorization":f"Basic {material}"}
    request = requests.post(url, headers=headers, verify=False)
    return request

def get_client(main_headers, mac=''):
    headers = main_headers
    if mac == '':
        url = f'{BASE_URL}/dna/intent/api/v1/client-health'
        meta = 'all'
    else:
        url = f'{BASE_URL}/dna/intent/api/v1/client-detail?macAddress={mac}'
        meta = 'mac'
    request = requests.get(url, headers=headers, verify=False)
    return request, meta

def parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', help='community string for snmp', required=True)
    parser.add_argument('--mac', help='community string for snmp', required=False)
    parser.add_argument('--interactive', help='community string for snmp', required=False)
    args = parser.parse_args()
    return args


def printer(request, meta):
    response = json.loads(request.text)
    print('*'*64)
    if meta == 'mac':
        print(json.dumps(json.loads(request.text), indent=3))
        print(f"Client hostname: {response['detail']['hostName']}") 
        print(f"Client IP: {response['detail']['hostIpV4']}") 
        print(f"Client connectivity: {response['detail']['hostType']}") 
        print(f"Client status: {response['detail']['connectionStatus']}") 
        print(f"Client switch connection: {response['detail']['connectedDevice'][0]['name']}") 
        print(f"Client switch port: {response['detail']['port']}\n") 
        print('*'*64)
        print('Client Health Score')
        print('*'*64)
        print(f"Client health score: {response['detail']['healthScore'][0]['score']}") 
    else: 
        print(json.dumps(json.loads(request.text), indent=3))
        print(f"Site: {response['response'][0]['siteId']}") 
        print(f"Total Clients: {response['response'][0]['scoreDetail'][0]['clientCount']}") 
        print('*'*64)
        print(f"Wired Clients: {response['response'][0]['scoreDetail'][1]['clientCount']}") 
        print(f"Good Clients: {response['response'][0]['scoreDetail'][1]['scoreList'][2]['clientCount']}") 
        print(f"Poor Clients: {response['response'][0]['scoreDetail'][1]['scoreList'][0]['clientCount']}") 
        

def main():
    args = parser()
    password = getpass.getpass() 
    material = base64.b64encode(f'{args.username}:{password}'.encode())
    material = material.decode()
    token = authentication(material)
    token = token.json()['Token']
    main_headers = {'X-Auth-Token': token, 'Content-Type': 'application/json'}
    if args.mac:
        request, meta = get_client(main_headers, args.mac)
    else:
       request, meta =  get_client(main_headers)
    
    printer(request, meta)
main()
