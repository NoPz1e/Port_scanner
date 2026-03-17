from concurrent.futures import ThreadPoolExecutor
import functools
import argparse , socket

#-------------------------------------- Port input treatment -----------------------------------------------------------
#----- Checks if port values ​​are valid ------
def isvalidPort(ports):
   
    if type(ports) == str:
        if 1 <= int(ports) <= 65535:
            return
        else:
            print(f'The port {ports} is not a valid port!!')
            exit()
    
    
    else:
        for i in ports:
            if 1 <= int(i) <= 65535:
                pass
            else:
                print(f'The port {i} is not a valid port!!')
                exit()
    
    
        return

#----- Treat the input of port and return only a list
def treat_ports(ports):

    # remove spaces
    ports = ports.replace(' ', '')
   
    l_port = []
    
    #Verifica if is only digits
    if ports.isdigit():
        
        #verifica se a porta é valdida
        isvalidPort(ports)
        l_port.append(int(ports))
        return l_port

    # verify if is a range of ports
    elif '-' in ports:
           
        start_end = ports.split('-')
        
        if len(start_end) != 2:
            print('Input of ports invalid!!')
            exit()
            
        # Verificar se as portas são validas
        isvalidPort(start_end)
        
        if int(start_end[0]) < int(start_end[1]):
            
            l_port.extend(range(int(start_end[0]), int(start_end[1])+1))
                    
            # returna a lista com 2 valores
            return l_port
        else:
            print('Input of ports invalid!!')
            exit()
    
    
    # verify if is a list of ports     
    elif ',' in ports:
        
        l_port = ports.split(',')
        
        isvalidPort(l_port)
        
        l_port = list(map(int, l_port))
        return l_port
        

#------------------------------------ Scan all port from the list in one host ---------------------------------------
def scan_port(port, host):

    try:
        tcp_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_s.settimeout(3)
        tcp_s.connect((host, port))
    
        tcp_s.close()
        return True
    except ConnectionRefusedError:
        return False
    
    except TimeoutError:
        return
    
    except Exception as error:
          print(error)   
        
        
# -------- Treat the arguments from comand line ---------
parser = argparse.ArgumentParser()

parser.add_argument('-t', '--target', help='Target ip or domanin to scan', required=True)
parser.add_argument('-p', '--port', help='Port o scan. Ex: (443,80) or (1-100)', default='443, 80, 53, 22, 25, 8080, 445, 143, 3389, 21')
parser.add_argument('-th', '--thread',type=int, help='Number of used thread', default=30)


args = parser.parse_args()

# ---- Call a function to treat the ports and arrange in ascending order -----
list_port = treat_ports(args.port)
list_port.sort()

print(f'Scannig {args.target} ..........')

# ------ Pre-fill the function scan_port with a host, for can use thread -------
scan_port_partial = functools.partial(scan_port, host=args.target)

# ------ Create a number of thread of argument specifies -------
with ThreadPoolExecutor(max_workers=args.thread) as executor:
    # ------- Call da function to scan the ports and save all results in one list ---------
    results = list(executor.map(scan_port_partial,list_port))
    
# ------------ Show on screen the results without the falses ---------- 
for port, result in zip(list_port, results):
    if result:
        print(f'-> {port} OPEN')
    elif result == None:
        print(f'-> {port} FILTERED')
