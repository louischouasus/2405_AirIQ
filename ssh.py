import paramiko
import time
from base64 import decodebytes


keydata = b"AAAAB3NzaC1yc2EAAAADAQABAAABAQCz3A0ADNCi0NEBNnMXEEdU3V3ENCrspmVUWUdak3ROJ5a12Y933GLLKLTALsFcnsuXn6JxjofYLpZFikmeLL8PoLNxXOaGSC42ah5I16edqn1gYVBwE+oGgOiSj//OcjGFHVZ7scTbptSdhrUpi94KOILBng/qG5r2I4+IN1zR8VCFvGJt21tXJwQkiJa73q/WmUZF9hoaL++AEp794X3nwxsr5cCT0S+PgclfkAErmLWyXOHmAbsmuvUlK/xhDfQZzLVmgthwViVZLm+1UrzdEatQlDZsfvjDl+J6P2rfedBKyCFr9XJ8lu0bUMloo6P0GMh0dlMvvbW+quTsLtZX"
key = paramiko.RSAKey(data=decodebytes(keydata))


def connect(hostname: str, username: str, password: str) -> paramiko.SSHClient:
    client = paramiko.SSHClient()
    client.get_host_keys().add(hostname, "ssh-rsa", key)
    client.connect(hostname=hostname, username=username, password=password, timeout=60)
    return client


def command(client: paramiko.SSHClient, cmd: str):
    stdin, stdout, stderr = client.exec_command(cmd)
    for line in iter(lambda: stdout.readline(2048), ""):
        print(line)


def close(client: paramiko.SSHClient):
    client.close()
