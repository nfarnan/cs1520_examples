def foo(*args):
	print(args)

foo()
foo(1, 2, 3, 4, 5)
foo("a", "string", 5, 8, "1")
foo(1, 2)
foo(*list(range(100)))
#foo("a", "string", 5, 8, "1", key="key")  # TypeError, unexpected keyword argument

def faux_print(*args, sep=" ", end="\n"):
	rv = str(args[0])
	for a in args[1:]:
		rv = rv + sep + a
	rv += end
	print(f"Would print '{rv}'")

faux_print("hello", "there", "testing")

def bar(**kwargs):
	print(kwargs)

bar(a="a", b="b", c=3)
#bar(5, a="a", b="b", c=3)  # TypeError, bar() takes 0 positional arguments but 1 was given

def baz(*args, **kwargs):
	print(args)
	print(kwargs)

baz(1, 2, 3, a="a", b="b", c="c")

def check(a, b, c):
	print(a)
	print(b)
	print(c)
	print()

l = [1, 2, 3]
check(*l)

d = {"b":2, "a":1, "c":3}
check(**d)
