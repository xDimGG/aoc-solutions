const fs = require('fs');

const convert = (input, left = false, right = false) => {
	if (input.element) return convert(input.element, left, right);

	if (Array.isArray(input))
		for (let i = 0; i < 2; i++) {
			input[i] = convert(input[i], i === 0, i === 1);
		}

	return {
		left,
		right,
		element: input,
		parent: null,
	};
}

const setParents = node => {
	if (Array.isArray(node.element))
		for (const el of node.element) {
			el.parent = node;
			setParents(el);
		}
};

const fix = node => {
	if (Array.isArray(node.element))
		for (const el of node.element) {
			if (el.element?.element !== undefined) el.element = el.element.element;
			fix(el);
		}
};

const input = fs.readFileSync('./input.txt').toString().trim().split('\n').map(JSON.parse);

const depth = node => {
	let i = 0;
	while (node.parent) {
		i++;
		node = node.parent;
	}
	return i;
}

const left = node => {
	while (node?.left) node = node.parent;
	if (node.parent === null) return null;
	node = node.parent.element[0];
	while (Array.isArray(node.element)) node = node.element[1];
	return node;
};

const right = node => {
	while (node?.right) node = node.parent;
	if (node.parent === null) return null;
	node = node.parent.element[1];
	while (Array.isArray(node.element)) node = node.element[0];
	return node;
};

const explode = node => {
	if (Array.isArray(node.element)) {
		if (depth(node) === 4) {
			const l = left(node);
			if (l) l.element += node.element[0].element;
			const r = right(node);
			if (r) {
				r.element += node.element[1].element;
				// console.log(node.element[1]);
			}
			node.element = 0;
			return true;
		}

		for (const el of node.element)
			if (explode(el))
				return true;
	}

	return false;
};

const split = node => {
	if (Array.isArray(node.element)) {
		for (const el of node.element)
			if (split(el))
				return true;
	} else if (node.element >= 10) {
		node.element = [
			Math.floor(node.element / 2),
			Math.ceil(node.element / 2),
		];
		convert(node.element);
		setParents(node);
		return true;
	}

	return false;
};

const magnitude = node => {
	if (Array.isArray(node.element))
		return magnitude(node.element[0]) * 3 + magnitude(node.element[1]) * 2;
	return node.element;
};

const toString = input => Array.isArray(input.element) ? `[${input.element.map(toString).join(',')}]` : input.element.toString();

// let sum = input.shift();

// for (const el of input) {
// 	sum = [sum, el];
// 	sum = convert(sum);
// 	setParents(sum);
// 	fix(sum);
// 	let exploded = false;
// 	while ((exploded = explode(sum)) || split(sum)) {
// 		// console.log(`${exploded ? "explosion: " : "split:     "}${toString(sum)}`)
// 	}
// }

let max = 0;

for (let x of input) {
	for (let y of input) {
		if (x === y) continue;
		let sum = [JSON.parse(JSON.stringify(x)), JSON.parse(JSON.stringify(y))];
		sum = convert(sum)
		setParents(sum);
		fix(sum);
		while (explode(sum) || split(sum)) {
			// console.log(`${exploded ? "explosion: " : "split:     "}${toString(sum)}`)
		}

		const m = magnitude(sum);
		if (m > max) {
			max = m;
			console.log(toString(sum));
		}
	}
}

console.log(max);
// console.log(console.log(require('util').inspect(sum, {showHidden: false, depth: null, colors: true})));