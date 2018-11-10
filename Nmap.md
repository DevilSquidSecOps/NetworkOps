# Nmap Commands
#### Quick enumeration scan of /24 network with output to grepable ASCII text format
nmap -oG network.txt -sS -F 10.10.40.0/24
#### OS detection with aggressive option using Syn TCP type scan for a target host
nmap -sS -O --osscan-guess 192.168.1.12/32
#### Service detection of possibly open UDP port
  nmap -sV -sU -p U:46878 10.10.10.92

## Advanced Commands
#### Feed ping scan results for Port 80 scan and OS discovery to new greppable file
cat ping.grep | awk '{print$2}' | grep -v Nmap | xargs nmap -oG 80-OS.grep -O --osscan-guess -T4 -p 80

# NSE Scripts
#### List available nse scripts run all scrips except the brute script ie;SNMP
  > find / -name snmp*.nse
  > nmap  --script "snmp-* and not snmp-brute*" -sU -v -p 161 10.10.10.92



## Filter Data
#### Grep for the discovered hosts
egrep -v "^#|Status: Up" $NMAP_FILE | cut -d' ' -f2
#### Grep for Discovered OS data from greppable file
grep "OS:" network.txt | sed 's/Host: //' | sed 's/Ports.\*OS://' | sed 's/Seq.\*$//' | sed 's/(//' | sed 's/)//'
