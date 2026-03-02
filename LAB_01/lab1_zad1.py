#!/usr/bin/env python

source = raw_input("Give infile:\n> ")
dest = raw_input("Give outfile:\n> ")

with open(source, 'r') as src, open(dest, 'w') as dst:
	for line in src:
		dst.write(line)
