import socket
from sys import argv as Arguments
from dns_table import DNSTable, DNSTableEntry, DNSFlag

def start_ts(table, port):
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        print('[TS]: Failed to open socket: {}\n'.format(err))
        exit()
        
    ss.bind(('', port))
    ss.listen(1)
    host = socket.gethostname()
    print('[TS]: TS is alive at {}:{}'.format(host, port))
    
    while True:
        csockid, addr = ss.accept()

        raw_data = csockid.recv(256)

        # if there is a \n at the end of the data,
        # then trim it
        data = str(raw_data.decode('utf-8')).strip()
        if data[-1] == '\n':
            data = data[:-1]

        print('[TS]: TS received the following message:')
        print("\t\'{}\'".format(data))

        record = table.lookup(data)
        msg = ""
        if record is None: 
            print('[TS]: No record found.')
            msg = "{} - Error:HOST NOT FOUND".format(hostname)
        else:
            print('[TS]: Found record.')
            msg = str(record)

        print('[TS] Sending back the following message:')
        print("\t'{}'".format(msg))

        csockid.send(msg.encode('utf-8'))

    print('[TS]: Closing... ')
    ss.close()
    print('Done.')
    exit()
    
if __name__ == '__main__':
    if len(Arguments) != 2:
        print("Expected arguments following the format: \n\n python ts.py tsListenPort\n\nPlease try again")
        exit()
    
    rawPort = Arguments[1]
    try:
        port = int(rawPort)
    except:
        print("Port argument must be an integer. Please try again")
        exit()

    # create a DNS table
    table = DNSTable()

    # load TS dns table entries into table
    with open("PROJI-DNSTS.txt") as file:
        lines = file.readlines()
        for line in lines:
            # remove \r\n from the end of each line
            line = line[:-2]
            [hostname, ip, raw_flag] = line.split(' ')

            flag = None
            if raw_flag == 'A':
                flag = DNSFlag.A
            elif raw_flag == 'NS':
                flag = DNSFlag.NS
            else:
                raise Exception("Cannot parse {} as a DNSFlag".format(raw_flag))

            entry = DNSTableEntry(hostname, ip, flag)
            table.add(entry)

    table.debug_print()
    # start server
    start_ts(table, port)
