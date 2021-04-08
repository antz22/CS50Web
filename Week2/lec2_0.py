# hello
print("hello world!")

# formatted strings
name = input("Name: ")
print("Hello, " + name + "!")
print(f"In other words, hello {name}!")

# input and conditions
n = int(input("Number: "))

if n > 0:
    print("n is positive.")
elif n < 0:
    print("n is negative")
else:
    print("n is zero")

# sequences and loops
name2 = "Harry"
print(name2[0])
names = ["Harry", "Ron", "Hermione"]
print(names[1][0])

names.append("Draco")
names.sort()
print(names)



