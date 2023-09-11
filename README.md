# dnac-client-audit
a quick script to audit a client in Catayst Center

# Usage   

```
./get_clients.py --help                                                    
usage: get_clients.py [-h] --username USERNAME [--mac MAC]
                      [--interactive INTERACTIVE]

optional arguments:
  -h, --help            show this help message and exit
  --username USERNAME   community string for snmp
  --mac MAC             community string for snmp
  --interactive INTERACTIVE
                        community string for snmp 

```

# Output

```
 python3 get_clients.py --username marc --mac 10:B3:D5:69:57:57                               
Password:
****************************************************************
Client hostname: SEP10B3D5695757
Client IP: 172.17.3.4
Client connectivity: WIRED
Client status: CONNECTED
Client switch connection: core-swa001.theblackcore.com
Client switch port: GigabitEthernet1/0/18

****************************************************************
Client Health Score
****************************************************************
Client health score: 10
