import socket
import os

SERVER_MAC = "14:5A:FC:1E:8C:10"
PORT = 5  # Debe coincidir con el puerto del servidor

def send_data(sock, message):
    """Envía un mensaje codificado al servidor."""
    sock.send(message.encode())

def receive_data(sock):
    """Recibe datos del servidor y los decodifica."""
    return sock.recv(1024).decode().strip()

def client_program():
    """Programa principal del cliente Bluetooth."""
    try:
        print(f"Conectando a {SERVER_MAC} en el puerto {PORT}...")
        client_sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        client_sock.connect((SERVER_MAC, PORT))
        print(receive_data(client_sock))  # Mensaje de bienvenida

        while True:
            print(receive_data(client_sock))  # Menú de opciones
            option = input("Ingrese opción: ")
            send_data(client_sock, option)

            if option == "1":
                print(receive_data(client_sock))  # Lista de archivos
            elif option == "2":
                filename = input("Ingrese el nombre del archivo a descargar: ")
                send_data(client_sock, filename)
                
                # Asegurarnos de recibir correctamente la respuesta del servidor
                response = receive_data(client_sock)
                
                with open(filename, "wb") as f:
                    while True:
                        data = client_sock.recv(1024)
                        if data == b"FINISHED":
                            break
                        f.write(data)
                print("Archivo descargado con éxito.")
            elif option == "3":
                filename = input("Ingrese el nombre del archivo a subir: ")
                try:
                    with open(filename, "rb") as f:
                        send_data(client_sock, filename)
                        receive_data(client_sock)  # READY

                        while chunk := f.read(1024):
                            client_sock.send(chunk)
                        client_sock.send(b"FINISHED")

                        print(receive_data(client_sock))  # Confirmación del servidor
                except FileNotFoundError:
                    print("Archivo no encontrado.")
            elif option == "4":
                print("Saliendo...")
                break
            else:
                print("Opción no válida.")
    except Exception as e:
        print(f"Error de conexión: {e}")
    finally:
        client_sock.close()

if __name__ == "__main__":
    client_program()
