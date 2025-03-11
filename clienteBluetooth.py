import socket
import os

HOST_MAC = "98:46:0A:9E:63:2A"
PORT = 5  # Debe coincidir con el puerto del servidor
# CV Address: 98:46:0a:9e:63:2a

def menu():
    print("\n1. Lista de archivos")
    print("2. Descargar archivo")
    print("3. Subir archivo")
    print("4. Salir")

while True:
    menu()
    opcion = input("Selecciona una opcion: ")

    client_socket = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    client_socket.connect((HOST_MAC, PORT))
    client_socket.send(opcion.encode()) 

    if opcion == "1":  
        lista = client_socket.recv(1024).decode()
        print("\nArchivos disponibles:")
        print(lista)

    elif opcion == "2":  
        nombre_archivo = input("Ingrese el nombre del archivo a descargar: ")
        client_socket.send(nombre_archivo.encode())

        respuesta = client_socket.recv(1024)
        if respuesta == b"OK":
            file_size = int(client_socket.recv(1024).decode())  
            received_size = 0
            with open(nombre_archivo, "wb") as f:
                while received_size < file_size:
                    datos = client_socket.recv(1024)
                    if not datos:
                        break
                    f.write(datos)
                    received_size += len(datos)
            print("\nArchivo descargado correctamente.")

            if nombre_archivo.endswith(".txt"):  
                with open(nombre_archivo, "r", encoding="utf-8") as f:
                    print("\nContenido del archivo:")
                    print(f.read())
        else:
            print("\nArchivo no encontrado en el servidor.")

    elif opcion == "3":  # Subir archivo
        nombre_archivo = input("Ingrese el nombre del archivo a subir: ")
        try:
            with open(nombre_archivo, "rb") as f:
                contenido = f.read()
            client_socket.send(nombre_archivo.encode())  
            confirmacion = client_socket.recv(1024)
            if confirmacion == b"OK":
                client_socket.send(contenido) 
                print("\nArchivo subido correctamente.")
            else:
                print("\nError en la subida del archivo.")
        except FileNotFoundError:
            print("\nEl archivo no existe.")

    elif opcion == "4":  
        print("\nCerrando conexion.")
        client_socket.close()
        break

    client_socket.close()