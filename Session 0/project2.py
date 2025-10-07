def is_palindrome(n):
    return str(n) == str(n)[::-1]

max = 0

for i in range(100, 1000):
    for j in range(100, 1000):
        prod = i * j
        if is_palindrome(prod) and prod > max:
            max = prod

print(max)
