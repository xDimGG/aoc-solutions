import statistics
import math

positions = [*map(int, open('./input.txt').read().split(','))]

m = statistics.median(positions)
print(int(sum([abs(x - m) for x in positions])))

mean = statistics.mean(positions)
values = [math.floor(mean), math.ceil(mean)]
results = [sum([abs(x - m) * (abs(x - m) + 1) / 2 for x in positions]) for m in values]
print(int(min(results)))
