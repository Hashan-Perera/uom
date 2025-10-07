#project euler problems
#problem2

a = 1
b = 2
sum = 0

while a <= 4000000:
    if a % 2 == 0:
        sum += a
    a, b = b, a + b

print(sum)



