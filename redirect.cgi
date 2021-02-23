#!/usr/bin/python2
# -*- coding: UTF-8 -*-

# enable debugging
import urllib2
import re
import cgi
import cgitb
import socket
import zlib
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

def getArticle(phrase, genes):
	p = " AND ".join(phrase.split())
	g = " OR ".join(genes.split())
	query = p + " ( " + g + " ) "
        url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?term=" + query
	url = re.sub(" ", "%20", url)
	page = urllib2.urlopen(url).read()
	ids = re.findall("<Id>([0-9]+)</Id>", page)
	if not ids:
		return ""
	else:
		return "https://www.ncbi.nlm.nih.gov/pubmed?term=" + " ".join(ids) + "[uid]"

def main():
	form = cgi.FieldStorage()
	try:
		genes = form['genes'].value
		phrase = form['phrase'].value
	except:
		genes = "asdf"
	data = getArticle(phrase, genes)
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
		print '<div style="width:1000px;height:50px;position:absolute;left:0;top:100px;overflow:hidden;background-color:#7A991A"><h1 style="color:#FFFFFF;margin:0;padding:5px;font-family:Verdana,Geneva,sans-serif;position:relative;left:50px">SEARCH</h1><p style="color:#FFFFFF;margin:0;position:absolute;right:10px;top:15px"></p><p><form style="position:absolute;left:500px;top:25%" name = "input" action = "client.cgi" method="GET"><input type="text" id="text" name="genes"><input type="submit" id="submit" value="Submit"></form></p></div>'	

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
		print '<div style="width:700px;height:100%;position:absolute;left:150px;top:0px;bottom:10px;overflow:auto:background-color:#FFFFFF">'
		print '<h3> Indirect Link Found </h3>'
		print '<hr />'
		print '<p style="text-indent:50px"> It appears that a PubMed search of your gene list for this specific phrase retrieved zero results. This could mean either an indirect link between your input and this specific noun phrase, or a possible false positive.</p>'
		print '</div>'
		print "</div>"
		print "</html>"

if __name__ == "__main__":
	main()
