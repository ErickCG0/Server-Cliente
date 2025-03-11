import socket
import os
import time

HOST = "98:46:0A:9E:63:2A"
PORT = 5

DIRECTORIO = "archivos"
os.makedirs(DIRECTORIO, exist_ok=True)

def listar_archivos():
    archivos = os.listdir(DIRECTORIO)
    return "\n".join(archivos) if archivos else "No hay archivos disponibles."

def manejar_cliente(conn, addr):
    print(f"Conexion establecida con {addr}")
    while True:
        try:
            opcion = conn.recv(1024).decode()
            if not opcion:
                break

            if opcion == "1":  
                archivos = listar_archivos()
                conn.sendall(archivos.encode())

            elif opcion == "2":  
                archivo_nombre = conn.recv(1024).decode()
                ruta = os.path.join(DIRECTORIO, archivo_nombre)

                if os.path.exists(ruta):
                    conn.sendall(b"OK")
                    with open(ruta, "rb") as f:
                       file_size = os.path.getsize(ruta)
                       conn.sendall(str(file_size).encode())  
                       time.sleep(1)
                       conn.sendall(f.read())
                else:
                    conn.sendall(b"ERROR: Archivo no encontrado.")

            elif opcion == "3":  
                archivo_nombre = conn.recv(1024).decode()
                ruta = os.path.join(DIRECTORIO, archivo_nombre)
                conn.sendall(b"OK")
                
                with open(ruta, "wb") as f:
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                        f.write(data)
                print(f"Archivo recibido: {archivo_nombre}")

            elif opcion == "4":  
                print(f"Cliente {addr} desconectado.")
                break
            else:
                conn.sendall(b"Opcion no valida.")

        except ConnectionResetError:
            break

    conn.close()

def main():
    with socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM) as server:
        server.bind((HOST, PORT))
        server.listen()
        print(f"Servidor escuchando en {HOST}:{PORT}")

        while True:
            conn, addr = server.accept()
            manejar_cliente(conn, addr)

main()