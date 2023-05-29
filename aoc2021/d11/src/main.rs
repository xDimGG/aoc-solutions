use std::{
	fs::File,
	io::{BufRead, BufReader},
	mem::MaybeUninit,
};

const SIZE: usize = 10;

struct Run<'a> {
	flashed: [[bool; SIZE]; SIZE],
	simulation: &'a mut Simulation,
}

impl<'a> Run<'a> {
	fn new(simulation: &'a mut Simulation) -> Self {
		Self {
			flashed: [[false; SIZE]; SIZE],
			simulation,
		}
	}

	fn step(&mut self) -> isize {
		let mut flashes = 0;

		for (y, arr) in self.simulation.entities.clone().iter().enumerate() {
			for (x, _) in arr.iter().enumerate() {
				flashes += self.incr(x as isize, y as isize);
			}
		}

		flashes
	}

	fn incr(&mut self, x: isize, y: isize) -> isize {
		if x < 0 || y < 0 || x > (SIZE - 1) as isize || y > (SIZE - 1) as isize {
			return 0;
		}
		if self.flashed[y as usize][x as usize] {
			0
		} else {
			let mut o = &mut self.simulation.entities[y as usize][x as usize];
			if o.energy == 9 {
				self.flashed[y as usize][x as usize] = true;
				o.energy = 0;
				1 + ([
					(-1, -1),
					(-1, 0),
					(-1, 1),
					(0, 1),
					(1, 1),
					(1, 0),
					(1, -1),
					(0, -1),
				])
				.iter()
				.map(|(dx, dy)| self.incr(x + dx, y + dy))
				.sum::<isize>()
			} else {
				o.energy += 1;
				0
			}
		}
	}
}

#[derive(Clone, Debug)]
struct Octopus {
	energy: u8,
}

struct Simulation {
	entities: [[Octopus; SIZE]; SIZE],
}

impl Simulation {
	fn new(entities: [[Octopus; SIZE]; SIZE]) -> Self {
		Simulation { entities }
	}

	fn run(&mut self) -> isize {
		Run::new(self).step()
	}
}

fn main() -> std::io::Result<()> {
	let mut octopuses: [[Octopus; SIZE]; SIZE] = unsafe { MaybeUninit::uninit().assume_init() };
	let f = File::open("./input.txt")?;
	let r = BufReader::new(f);

	for (y, line) in r.lines().enumerate() {
		for (x, c) in line?.chars().enumerate() {
			octopuses[y][x] = Octopus {
				energy: (c as u8 - '0' as u8),
			};
		}
	}

	let mut sim = Simulation::new(octopuses);

	'outer: for i in 0.. {
		sim.run();
		let first = sim.entities[0][0].energy;

		for arr in &sim.entities {
			for o in arr {
				if o.energy != first {
					continue 'outer;
				}
			}
		}

		print!("Loop {}", i + 1);
		break;
	}

	Ok(())
}
