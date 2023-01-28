import sys, re

with open('setup.py') as f:
	texts = f.read()

a = 'v' + re.search(r'version=\'(.+)\',\n', texts).group(1)
b = sys.argv[1]
print(a, b)
assert a == b
