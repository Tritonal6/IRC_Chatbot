#!/usr/bin/python3
import socket

ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = "chat.freenode.net" # Server
channel = "##bot-testing" # IRC Channel
botnick = "TestTubeBaby" # Bot nickname
adminname = "Sidewinder6" # Our admin name
exitcode = "terminate " + botnick # Get rid of the specific bot

ircsock.connect((server, 6667)) # Connect to server using specified port 6667
ircsock.send(bytes("USER "+ botnick +" "+ botnick +" "+ botnick + " "+ botnick + "\n", "UTF-8"))
ircsock.send(bytes("NICK "+ botnick +"\n", "UTF-8")) # Assign the nickname to the bot
# This just created a form with fields filled with the botname

#BOT FUNCTIONS
def joinchan(chan): # join channel(s)
	ircsock.send(bytes("JOIN "+ chan +"\n", "UTF-8")) # Send a bytestring with JOIN - channel - newline.
	ircmsg = ""	#Empty string as a placeholder.
	while ircmsg.find("End of /NAMES list.") == -1:
		ircmsg = ircsock.recv(2048).decode("UTF-8") # Receive IRC message and decode bytestring using UTF-8
		ircmsg = ircmsg.strip('\n\r') # Strip the irc message of newlines
		print(ircmsg) # Print the IRC message.

def ping(): # respond to server pings
	ircsock.send(bytes("Pong :pingis\n", "UTF-8")) # Respond pong to the server ping to show we're still alive.

"""
 By now, all of our major preparations are complete. We can now write a few functions that way our
		bot actually has something to do
"""

def sendmsg(msg, target=channel): 	# Sends a message to the target
	ircsock.send.send(bytes("PRIVMSG "+ target +" :"+ msg +"\n", "UTF-8"))
"""
	Time to create the continuous function of the bot - this is the main function. THis calls the other
	funcs as necessary, and processes the information received from IRC
"""
def main(): # Things are about to get long. Really, REALLY long.
	joinchan(channel)
	while 1:  # This is where we take the information sent to us from the IRC server.
		ircmsg = ircsock.recv(2048).decode("UTF-8") #Rcv bytestring and decode using UTF-8
		ircmsg = ircmsg.strip('\n\r') #Strip new lines out of the IRC message.
		print(ircmsg) # Prints the cleaned IRC message.

		if ircmsg.find("PRIVMSG") != -1:
# We want to get the nick of the person who sent the message.
			name = ircmsg.split('!',1)[0][1:]
			message = ircmsg.split('PRIVMSG',1)[1].split(':',1)[1]
# Check if the name is less than 17 characters. Make sure we're not talking to ghosts
			if len(name) < 17:
				if message.find('Hi ' + botnick) != -1:
					sendmsg("Hello " + name + "!")
#Here's an example of how you can look for a 'code' at the beginning of a message and parse it to do a specific task.
				if message[:5].find('.tell') != -1:
					target = message.split(' ', 1)[1]
				if target.find(' ') != -1:
					message = target.split(' ', 1)[1]
					target = target.split(' ')[0]
				else:
					target = name
					message = "Could not parse. The message should be in the format of '.tell [target] [message]' to work properly."
					sendmsg(message, target)
# Yay for infinity loop functions and stuff. Time to create the omega to the alpha
# We'll check for some text and use that to end the loop. We'll end the script on the call to main()
		if name.lower() == adminname.lower() and message.rstrip() == exitcode:
			sendmsg("oh...okay. :'(")
			ircsock.send(bytes("Quit \n", "UTF-8"))
			return
		else:
# Respond to them pings.
#If the message ISN'T a PRIVMSG, it still may need some type of response. If the info we received was a PING
##request - we'd call the ping() function that we defined earlier to respond with a PONG. This is a way of letting
###the server know that we're still online and connected.
			if ircmsg.find("PING :") != -1:
				ping()

main() # Start her up fam
