fl1 = open('QProblem3/output.txt')
fl2 = open('QProblem3/output1.txt')

data1 = fl1.read().splitlines()
data2 = fl2.read().splitlines()

print(len(data1), len(data2))
print(sum([1 if a != b else 0 for a, b in zip(data1, data2)]))
