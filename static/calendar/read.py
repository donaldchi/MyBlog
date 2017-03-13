#!/usr/bin/env python3

import codecs

fin  = codecs.open('calendar.js', 'r')
for line in fin:
	if line.strip()!="":
		print(line)
