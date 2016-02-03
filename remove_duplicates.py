import os

with open('duplicates/files.txt') as f:
	for path in f.read().split('\n'):
		os.remove(path)