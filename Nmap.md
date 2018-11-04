# Nmap Commands
#### Quick enumeration scan of /24 network with output to grepable ASCII text format
nmap -oG network.txt -sS -F 10.10.40.0/24
#### OS detection with aggressive option using Syn TCP type scan for a target host
nmap -sS -O --osscan-guess 192.168.1.12/32
#### Port 80 scan and OS discovery to greppable file
cat ping.grep | awk '{print$2}' | grep -v Nmap | xargs nmap -oG 80-OS.grep -O --osscan-guess -T4 -p 80
## Filter Data
#### Grep for the discovered hosts
egrep -v "^#|Status: Up" $NMAP_FILE | cut -d' ' -f2
#### Grep for Discovered OS data from greppable file
grep "OS:" network.txt | sed 's/Host: //' | sed 's/Ports.\*OS://' | sed 's/Seq.\*$//' | sed 's/(//' | sed 's/)//'
