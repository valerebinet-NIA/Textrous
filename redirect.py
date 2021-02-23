#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

# enable debugging
import re
import cgi
import cgitb
import socket
import zlib
import os # get environment settings
cgitb.enable(display = 0, logdir = "./tmp")

print "Content-Type: text/html\n"

def getLink(words, genes):
	return '<a style="color:blue" href="https://textrous.irp.nia.nih.gov/clientph.cgi?genes=' + genes + '&words=' + words + '">' + words + '</a>'

def getTable(string, genes):
	res = '<table style="border:1px solid black;width:100%;">'
	res += '<tr style="background-color:#CCCCCC"><th style="text-align:left;border:1px solid black;width:50%">Word</th><th style="text-align:left;border:1px solid black;">Cosine Similarity</th></tr>'
	for i in xrange(0, len(string), 2):
		if i % 4 == 0:
			res += '<tr>'
		else:
			res += '<tr style="background-color:#DDDDDD">'
		res += "<td>" + getLink(string[i+1], genes) + "</td>"
		res += "<td>" + string[i] + "</td>"
		res += "</tr>"
	res += "</table>"
	return res

def main():
	try:
		genes = 'app'
		phrase = 'protein'
	except:
		genes = "asdf"
	HOST = os.environ['TEXTROUS_HOST'] # The remote host
	PORT = os.environ['TEXTROUS_PORT'] # The same port as used by the server
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, int(PORT)))
	s.sendall(genes+"="+phrase)
	data = s.recv(16384)
	s.close()
	data = zlib.decompress(str(data))
	if data:
		print '<!DOCTYPE html>'
		print '<html>'
		print '<meta http-equiv="Refresh" content="0; url=' + data + '" />'
		print '</head>'
		print '<body>'
		print '<p>Please follow <a href="' + data + '">this link</a>.</p>'
		print '</body>'
		print '</html>'
	else:	

		print '<!DOCTYPE html>'
		print '<html style="height:100%">'
		print '<head>'
		print '<link rel="stylesheet" type="text/css" href="https://textrous.irp.nia.nih.gov/t.css"/>'
		print '</head>'
		print '<body style="height:100%">'
	
		print '<div style="width:1000px;height:100px;position:absolute;left:0;top:0;overflow:hidden;background-color:#617f10">'
		print '<img style="position:absolute;top:5px;left:45px" src="logo2.bmp" height=90px>'
		print '<ul id="main-nav">'
		print '<li id="main-navli"><a id="main-navli" href="https://textrous.irp.nia.nih.gov/query.php">Home</a></li>'
		print '<li id="main-navli"><a id="main-navli" href="https://textrous.irp.nia.nih.gov/features.php">Features</a></li>'
		print '<li id="main-navli"><a id="main-navli" href="https://textrous.irp.nia.nih.gov/tutorial.php">Tutorial</a></li>'
		print '<li id="main-navli"><a id="main-navli" href="https://textrous.irp.nia.nih.gov/about.php">About</a></li>'
		print '<li id="main-navli"><a id="main-navli" href="https://textrous.irp.nia.nih.gov/contact.php">Contact</a></li>'
		print '</ul>'
		print '</div>'

	

		print '<div style="width:1000px;height:30px;position:absolute;left:0px;top:150px;overflow:hidden;">'	
		print '<ul id="sec-nav">'
		print '<li id="sec-navli"><a id="sec-navli" href="#"><b>Table (Cosine)</b></a></li>'
		print '<li id="sec-navli"><a id="sec-navli" href="clientz.cgi?genes=' + genes + '">' + 'Table (Z-Scores)</a></li>'
		print '<li id="sec-navli"><a id="sec-navli" href="clientp.cgi?genes=' + genes + '">' + 'Table (p-Values)</a></li>'
		print '<li id="sec-navli"><a id="sec-navli" href="clientw.cgi?genes=' + genes + '">' + 'Hierarchical Cloud</a></li>'
		print '<li id="sec-navli"><a id="sec-navli" href="clienth.cgi?genes=' + genes + '">' + 'Heat Map</a></li>'
		print '</ul>'
		print '</div>'	
	
		print '<div style="width:1000px;position:absolute;left:0px;top:180px;bottom:10px;overflow:auto;background-color:#EEEEEE">'
	
	
		print "</div>"
		print "</html>"

if __name__ == "__main__":
	main()
