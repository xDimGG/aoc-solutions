use std::{
	collections::HashSet,
	fs::File,
	io::{BufRead, BufReader, Result},
};

enum Direction {
	Vertical,
	Horizontal,
}

struct Instruction(Direction, u32);

impl Instruction {
	fn apply(&self, x: u32, y: u32) -> (u32, u32) {
		match self.0 {
			Direction::Vertical => {
				if x < (self.1) {
					(x, y)
				} else {
					(2 * self.1 - x, y)
				}
			}
			Direction::Horizontal => {
				if y < (self.1) {
					(x, y)
				} else {
					(x, 2 * self.1 - y)
				}
			}
		}
	}
}

fn main() -> Result<()> {
	let f = File::open("./input.txt")?;
	let r = BufReader::new(f);
	let mut xs: Vec<u32> = vec![];
	let mut ys: Vec<u32> = vec![];
	let mut instructions: Vec<Instruction> = vec![];

	for line in r.lines() {
		let line = line?;
		if line.starts_with("fold along") {
			let (axis, val) = &line["fold along ".len()..].split_once('=').unwrap();
			instructions.push(Instruction(
				if *axis == "x" {
					Direction::Vertical
				} else {
					Direction::Horizontal
				},
				val.parse().unwrap(),
			));
		} else if let Some((x, y)) = line.split_once(',') {
			xs.push(x.parse().unwrap());
			ys.push(y.parse().unwrap());
		}
	}

	let mut points: Vec<(u32, u32)> = xs.clone().into_iter().zip(ys.clone()).collect();

	for point in &mut points {
		for instruction in &instructions {
			*point = instruction.apply(point.0, point.1);
			// break;
		}
	}

	points.sort();
	points.dedup();

	let max_x = points.last().unwrap().0 + 1;
	let max_y = points
		.iter()
		.max_by(|(_, y1), (_, y2)| y1.cmp(y2))
		.unwrap()
		.1 + 1;

	for y in 0..max_y {
		for x in 0..max_x {
			if points.contains(&(x, y)) {
				print!("#")
			} else {
				print!(".")
			}
		}
		println!()
	}

	dbg!(points.len());

	Ok(())
}
