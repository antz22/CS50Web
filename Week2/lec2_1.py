# tuples - pair values
coordinateX = 10.0
coordinateY = 20.0

coordinate = (10.0, 20.0)

#Create an empty set
s = set()

# Add elements to set
# each element that occurs is unique - like mathematical sets
s.add(1)
s.add(2)
s.add(3)
s.add(4)
s.add(3)

s.remove(2)

print(s)

print(f"The set has {len(s)} elements.")



# looping
for i in range(6):
    print(i)

names = ["Harry", "Ron", "Hermione"]
for name in names:
    print(name)
