use std::{
	collections::HashSet,
	fs::File,
	io::{BufRead, BufReader, Result},
};

fn main() -> Result<()> {
	let f = File::open("./input.txt")?;
	let r = BufReader::new(f);

	let mut last = 0;
	let mut increments = 0;

	// for line in r.lines() {
	// 	let num = line?.parse::<u32>().unwrap();
	// 	if last == 0 {
	// 		last = num;
	// 		continue;
	// 	}

	// 	if last < num {
	// 		increments += 1;
	// 	}

	// 	last = num;
	// }

	for line in r
		.lines()
		.map(|s| s.unwrap().parse::<u32>().unwrap())
		.collect::<Vec<u32>>()
		.windows(3)
	{
		let num = line.iter().sum();
		if last == 0 {
			last = num;
			continue;
		}

		if last < num {
			increments += 1;
		}

		last = num;
	}

	dbg!(increments);

	Ok(())
}
