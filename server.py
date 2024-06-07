import socket

def request_nih(koneksi_klien):
    request = koneksi_klien.recv(1024).decode()
    print(request)
    
    request_line = request.splitlines()[0]
    filename = request_line.split()[1]
    
    if filename == '/':
        filename = '/index.html'
    filename = filename[1:]
    
    try:
        with open(filename, 'rb') as f:
            responbody = f.read()
        responheader = 'HTTP 200 OK\n\n'
        
    except FileNotFoundError:
        responheader = 'HTTP 404 ERROR CUY\n\n'
        responbody = b'404 ERROR'
        
    respon = responheader.encode() + responbody
    
    koneksi_klien.sendall(respon)
    koneksi_klien.close()
    
def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8003))
    server_socket.listen(5)
    
    print('server berjalan di port 8003')
    
    while True:
        koneksi_klien, alamat = server_socket.accept()
        request_nih(koneksi_klien)
        
main()