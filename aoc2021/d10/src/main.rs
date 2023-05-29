use core::panic;
use std::collections::VecDeque;
use std::fs::File;
use std::io::{self, BufRead, BufReader};
use std::ops::Index;

fn main() -> io::Result<()> {
	let f = File::open("./input.txt")?;
	let r = BufReader::new(f);
	let mut scores = vec![];

	for line in r.lines() {
		let line = line?;
		if process_line_p1(&line).is_none() {
			scores.push(process_line_p2(&line))
		}
	}

	scores.sort();
	println!("Sum: {}", scores[scores.len() / 2]);

	Ok(())
}

fn process_line_p1(s: &str) -> Option<i32> {
	let mut stack = Vec::new();

	for c in s.chars() {
		match c {
			'(' | '[' | '{' | '<' => stack.push(c),
			')' | ']' | '}' | '>' => match stack.pop() {
				Some(end) => {
					let corresponds = match c {
						')' => end == '(',
						']' => end == '[',
						'}' => end == '{',
						'>' => end == '<',
						_ => false,
					};
					if !corresponds {
						return op_to_score(c);
					}
				}
				None => return op_to_score(c),
			},
			_ => panic!("Unexpected char {c}"),
		}
	}

	None
}

fn process_line_p2(s: &str) -> i64 {
	let mut stack = Vec::new();

	for c in s.chars() {
		match c {
			'(' | '[' | '{' | '<' => stack.push(c),
			')' | ']' | '}' | '>' => {
				stack.pop();
			}
			_ => panic!("Unexpected char {c}"),
		}
	}

	stack.into_iter().rev().fold(0, |acc, c| {
		(acc * 5)
			+ match c {
				'(' => 1,
				'[' => 2,
				'{' => 3,
				'<' => 4,
				_ => panic!("Unexpected char {c}"),
			}
	})
}

fn op_to_score(c: char) -> Option<i32> {
	match c {
		')' => Some(3),
		']' => Some(57),
		'}' => Some(1197),
		'>' => Some(25137),
		_ => None,
	}
}
