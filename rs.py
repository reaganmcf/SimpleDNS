import socket
from sys import argv as Arguments
from dns_table import DNSTable, DNSTableEntry, DNSFlag

def start_rs(table, port):
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        print('[RS]: Failed to open socket: {}\n'.format(err))
        exit()
        
    ss.bind(('', port))
    ss.listen(1)
    host = socket.gethostname()
    print('[RS]: RS is alive at {}:{}\n'.format(host, port))
    
    while True:
        csockid, addr = ss.accept()

        raw_data = csockid.recv(256)

        # if there is a \n at the end of the data,
        # then trim it
        data = str(raw_data.decode('utf-8', 'ignore')).strip()
        if len(data) > 0 and data[-1] == '\n':
            data = data[:-1]

        print('[RS]: RS received the following message:')
        print("\t'{}'".format(data))

        record = table.lookup(data)
        if record.flag == DNSFlag.A:
            print('[RS]: Found record.')
        else:
            print('[RS]: No record found. Sending back NS record for TS')

        msg = str(record)
        
        print('[RS]: Sending back the following message:')
        print("\t'{}'\n".format(msg))
        
        csockid.send(msg.encode('utf-8'))


    print('[RS]: Closing... ')
    ss.close()
    print('[RS]: Done.')
    exit()
    
if __name__ == '__main__':
    if len(Arguments) != 2:
        print("Expected arguments following the format: \n\n python rs.py rsListenPort\n\nPlease try again")
        exit()
    
    rawPort = Arguments[1]
    try:
        port = int(rawPort)
    except:
        print("Port argument must be an integer. Please try again")
        exit()

    # create a DNS table
    table = DNSTable()

    # load RS dns table entries into table
    with open("PROJI-DNSRS.txt") as file:
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
    start_rs(table, port)
