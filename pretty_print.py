import pprint
with open("c:/map") as F:
	a = 0
	for line in F:
		pprint.pprint(line)
		
		a+=1
		if a == 10:
			break