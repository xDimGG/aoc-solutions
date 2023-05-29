use std::{rc::{Rc, Weak}, cell::RefCell};


#[derive(Clone, Debug)]
struct Node {
	parent: Option<Weak<RefCell<Node>>>,
	data: Data,
}

#[derive(Clone, Debug)]
enum Data {
	Value(i32),
	Pair(Rc<RefCell<Node>>, Rc<RefCell<Node>>),
}

fn main() {
	let mut a = Rc::new(RefCell::new(Node {
		parent: None,
		data: Data::Value(0),
	}));
	let b = Node {
		parent: Some(Rc::downgrade(&a)),
		data: Data::Value(1),
	};
	let c = Node {
		parent: Some(Rc::downgrade(&a)),
		data: Data::Value(2),
	};

	{	
		a.borrow_mut().data = Data::Pair(Rc::new(RefCell::new(b)), Rc::new(RefCell::new(c)));
	}

	if let Data::Pair(a, b) = &a.borrow().data {
		dbg!(a.borrow().parent.as_ref().unwrap().upgrade().unwrap().borrow());
	};
}