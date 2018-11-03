#OvpnSwitch script that will change your vpn connection and cycle through the "US" .ovpn conns provided by PIA VPN provider
#Two required parameters: your sudo password and path to the ovpn files that should be in one directory
#Additional files: your last_connection.txt file and your login.txt file that contains your username and password for the vpn provider

import sh
import os
import fnmatch
import re
import time 
import sys


code = sys.argv[1] #enter sudo password
openvpn_path = sys.argv[2] #enter path containing your PIA .ovpn files, last_connection.txt, login.txt. Do not end the path with a '/'

passcode = f"{code}\n" #newline character is needed at end

# -S says "get the password from stdin"
my_sudo = sh.sudo.bake("-S", _in=passcode)

#FUNCTION TO RETURN A LIST OF FILENAMES MATCHED BY MY REGEX QUERY
def get_files(reg,files):
    US_nodes = []
    for item in files:
        c = reg.findall(item)#method 2(returns a list per item regardless of what's found)
        if c!= []:#remove all empty values returned since some of the items don't have the match it still returns the list empty per item
    #         print(c[0])#print only the the values and remove the list portion
            US_nodes.append(c[0]) #append only the value of each list that was made per item
    print ("List returned as 'US_nodes' contains %s items" % (len(US_nodes)))
    return US_nodes 
#USING THE FUNCTION 'get_files'
regex_num = re.compile('US.*\.ovpn') #The regex pattern to match for, we only want US ovpn nodes
opnvpn_files = my_sudo.ls(openvpn_path) #using the sh module and 'ls' command get the list of files to search through

#feed the parameters into the function and set a variable to capture the values of the produced list
US_nodes = get_files(regex_num,opnvpn_files) 

#Verify List contains your desired values
for item in US_nodes:
    print(item)
#Kill the current connection using sudo
try:
    my_sudo.killall('openvpn')
except Exception as e:
    print(e)
    pass
time.sleep(3)
#verify your off vpn by checking your IP
a = sh.wget('http://ipinfo.io/ip' ,'-qO','-')
print("Current IP:",a) 

#this function requires the path to a text files containing one of the nodes and another list of the nodes we created earlier $
def get_next_conn(path,nodes):
    last_conn_list = [] #list to capture our log text file 
    with open(path,'r') as file: #this loop should append each line in our file to the list like saying file = open('log.txt','r') this operation wil$
        for line in file:
            last_conn_list.append(line.strip())       
    print('List made from file:',last_conn_list) #verify list looks good
    #if conn in last_conn_list exists in US_ovpn list print the next connection on the US_ovpn list
    a = set(last_conn_list) & set(US_nodes) #grabs the matching compared node
    print('match for %s was made between our two lists'%(a))
    b = next(iter(a)) #strips the string from the dictionary that gets made
    print('Last Connection was:',b)
    c = nodes.index(b) #finds where in the list of nodes the last connection sat in 
    if b == US_nodes[-1]: #if we hit the last item on our list we will need to start over with a -1+1
        c = -1
    else:
        pass
    next_conn = nodes[c+1]  #Get the next item in the list relative to our last conn item 
    print('Next Connection is:',next_conn)   
    last_connect = open(path,'w') #open the log file for writing
    last_connect.write("%s" % (next_conn)) #write the new connection to the file for later reference
    last_connect.close()
    return next_conn #remember to set a variable when calling the function to capture this value

last_conn_log = f'{openvpn_path}/last_connection.txt'
next_conn = get_next_conn(last_conn_log,US_nodes)
print(next_conn) #Connect to a PIA VPN node

#For Jupyter Cells this will stay on and you can exit the cell with stop but your pia connection will continue until the killall is run on the process

sh.cd(openvpn_path) #need to be in the directory first

#encap your command in a variable so the background parameter(bg) runs as well otherwise it will hang
run = my_sudo.openvpn('--config',f'{openvpn_path}/{next_conn}', '--auth-user-pass', f'{openvpn_path}/login.txt', _bg=True)

sh.cd(openvpn_path)
time.sleep(10) #shouldn't take longer than 10 seconds to make the new connection
new_ip = sh.wget('http://ipinfo.io/ip' ,'-qO','-')
if a != new_ip:
    print("new connection made:", new_ip)
else:
    print("connection not made:", a)
