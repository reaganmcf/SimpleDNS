# SimpleDNS

> A simplified DNS system consisting of a client program and two server programs: RS (a simplified root DNS server) and TS (a simplified top-level DNS server)

## Usage
1. Start the TS server
```bash
$ python2.7 ts.py tsListenPort
```

2. Start the RS server
```bash
$ python2.7 rs.py rsListenPort tsHostname
```

3. Start the client
```bash
$ python2.7 client.py rsHostname rsListenPort tsListenPort
```

## Writeup

###### 0. Please write down the full names and netids of both your team members
Reagan McFarland - rpm141

###### 1. Briefly discuss how you implemented your recursive client functionality
The way I implemented the recursive client functionality is by storing the lookup logic in a function `def lookup(dns_hostname, dns_port, hostname)` in `client.py`.
The main dispatch inside client calls this function with the `rsHostname` and `rsListenPort` on its first call.
If the RS DNS server returns a `NS` record back, then we parse out the hostname as of the TS DNS server, and call `return lookup(res_hostname, TS_LISTEN_PORT, hostname)`.
This will recursively call the function again, but making the request to the TS DNS server instead of the RS DNS server.

###### 2. Are there known issues or functions that aren't working currently in your attached code? If so, explain.

There are no known issues or functions that aren't working currently in the code base. I have tested all the code across multiple machines and received the exact same results.

###### 3. What problems did you face developing code for this project?
I faced some problems with python2.7, instead of using python3. Although most of the issues were just syntax based so no real blockers.

###### 4. What did you learn by working on this project?
I learned a lot about socket programming with python, as well as command line argument parsing with python. I have somehow made it this far
without really doing CLAP with python somehow, so it was nice to learn more about it.
