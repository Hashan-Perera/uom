#promblem5
def smallest_multiple():
    activity=True
    n=2520
    while activity:
        n=n+1
        for i in range(11,20):
            if n%i!=0:
                break
        else:
            activity=False
            print(n)
smallest_multiple()