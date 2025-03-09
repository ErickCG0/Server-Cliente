import socket

HOST = "127.0.0.1"
PORT = 65535  

def menu():
    print("\n1. Lista de archivos")
    print("2. Descargar archivo")
    print("3. Subir archivo")
    print("4. Salir")

while True:
    menu()
    opcion = input("Selecciona una opcion: ")

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    client_socket.send(opcion.encode()) 

    if opcion == "1":
        lista = client_socket.recv(1024).decode()
        print("\nArchivos disponibles:")
        print(lista)

    elif opcion == "2":
        nombre_archivo = input("Ingrese el nombre del archivo a descargar: ")
        client_socket.send(nombre_archivo.encode())

        datos = client_socket.recv(1024)
        if b"ERROR" in datos:
            print("\nArchivo no encontrado en el servidor.")
        else:
            with open(nombre_archivo, "wb") as f:
                f.write(datos)
            print("\nArchivo descargado correctamente.")

    elif opcion == "3":
        nombre_archivo = input("Ingrese el nombre del archivo a subir: ")

        try:
            with open(nombre_archivo, "rb") as f:
                contenido = f.read()
            client_socket.send(nombre_archivo.encode())  
            client_socket.send(contenido) 
            mensaje = client_socket.recv(1024).decode()
            print("\n", mensaje)
        except FileNotFoundError:
            print("\nEl archivo no existe. ")

    elif opcion == "4":
        print("\nCerrando conexion.")
        client_socket.close()
        break

    client_socket.close()

