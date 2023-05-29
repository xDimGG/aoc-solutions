elves = [sum(map(int, line.split('\n'))) for line in open('./input.txt').read().split('\n\n')]

# Possible optimization: remove sort
elves = sorted(elves, reverse=True)

print(elves[0])
print(sum(elves[:3]))