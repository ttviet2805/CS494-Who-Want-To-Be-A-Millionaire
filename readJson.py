import re

def readJson(filePath):
	with open(filePath, 'r') as file:
		content = file.read()
	
	x = re.findall(r'\{(?s:.*?)\}', content)
	return x

x = readJson('data.py')

for e in x:
	print(e) 