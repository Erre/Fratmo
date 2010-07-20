import socket
from time import sleep
from random import randint

def control():

	return "!roulette"


def main(list):

	list.append((list[2].split("!roulette ")[1])[:-2])

	
	list[0].send("PRIVMSG %s :Ciao %s, ora estrarro' un numero a caso, se il numero sara' maggiore di 50 ti kickero', altrimenti rimarrai nel chan\r\n" % (list[1],list[3]))
	list[0].send("PRIVMSG %s :Estrazione numero in corso...\r\n" % (list[1]))

	a = randint(1, 100)
	sleep(2)

	list[0].send("PRIVMSG %s :Numero estratto: %d\r\n" % (list[1], a))

	if a < 50:
        	list[0].send("PRIVMSG %s :Ok, sei fortunato, non ti kicko.\r\n" % (list[1]))
        elif a == 50:
        	list[0].send("PRIVMSG %s :50, CHE CULO ROTTO!\r\n" % (list[1]))
        else:
       		list[0].send("KICK %s %s :Non sei fortunato al gioco, fanculo :D\r\n" % (list[1], list[3]))
