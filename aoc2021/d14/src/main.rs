use std::{
	collections::{hash_map::Entry, HashMap},
	fs::File,
	io::{BufRead, BufReader, Result},
	ops::Index,
};

fn main() -> Result<()> {
	let f = File::open("./input.txt")?;
	let mut r = BufReader::new(f);

	let mut template = String::new();
	r.read_line(&mut template)?;
	template = template.trim().into();
	r.read_line(&mut String::new())?;

	let mut insertions = HashMap::new();

	for line in r.lines() {
		let line = line?;
		let (l, r) = line.split_once(" -> ").unwrap();
		insertions.insert(l.to_string(), r.to_string().chars().next().unwrap());
	}

	dbg!(template.clone());

	let mut pairs: HashMap<String, u128> = HashMap::new();
	for pair in template.chars().collect::<Vec<char>>().windows(2) {
		*pairs.entry(pair.iter().collect::<String>()).or_insert(0) += 1;
	}
	let mut count = HashMap::new();
	for c in template.chars() {
		*count.entry(c).or_insert(0) += 1;
	}

	for _ in 1..=40 {
		let mut new_pairs: HashMap<String, u128> = HashMap::new();

		for (key, num) in pairs.clone() {
			if num == 0 {
				continue;
			}

			let res = insertions.get(&key).unwrap();
			let left = key.chars().next().unwrap().to_string() + &res.to_string();
			let right = res.to_string() + key.chars().last().unwrap().to_string().as_str();

			*new_pairs.entry(left).or_insert(0) += num;
			*new_pairs.entry(right).or_insert(0) += num;
			*count.entry(*res).or_insert(0) += num;
		}

		pairs = new_pairs;
	}

	dbg!(count.clone());
	dbg!(count.values().max().unwrap() - count.values().min().unwrap());

	Ok(())
}

fn expand(template: String, insertions: &HashMap<String, char>, iterations: i32) -> String {
	if iterations == 0 {
		template
	} else {
		expand(
			template
				.chars()
				.collect::<Vec<char>>()
				.windows(2)
				.map(|x| {
					format!(
						"{}{}",
						x[0],
						*insertions.get(&x.iter().collect::<String>()).unwrap()
					)
				})
				.collect::<String>()
				+ &template.chars().last().unwrap().to_string(),
			insertions,
			iterations - 1,
		)
	}
}
