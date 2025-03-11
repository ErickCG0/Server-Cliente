import socket
import os

DIRECTORY = "shared_files"

if not os.path.exists(DIRECTORY):
    os.makedirs(DIRECTORY)

def list_files():
    """Devuelve una lista de archivos en el directorio compartido."""
    return "\n".join(os.listdir(DIRECTORY)) or "No hay archivos disponibles."

def handle_client(client_sock):
    """Maneja la comunicación con un cliente."""
    try:
        client_sock.send("Bienvenido al servidor Bluetooth\n".encode())
        
        while True:
            client_sock.send("\nOpciones:\n1. Listar archivos\n2. Descargar archivo\n3. Subir archivo\n4. Salir\nSeleccione una opción: ".encode())
            option = client_sock.recv(1024).decode().strip()

            if option == "1":
                client_sock.send(list_files().encode())
            elif option == "2":
                client_sock.send("Ingrese el nombre del archivo: ".encode())
                filename = client_sock.recv(1024).decode().strip()
                filepath = os.path.join(DIRECTORY, filename)

                if os.path.exists(filepath):
                    client_sock.send("EXISTS".encode())
                    with open(filepath, "rb") as f:
                        while chunk := f.read(1024):
                            client_sock.send(chunk)
                    client_sock.send(b"FINISHED")
                else:
                    client_sock.send("NOEXIST".encode())
            elif option == "3":
                client_sock.send("Ingrese el nombre del archivo a subir: ".encode())
                filename = client_sock.recv(1024).decode().strip()
                filepath = os.path.join(DIRECTORY, filename)

                client_sock.send("READY".encode())
                with open(filepath, "wb") as f:
                    while True:
                        data = client_sock.recv(1024)
                        if data == b"FINISHED":
                            break
                        f.write(data)

                client_sock.send("Archivo recibido correctamente.".encode())
            elif option == "4":
                client_sock.send("Saliendo...\n".encode())
                break
            else:
                client_sock.send("Opción no válida.".encode())

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_sock.close()

def start_server():
    """Inicia el servidor Bluetooth."""
    server_sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(("14:5A:FC:1E:8C:10", 5))  # Asegúrate de que este es el puerto correcto
    server_sock.listen(1)

    print("Servidor esperando conexiones en el puerto 5...")

    while True:
        client_sock, client_info = server_sock.accept()
        print(f"Conexión aceptada desde {client_info}")
        handle_client(client_sock)

if __name__ == "__main__":
    start_server()