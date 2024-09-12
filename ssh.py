import socket

def check_bsd_openssh_service(host):
    port = 22
    try:
        ip = socket.gethostbyname(host)
    except socket.gaierror:
        return f"{host} - can't resolve to IP"
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((ip, port))
        banner = sock.recv(1024).decode().strip()
        sock.close()
        return f"{host} ({ip}) - {banner}"
    except socket.timeout:
        return f"{host} ({ip}) - error: connection timeout"
    except socket.error as e:
        return f"{host} ({ip}) - error: {e}"

def main():
    file_path = "port22.txt"
    
    try:
        with open(file_path, 'r') as file:
            hosts = file.readlines()
        for host in hosts:
            host = host.strip()
            if host:
                result = check_bsd_openssh_service(host)
                print(result)
    except FileNotFoundError:
        print(f"File {file_path} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
