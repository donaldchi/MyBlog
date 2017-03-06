#!/Users/chi/lib/anaconda3/bin/python
#coding: utf-8

import requests
import sys, io
import cgi
import cgitb;cgitb.enable()

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

response = requests.get('http://127.0.0.1:8000/feed')

result = response.json()

size = result['length']

print('Content-type: text/html; charset=UTF-8\r\n')

print('<table id="latestblog" rules="rows">')

for count in range(0, size):
	if count == 6: break
	item = 'item' + str(count)
	time = result[item]['date']
	print("<tr><td><br><a href='http://127.0.0.1:8000/details/"+result[item]['slug']+"'>"+result[item]['title']+"</a>")
	print("<br>Updated: "+ time + "</td></tr>")
print("</table>")