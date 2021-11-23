from enum import Enum


class DNSFlag(Enum):
    A = 1
    NS = 2


class DNSTableEntry:
    def __init__(self, hostname, ip, flag):
        if flag != DNSFlag.A and flag != DNSFlag.NS:
            raise Exception(
                "DNSTableEntry.__init__: flag must be a DNSFlag type.")

        self._hostname = hostname.lower()
        self._ip = ip
        self._flag = flag

    @property
    def hostname(self):
        return self._hostname

    @property
    def ip(self):
        return self._ip

    @property
    def flag(self):
        return self._flag

    def __str__(self):
        flag = ""
        if self._flag == DNSFlag.A:
            flag = 'A'
        elif self._flag == DNSFlag.NS:
            flag = 'NS'

        return "{} {} {}".format(self._hostname, self._ip, flag)


class DNSTable:
    def __init__(self):
        self._aRecords = []
        self._nsRecord = None

    def add(self, table_entry):
        if not isinstance(table_entry, DNSTableEntry):
            raise Exception(
                "DNSTable.add: table_entry must be an instance of DNSTableEntry"
            )

        if table_entry.flag == DNSFlag.NS:
            self._nsRecord = table_entry
        else:
            self._aRecords.append(table_entry)

    def lookup(self, hostname):
        if not isinstance(hostname, str):
            raise Exception("DNSTable.lookup: hostname must be a str type")

        # ignore case
        hostname = hostname.lower()

        matches = [x for x in self._aRecords if x.hostname == hostname]
        if len(matches) > 0:
            return matches[0]
        else:
            return self._nsRecord

    def debug_print(self):
        all_records = self._aRecords
        if self._nsRecord != None:
            all_records.append(self._nsRecord)
        for (index, entry) in enumerate(all_records):
            host = entry.hostname
            ip = entry.ip
            flag = entry.flag

            output = "[Rec {}]: Host: {}, IP: {}, Flag: {}".format(
                index, host, ip, flag)
            print(output)
