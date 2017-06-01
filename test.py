f = open("device_log.txt","a")
stri = "vo doi"
f.write("thinh dz %s \n" %  stri)
f.close()
f = open("device_log.txt","r")
lines = f.readlines()
f.close()

number = len(lines)
if number > 10:
	f = open("device_log.txt","w")
	number = number -10
	for line in lines:
		if number == 0:
			f.write(line)
		else:
			number -= 1
	f.close()
