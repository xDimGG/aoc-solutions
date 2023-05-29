use std::{
	fs::File,
	io::{BufRead, BufReader},
	ops::{Add, AddAssign},
};

use nom::{
	branch::alt,
	character::complete::{char, u64},
	sequence::{delimited, separated_pair},
	IResult, Parser,
};

#[derive(Clone, Debug)]
enum Item {
	Value(u64),
	Pair(Box<Item>, Box<Item>),
	None,
}

impl Add for Item {
	type Output = Self;

	fn add(self, other: Self) -> Self::Output {
		if let Item::Value(a) = self {
			if let Item::Value(b) = other {
				return Item::Value(a + b)
			}
		}

		Self::Pair(Box::new(self), Box::new(other))
	}
}

impl AddAssign for Item {
    fn add_assign(&mut self, rhs: Self) {
			*self = self.clone() + rhs;
    }
}

#[derive(Clone, Debug)]
enum Position {
	Left,
	Right,
	None,
}

#[derive(Clone, Debug)]
struct ItemState {
	item: Box<Item>,
	depth: i8,
	pos: Position,
}

fn main() -> anyhow::Result<()> {
	let f = File::open("./input.txt")?;
	let r = BufReader::new(f);

	let mut sum = vec![];

	for line in r.lines() {
		let (_, item) = parse_list(&line?).unwrap();

		let mut states = flat_items(item);
		reduce(&mut states);

		if sum.is_empty() {
			sum = states;
		} else {
			sum.append(&mut states);
	
			for v in &mut sum {
				v.depth += 1;
			}
	
			reduce(&mut sum);
		}
	}

	dbg!(&sum);

	Ok(())
}

fn parse_list(input: &str) -> IResult<&str, Item> {
	alt((
		u64.map(Item::Value),
		delimited(
			char('['),
			separated_pair(parse_list, char(','), parse_list),
			char(']'),
		)
		.map(|(a, b)| Item::Pair(Box::new(a), Box::new(b))),
	))(input)
}

fn flat_items(item: Item) -> Vec<ItemState> {
	let mut acc = vec![];
	flat_items_inner(Box::new(item), Position::Left, &mut vec![ItemState {
		depth: -1,
		item: Box::new(Item::None),
		pos: Position::None,
	}], &mut acc);
	acc
}

fn flat_items_inner(item: Box<Item>, pos: Position, ancestors: &mut Vec<ItemState>, accumulated: &mut Vec<ItemState>) {
	let parent = ancestors.last().unwrap().clone();
	ancestors.push(ItemState {
		item: item.clone(),
		depth: parent.depth + 1,
		pos,
	});
	match *item {
		Item::Pair(a, b) => {
			flat_items_inner(a, Position::Left, &mut ancestors.clone(), accumulated);
			flat_items_inner(b, Position::Right, &mut ancestors.clone(), accumulated);
		},
		Item::Value(_) => { accumulated.push(ancestors.pop().unwrap()); },
		Item::None => panic!(),
	};
}

fn reduce(states: &mut Vec<ItemState>) {
	let mut i = 0;
	while i < states.len() {
		let state = states[i].clone();
		if state.depth == 5 {
			let sibling = states.remove(i + 1);

			if i > 0 {
				*states[i - 1].item += *state.item;
			}
			if i < states.len() - 1 {
				*states[i + 1].item += *sibling.item;
			}

			states[i].item = Box::new(Item::Value(0));
			states[i].depth -= 1;

			// Let's go back an element and check the new states
			if i > 0 {
				i -= 1;
			}
			continue;
		}

		if let Item::Value(v) = *state.item {
			if v >= 10 {
				states[i] = ItemState {
					depth: state.depth + 1,
					item: Box::new(Item::Value(v / 2)),
					pos: Position::Left,
				};
				states.insert(i + 1, ItemState {
					depth: state.depth + 1,
					item: Box::new(Item::Value(v / 2 + (v % 2))),
					pos: Position::Right,
				});

				// Let's check our new states
				// if i > 0 {
				// 	i -= 1;
				// }
				continue;
			}
		}

		i += 1;
	}
}

fn serialize_states(states: &Vec<ItemState>) -> String {
	let mut str = String::with_capacity(states.len() * 3);

	for (i, el) in states.iter().enumerate() {
		if let Item::Value(v) = *el.item {
			if i > 0 {
				let diff = el.depth - states[i - 1].depth;
				// if diff == 0 {
				// 	str += 
				// }
				let l_bracket = if diff < 0 { "[" } else { "]" };
				let r_bracket = if diff < 0 { "]" } else { "[" };
				str += &r_bracket.repeat(diff.abs() as usize);
				str += &l_bracket.repeat(diff.abs() as usize);
				// if diff 
			} else {
				str += &"[".repeat(el.depth as usize);
			}
	
			str += &v.to_string();

			if i == states.len() - 1 {
				str += &"]".repeat(el.depth as usize);
			} else if matches!(el.pos, Position::Left) {
				str += ",";
			}
		}
	}

	str
}

fn magnitude(states: &Vec<ItemState>) -> u64 {
	states.iter().fold(0, |acc, state| {
		if let Item::Value(v) = *state.item {
			acc + v.pow((state.depth as u32 - 1) * match state.pos {
				Position::Left => 3,
				Position::Right => 2,
				Position::None => panic!(),
			})
		} else {
			acc
		}
	})
}
