import socket
import re
import os

class http_server():
    def __init__(self):
        self.serv = socket.socket()
        self.serv.bind(('', 80))
        self.serv.listen()

    def get_file_content(self, d_path, filename):
        file_path = os.path.join(d_path, filename)
        with open(file_path, 'rb') as f:
            print('file found')
            file_content = f.read()
            return file_content
    
    def send_file(self, d_path, filename, client, header_content_type):
        if filename == 'page1.html': # moved -> redirection (302)
            new_location = '/page2.html'
            res_header = (
                "HTTP/1.1 302 Moved Temporarily\r\n"
                "Location: {}\r\n" # location of redirect file
                "Content-Type: text/html; charset=utf-8\r\n"
                "Content-Length: 0\r\n"
                "\r\n".format(new_location)
            )
            client.sendall(res_header.encode())
        elif filename == 'cantgohere.html': # forbidden -> no access (403)
            res_header = 'HTTP/1.1 403 Forbidden\r\n'
            print(res_header)
            client.sendall(res_header.encode())
        else:
            file_content = self.get_file_content(d_path, filename)
            res_header = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: {}\r\n"
                "Content-Length: {}\r\n"
                "\r\n".format(header_content_type[filename[filename.rfind('.')+1:]], len(file_content)) # rfind to find index of last accurance
            ) # line-breaks are for better readability
            client.sendall(res_header.encode())
            print(res_header)
            client.sendall(file_content) # שליחת כל הקובץ ללא חלוקה

    def start(self):
        header_content_type = {
            'html':"text/html; charset=utf-8",
            'txt':"text/html; charset=utf-8",
            'jpg':"image/jpeg",
            'ico':"image/x-icon",
            'js':"text/javascript; charset=UTF-8",
            'css':"text/css"
        }
        while True:
            client, addr = self.serv.accept()
            print('new connection established')
            req = client.recv(1024).decode()
            match = re.match(r'GET /(.*) HTTP/1.1\r\n', req) # (.*) is a regular expression (can be any length) that holds the name of the requested file

            if match:
                print('GET HTTP request received')
                filename = match.group(1)
                if filename == '': filename = 'index.html' # when not asking for a file, will direct to index.html (default)
                d_path = "C:/Users/user2/Documents/VSCode/Software Engineering/11th grade/cyber/HTTP exercise/root dictionary"
                print('requested file name:', filename)
                
                # Use os.path.join to create the full path to the file
                file_path = os.path.join(d_path, filename)
                
                if os.path.isfile(file_path): # if file exists in this path
                    self.send_file(d_path, filename, client, header_content_type)
                else:
                    print('file not found')
                    res_header = "HTTP/1.1 404 Not Found\r\n"
                    client.sendall(res_header.encode())
                client.close()
            else:  # if didn't understand request
                print('invalid request')
                res_header = (
                    "HTTP/1.1 500 Internal Server Error\r\n"
                )
                client.sendall(res_header.encode())
                client.close()


if __name__ == '__main__':
    serv = http_server() # hello
    serv.start()