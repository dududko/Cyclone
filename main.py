from cyclone1.cyclone import Cyclone


def myFunction(n):
    for i in range(n):
        if i % 2 == 0:
            print(i)
            continue

the_world_is_flat = True
if the_world_is_flat:
    print("Be careful not to fall off!")
# this is first comment
print(2 + 2)
text = 2 ** 6
t = text / 2
print("doesn't ")
print("doesn\'t ")

squares = [1, 2, 4, 9, 16]
squares = squares + [25]
squares.append(6 ** 2)
print(squares[-1])

i = 0;
while i < len(squares):
    print(squares[i])
    i = i + 1

# x = input("write down x: ")
x = 0
if x == 0:
    print("0")
elif x == 1:
    print("1")
else:
    print(x)

print(range(1, 10))
myFunction(10)
print()
ls = [1, 10, 2]
print(list(range(*ls)))

x = Cyclone()
x.set_pos([1, 2])
x.set_size(3, 20)
print(x.pos)
print(x.sizeX)
print(x.sizeY)
