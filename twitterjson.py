import json
import pprint
with open("c:/twitter.json") as F:
	for line in F:
		pprint.pprint(json.loads(line))
		break
