const arr = Array.from({ length: 1000 }, () => Array.from({ length: 1000 }, () => 0));

for (let y = 0; y < 1000; y++) {
	for (let x = 0; x < 1000; x++) {
		arr[y][x] = 1;
	}
}