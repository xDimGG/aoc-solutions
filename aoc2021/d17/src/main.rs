use nom::{
	bytes::streaming::{tag, take},
	character::{complete::digit1, self},
	combinator::{map, map_res},
	error::ErrorKind,
	number::{self, streaming::be_u16},
	sequence::{separated_pair, tuple},
	IResult, Needed,
};
use std::{fs::read_to_string, ops::RangeInclusive, str::FromStr};

fn parse_range(input: &str) -> IResult<&str, RangeInclusive<i32>> {
	map(
		separated_pair(
			character::complete::i32,
			tag(".."),
			character::complete::i32,
		),
		|(a, b)| a..=b,
	)(input)
}

fn parse_input(input: &str) -> IResult<&str, Area> {
	let (input, (_, a, _, b)) = tuple((
		tag("target area: x="),
		parse_range,
		tag(", y="),
		parse_range,
	))(input)?;
	Ok((input, Area(a, b)))
}

fn main() -> anyhow::Result<()> {
	let str = read_to_string("./input.txt")?;

	let (_, area) = parse_input(&str).unwrap();

	let mut xs = vec![];
	let mut x_test = 1;
	while x_test <= *area.0.end() {
		let mut sim = State::new(x_test, 0);
		while !(sim.before(&area) || sim.after(&area)) {
			if area.0.contains(&sim.x) {
				xs.push(x_test);
				break;
			}

			sim.step();
		}

		x_test += 1;
	}

	xs.sort();
	xs.dedup();

	// dbg!(xs);

	let mut total = 0;
	let mut y_test = -300;
	loop {
		for (i, x) in xs.iter().enumerate() {
			let mut state = State::new(*x, y_test);
			if state.step_until_hit(&area) {
				total += 1;
				dbg!(state.max_y);
				dbg!(total);
			}
		}
		y_test += 1;
	}

	dbg!(total);

	// for (i, x) in xs.iter().enumerate() {
	// 	for y_test in -300..100 {
	// 		let mut state = State::new(*x, y_test);
	// 		if state.step_until_hit(&area) {
	// 			// println!("{},{}", x, y_test);
	// 			dbg!(state.max_y);
	// 			total += 1;
	// 			dbg!(total);
	// 		}
	// 	}

	// 	// if state.after(&area) {
	// 	// 	xs.drain(i..)
	// 	// }

	// }

	
	dbg!(State::new(7, -1).step_until_hit(&area));

	Ok(())
}

#[derive(Debug)]
struct Area(RangeInclusive<i32>, RangeInclusive<i32>);

#[derive(Debug)]
struct State {
	x: i32,
	x_vel: i32,
	y: i32,
	y_vel: i32,
	max_y: i32,
}

impl State {
	fn new(x_vel: i32, y_vel: i32) -> Self {
		Self {
			x: 0,
			x_vel,
			y: 0,
			y_vel,
			max_y: 0,
		}
	}

	fn step(&mut self) {
		self.x += self.x_vel;
		self.y += self.y_vel;
		if self.x_vel > 0 {
			self.x_vel -= 1;
		}
		if self.x_vel < 0 {
			self.x_vel += 1;
		}

		self.y_vel -= 1;

		if self.y > self.max_y {
			self.max_y = self.y;
		}
	}

	fn step_until_hit(&mut self, area: &Area) -> bool {
		while !self.dead(area) {
			self.step();
			if self.within(area) {
				return true
			}
		}

		false
	}

	fn within(&self, area: &Area) -> bool {
		area.0.contains(&self.x) && area.1.contains(&self.y)
	}

	fn after(&self, area: &Area) -> bool {
		self.x > *area.0.end()
	}

	fn before(&self, area: &Area) -> bool {
		self.x_vel == 0 && self.x < *area.0.start()
	}

	fn under(&self, area: &Area) -> bool {
		self.y_vel < 0 && self.y < *area.1.end().min(area.1.start())
	}

	fn dead(&self, area: &Area) -> bool {
		self.after(area) || self.before(area) || self.under(area)
	}
}
