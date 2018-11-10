# Nmap Commands
#### Quick enumeration scan of /24 network with output to grepable ASCII text format
nmap -oG network.grep -sS -F 10.90.23.0/24
#### OS detection with aggressive option using Syn TCP type scan for a target host
nmap -sS -O --osscan-guess 192.168.1.12/32
#### Service detection of given UDP/TCP ports with highest version intensity probing
  nmap -sV --version-intensity 9 -sU -sS -p U:35536,53,161,T:3306,53 10.10.11.89

## Advanced Commands
#### Feed ping scan results for Port 80 scan and OS discovery to new greppable file
cat ping.grep | awk '{print$2}' | grep -v Nmap | xargs nmap -oG 80-OS.grep -O --osscan-guess -T4 -p 80

# NSE Scripts
#### List available nse scripts ie;SNMP
find / -name snmp*.nse
#### run all scrips except the brute script ie;SNMP
nmap  --script "snmp-* and not snmp-brute*" -sU -v -p 161 10.10.44.2



## Filter Data
#### set var for greppable nmap output
NMAP_FILE=network.grep
#### Grep for the discovered hosts
egrep -v "^#|Status: Up" $NMAP_FILE | cut -d' ' -f2
#### Grep for Discovered OS data from greppable file
grep "OS:" network.txt | sed 's/Host: //' | sed 's/Ports.\*OS://' | sed 's/Seq.\*$//' | sed 's/(//' | sed 's/)//'
