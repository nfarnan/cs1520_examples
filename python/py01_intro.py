import random

# basic syntax overview example
r = random.randint(0, 100)
while r < 85:
	if r > 70:
		print(r, ":  so close!", sep="")
	elif r > 45:    # yes, the else if syntax is odd...
		print(r, end="")
		print(":  Getting there...")
	else:
		print(f"{r}:  Still so far away!")

	r = random.randint(0, 100)
print("OUT!")
