# Nmap Commands
#### Quick enumeration scan of /24 network with output to grepable ASCII text format
nmap -oG network -sS -F 10.10.40.0/24
#### OS detection with aggressive option using Syn TCP type scan
nmap -sS -O --osscan-guess 192.168.1.12/32 
