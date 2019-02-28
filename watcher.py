import os
import time

old_out = ""
while True:
	files = [f.replace(".txt", "").replace("_", "") for f in os.listdir("out_random/")]
	d = {}
	for file in files:
		if file[-1] not in d:
			d[file[-1]] = []
		else:
			d[file[-1]].append(int(file[:-1]))

	keylist = d.keys()
	keylist = sorted(keylist)
	out = ''.join([(str(x) + ": " + str(max(d[x])) + "\n") for x in keylist])
	if out != old_out:
		os.system("clear")
		print(out)
	old_out = out
	time.sleep(0.2)