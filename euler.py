# 1 	Multiples of 3 and 5

n = 1000
mults = []
for i in range(1, n):
    if i % 3 == 0 or i % 5 ==0:
		mults.append(i)

sum(mults)

#2	Even Fibonacci numbers

		
>>> sum(mults)
233168


# https://projecteuler.net/problem=539

n = 1000

def get_p(n):
    vals = [i for i in range(1, n+1)]

    start_from_left = True

    while len(vals) > 1:
        new_list = []
        length = int(len(vals))
        if start_from_left == True:
            for v in range(1, length,2):
                num = int(vals[v])
                new_list.append(num)
        elif start_from_left == False:
            for v in range(length-2, -1, -2):
                num = vals[v]
                new_list.append(num)
                
        start_from_left = not start_from_left
        new_list.sort()
        vals = new_list
    
    return vals[0]

def get_s(n):

    total = 0
    for i in range(1, n + 1):
        total += get_p(i)

    return total

x = 10 ** 18
s = get_s(x)

print(s % 987654321)
