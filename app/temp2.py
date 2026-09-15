import random

numbers = list(range(100))
random.shuffle(numbers)
print(numbers)

numbers = range(2, 8, 2)
print("Банан" * len(numbers))
print(list(numbers))


start, step, counter = 6,3,10
print([*range(start, counter * step + start, step)])

l1=[1,2,3]
l2=[3,2,1]
l3=[1,3,2]
if l1==l3:
    print("true")
else:
    print("false")

        
for i in range(2):
    for j in range(1, 6):
        if j % 2 == 1:
            continue
        if j == 3:
            break
        print(i, j)