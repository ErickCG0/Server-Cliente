# -*- coding: utf-8 -*-
import socket
import os

HOST = "0.0.0.0" 
PORT = 65535       

def listar_archivos():
    archivos = os.listdir("archivos") 
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
                conn.sendall(b"")
                archivo_nombre = conn.recv(1024).decode()
                
                ruta = os.path.join("archivos", archivo_nombre)
                if os.path.exists(ruta):
                    conn.sendall(b"OK")
                    with open(ruta, "rb") as f:
                        conn.sendfile(f)
                else:
                    conn.sendall(b"ERROR: Archivo no encontrado.")

            elif opcion == "3": 
                conn.sendall(b"Ingrese el nombre del archivo:")
                archivo_nombre = conn.recv(1024).decode()
                
                conn.sendall(b"OK")
                ruta = os.path.join("archivos", archivo_nombre)
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
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen()
        print(f"Servidor escuchando en {HOST}:{PORT}")

        while True:
            conn, addr = server.accept()
            manejar_cliente(conn, addr)

main()

