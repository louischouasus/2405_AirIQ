import ssh
import parse_airiq
import draw_chart

hostname = "192.168.50.1"
username = "admin"
password = "qwe123"

client = ssh.connect(hostname, username, password)
print(ssh.command(client, "date"))
