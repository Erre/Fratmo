#!/usr/bin/python
###################################################
# Fratmo IRC Bot version 0.4 			  #
# Author: !R~ 					  #
# Description: stupid irc bot with plugin support #
# Thanks to my favourite drug-sniffer, Nigger- 	  #
###################################################

import os
import sys
import socket

class Bot:

	sys.path[0] += "/.plugins"
	diz_plugins = {}
	diz_load = {}
	autoload = int(raw_input("Set plugins autoload? (0 = No / 1 = Yes): "))
	 
	def __init__(self, server, port, channel, user, nick):
		
		self.channel = channel

                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.connect((server, port))

                self.s.send("USER %s 0 *: %s\r\n" % (user, user))
                self.s.send("NICK %s\r\n" % nick)
                self.s.send("JOIN %s\r\n" % channel)

		if self.autoload == 1:
			diz = self.create_diz_autoload()

                while True:

			self.data = self.s.recv(4096)

			if self.data.find ('PING') != -1:
                                self.pong()
			if self.data.find ('!load ') != -1:
				self.load_plugin((self.data.split("!load ")[1])[:-2])
			if self.data.find('!unload ') != -1:
				self.unload_plugin((self.data.split("!unload ")[1])[:-2])

			print self.data

			if self.autoload == 1:
				self.search_plugin(self.data, diz)
			if self.autoload == 0:
				self.search_plugin(self.data, self.diz_load)
				

	def pong(self):

		self.s.send("PONG %s \r\n" % self.data.split()[1])
        	self.s.send("JOIN %s\r\n" % self.channel)

	def autoload_plugin(self):

		return [__import__(i.split(".")[0], globals(), locals(), ['control', 'main']) for i in os.listdir(sys.path[0]) if not i.endswith("pyc")]

	def create_diz_autoload(self):
		
		for i in os.listdir(sys.path[0]):
			if not i.endswith("pyc"):
				plugin = __import__(i.split(".")[0], globals(), locals(), ['control'])
				self.diz_plugins[i.split(".")[0]] = plugin.control()

		list = self.autoload_plugin()
		for i in list:
			self.diz_load[i.control()] = i.main
		return self.diz_load

	def load_plugin(self, plugin):
		
		if plugin in self.diz_plugins.keys():
			self.s.send("PRIVMSG %s :Plugin already loaded\r\n" % (self.channel))
		else:
			try:
				plug = __import__(plugin, globals(), locals(), ['control', 'main']) 
				self.diz_load[plug.control()] = plug.main
				self.diz_plugins[plugin] = plug.control()
				self.s.send("PRIVMSG %s :Plugin succesfully loaded\r\n" % (self.channel))
			except:
				self.s.send("PRIVMSG %s :Failed to load plugin: no plugin named '%s'\r\n" % (self.channel, plugin))

	def unload_plugin(self, plugin):

		if plugin in self.diz_plugins.keys():
			del self.diz_load[self.diz_plugins[plugin]]
			del self.diz_plugins[plugin]
			self.s.send("PRIVMSG %s :Plugin successfully unloaded\r\n" % (self.channel))
		else:
			self.s.send("PRIVMSG %s :Cannot unload %s plugin: no plugin named '%s' was loaded\r\n" % (self.channel, plugin, plugin))
				
	def search_plugin(self, string, diz):

		list = [self.s, self.channel, self.data]

		for i in diz.keys():
			if string.find(i) != -1:
				start_plugin = diz[i]
				start_plugin(list)
				
Bot("irc.unitx.net", 6667, "#Unit-X", "Fratmo", "Fratmo") 
