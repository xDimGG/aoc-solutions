use std::{
	// cell::{RefCell, RefMut},
	cell::UnsafeCell as RefCell,
	fmt::Debug,
	fs::File,
	io::{BufRead, BufReader},
	rc::{Rc, Weak}, ops::{Add, AddAssign}, time::Duration, thread,
};

use nom::{
	branch::alt,
	character::complete::{char, u64},
	sequence::{delimited, separated_pair},
	IResult, Parser,
};

#[derive(Clone, Debug)]
struct Node {
	data: Data,
	parent: Option<Weak<RefCell<Node>>>,
	position: Position,
}

impl Node {
	unsafe fn sex(data: Data, parent: Option<RcNode>, position: Position) -> RcNode {
		let p = Rc::new(RefCell::new(Node {
			data,
			parent: parent.clone().map(|p| Rc::downgrade(&p)),
			position,
		}));
		if let Data::Children(a, b) = &(*p.get()).data {
			(*a.get()).parent = Some(Rc::downgrade(&p));
			(*b.get()).parent = Some(Rc::downgrade(&p));
			(*a.get()).position = Position::Left;
			(*b.get()).position = Position::Right;
		};
		p
	}

	unsafe fn sex_data(a: Data, b: Data, parent: Option<RcNode>, position: Position) -> RcNode {
		Self::sex(
			Data::Children(
				Rc::new(RefCell::new(Node {
					data: a,
					parent: None,
					position: Position::Left,
				})),
				Rc::new(RefCell::new(Node {
					data: b,
					parent: None,
					position: Position::Right,
				})),
			),
			parent,
			position,
		)
	}
}

#[derive(Clone)]
enum Data {
	Value(u64),
	Children(RcNode, RcNode),
}

impl Debug for Data {
	fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
		match self {
			Data::Value(v) => write!(f, "{:?}", v),
			Data::Children(a, b) => write!(f, "[{:?},{:?}]", unsafe { &(*a.get()).data }, unsafe { &(*b.get()).data } ),
		}
	}
}

impl Add for Data {
	type Output = Self;

	fn add(self, rhs: Self) -> Self::Output {
		if let Data::Value(a) = self {
			if let Data::Value(b) = rhs {
				return Data::Value(a + b)
			}
		}

		panic!("cannot add {:?} + {:?}", self, rhs);
	}
}

impl AddAssign for Data {
	fn add_assign(&mut self, rhs: Self) {
		*self = self.clone() + rhs;
	}
}

#[derive(Clone, Debug)]
enum Position {
	Left,
	Right,
	TBD,
}

type RcNode = Rc<RefCell<Node>>;

fn main() -> anyhow::Result<()> {
	unsafe {
		let f = File::open("./input.txt")?;
		let r = BufReader::new(f);

		let mut sum: Option<RcNode> = None;

		for line in r.lines() {
			let (_, item) = parse_list(None)(&line?).unwrap();

			sum = match sum {
				Some(s) => {
					println!("  {:?}", &(*s.get()).data);
					println!("+ {:?}", &(*item.get()).data);
					Some(Node::sex(
						Data::Children(
							Rc::clone(&s),
							Rc::clone(&item),
						),
						None,
						Position::TBD,
					))
				},
				None => Some(item),
			};

			reduce(Rc::clone(&sum.as_ref().unwrap().clone()));

			println!("= {:?}\n", &(*sum.as_ref().unwrap().get()).data);
		}

		// dbg!(&*sum.unwrap().get());
		dbg!(magnitude(&*sum.unwrap().get()));

		Ok(())
	}
}

unsafe fn parse_list(parent: Option<RcNode>) -> impl FnMut(&str) -> IResult<&str, RcNode> {
	move |input| {
		alt((
			u64.map(|x| {
				Rc::new(RefCell::new(Node {
					data: Data::Value(x),
					parent: parent.clone().map(|p| Rc::downgrade(&p)),
					position: Position::TBD,
				}))
			}),
			delimited(
				char('['),
				separated_pair(
					parse_list(parent.clone()),
					char(','),
					parse_list(parent.clone()),
				),
				char(']'),
			)
			.map(|(a, b)| Node::sex(Data::Children(a, b), parent.clone(), Position::TBD)),
		))(input)
	}
}

unsafe fn reduce(node: RcNode) {
	println!("    Reducing: {:?}", &(*node.get()).data);
	let mut exploded = false;
	while {
		exploded = explode(Rc::clone(&node), 0);
		exploded
	} || {
		exploded = false;
		split(Rc::clone(&node), 0)
	} {
		if exploded {
			println!("    exploded:{:?}", &(*node.get()).data);
		} else {
			println!("    splitted:{:?}", &(*node.get()).data);
		}
	}
	
}

unsafe fn explode(node: RcNode, depth: i32) -> bool {
	if let Data::Children(a, b) = (*node.get()).data.clone() {
		if depth >= 4 {
			first_left(&(*node.get())).clone().map(|(x, _)| { print!("add"); (*x.get()).data += (*a.get()).data.clone() });
			first_right(&(*node.get())).clone().map(|(x, _)| (*x.get()).data += (*b.get()).data.clone());
			(*node.get()).data = Data::Value(0);
			true
		} else {
			explode(a, depth + 1) || explode(b, depth + 1)
		}
	} else {
		false
	}
}

unsafe fn split(node: RcNode, depth: i32) -> bool {
	match (*node.get()).data.clone() {
		Data::Value(v) => {
			if v >= 10 {
				*(node.get()) = (*Node::sex_data(
					Data::Value(v / 2),
					Data::Value(v / 2 + (v % 2)),
					(*node.get())
						.parent
						.as_ref()
						.map(|p| p.clone().upgrade())
						.flatten(),
					(*node.get()).position.clone(),
				)
				.get())
				.clone();
				(*node.get()).clone().parent.unwrap();
				true
			} else {
				false
			}
		}
		Data::Children(a, b) => {
			split(a, depth + 1) || split(b, depth + 1)
		}
	}
}

unsafe fn parent(node: &Node) -> Option<RcNode> {
	node.parent.as_ref()?.clone().upgrade()
}

unsafe fn first_left(node: &Node) -> Option<(RcNode, i32)> {
	let mut depth = 4;
	let mut right_ancestor = Rc::new(RefCell::new(node.clone()));
	while let Position::Left = (*right_ancestor.get()).position {
		depth -= 1;
		right_ancestor = parent(&*right_ancestor.get())?;
	}
	println!("{:?}", &(*right_ancestor.get()).data);
	if (*right_ancestor.get()).parent.is_none() {
		return None;
	}
	right_ancestor = parent(&*right_ancestor.get())?;
	if let Data::Children(ref r, _) = (*right_ancestor.get()).data {
		right_ancestor = Rc::clone(r);
	}
	while let Data::Children(_, ref r) = (*right_ancestor.get()).data {
		depth += 1;
		right_ancestor = Rc::clone(r);
	}
	Some((Rc::clone(&right_ancestor), depth + 1))
}

unsafe fn first_right(node: &Node) -> Option<(RcNode, i32)> {
	let mut depth = 4;
	let mut right_ancestor = Rc::new(RefCell::new(node.clone()));
	while let Position::Right = (*right_ancestor.get()).position {
		depth -= 1;
		right_ancestor = parent(&*right_ancestor.get())?;
	}
	if (*right_ancestor.get()).parent.is_none() {
		return None;
	}
	right_ancestor = parent(&*right_ancestor.get())?;
	if let Data::Children(_, ref r) = (*right_ancestor.get()).data {
		right_ancestor = Rc::clone(r);
	}
	while let Data::Children(ref r, _) = (*right_ancestor.get()).data {
		depth += 1;
		right_ancestor = Rc::clone(r);
	}
	Some((Rc::clone(&right_ancestor), depth + 1))
}

#[allow(dead_code)]
unsafe fn magnitude(node: &Node) -> Option<u64> {
	match node.data {
		Data::Value(v) => Some(v),
		Data::Children(ref a, ref b) => {
			Some(3 * magnitude(&(*a.get()))? + 2 * magnitude(&(*b.get()))?)
		}
	}
}
