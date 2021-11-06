from sys import argv as Arguments
from dns_table import DNSFlag
import socket
import time

RS_HOSTNAME = ""
RS_LISTEN_PORT = -1
TS_LISTEN_PORT = -1

def lookup(dns_hostname, dns_port, hostname):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        print('[Client]: Failed to open socket: {}\n'.format(err))
        exit()

    sock.connect((dns_hostname, dns_port))
    sock.send(hostname.encode('utf-8'))

    raw_response = sock.recv(200)
    response = str(raw_response.decode('utf-8', 'ignore')).strip()
    print("[Client]: Received response:")
    print("\t'{}'".format(response))


    # check if error from TS
    if 'Error:HOST NOT FOUND' in response:
        print(response)
    else:
        [res_hostname, res_ip, flag_or_error] = response.split(' ')
        if flag_or_error == 'A':
            print(response)
        elif flag_or_error == 'NS':
            lookup(res_hostname, TS_LISTEN_PORT, hostname)
        else:
            raise Exception("Unsupported DNSFlag with value {}".format(raw_flag))
    
    sock.close()

if __name__ == "__main__":
    if len(Arguments) != 4:
        print("Expected arguments following the format: \n\n python client.py rsHostname rsListenPort tsListenPort\n\nPlease try again")
        exit()

    RS_HOSTNAME = Arguments[1]

    try:
        RS_LISTEN_PORT = int(Arguments[2])
        TS_LISTEN_PORT = int(Arguments[3])
    except:
        print("Port arguments must be integers. Please try again")
        exit()

    with open("PROJI-HNS.txt") as file:
        lines = file.readlines()
        for line in lines:
            # remove \r\n from the end of each line
            hostname = line[:-2]
            print(hostname)
            
            lookup(RS_HOSTNAME, RS_LISTEN_PORT, hostname)
            time.sleep(1)
