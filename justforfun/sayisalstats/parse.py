import matplotlib.pyplot as plt

f = open("data.txt")
l = []
for line in f:
    l.extend(map(int, line.strip().split(" 	")[1:7]))

plt.hist(l)
plt.show()
