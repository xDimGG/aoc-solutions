import numpy as np

raw = open('./input.txt').read().split('\n\n')

enhancements = np.array([c == '#' for c in raw[0]])
image = np.array([[c == '#' for c in line] for line in raw[1].split('\n')])
ITERATIONS = 50

bits = (2 ** np.arange(9))[::-1]

for x in range(ITERATIONS):
	default = enhancements[0] and x % 2 == 1
	new_image = np.zeros((image.shape[0] + 2, image.shape[1] + 2), dtype=bool)

	image = np.pad(image, pad_width=2, constant_values=default, mode='constant')
	windows = np.lib.stride_tricks.sliding_window_view(image, (3, 3))
	for i, row in enumerate(windows):
		for j, window in enumerate(row):
			n = (window.flatten() * bits).sum()
			new_image[i, j] = enhancements[n]

	image = new_image
	if x == 1:
		print(new_image.sum())

print(new_image.sum())