use std::{
	collections::{hash_map::Entry, HashMap, HashSet},
	fs::File,
	io::{BufRead, BufReader},
};

fn is_little_cave(name: String) -> bool {
	name != "start" && name.to_ascii_lowercase() == *name
}

#[derive(Default, PartialEq, Eq)]
struct Graph {
	nodes: HashMap<String, HashSet<String>>,
}

impl Graph {
	fn insert_node(&mut self, name: String) {
		if !self.nodes.contains_key(&name) {
			self.nodes.insert(name, HashSet::new());
		}
	}

	fn insert_edge(&mut self, a: String, b: String) {
		self.insert_node(a.clone());
		self.insert_node(b.clone());
		self.nodes.get_mut(&a).unwrap().insert(b.clone());
		self.nodes.get_mut(&b).unwrap().insert(a.clone());
	}

	fn neighbors(&self, name: String) -> Option<&HashSet<String>> {
		self.nodes.get(&name)
	}
}

struct Run<'a> {
	graph: &'a Graph,
	visited_small_caves: HashSet<String>,
}

impl<'a> Run<'a> {
	fn new(graph: &'a Graph) -> Self {
		Self {
			graph,
			visited_small_caves: HashSet::new(),
		}
	}

	fn run_pathfinding(&mut self, entry: String, exit: String) -> Vec<Vec<String>> {
		let mut paths = Vec::new();

		if is_little_cave(entry.clone()) {
			self.visited_small_caves.insert(entry.clone());
		}

		for n in self.graph.neighbors(entry.clone()).unwrap() {
			if n == "start" || self.visited_small_caves.contains(n) {
				continue;
			}

			if *n == exit {
				paths.push([exit.clone()].into());
				continue;
			}

			let mut r = Self::new(&self.graph);
			r.visited_small_caves = self.visited_small_caves.clone();

			let mut found_paths = r.run_pathfinding(n.clone(), exit.clone());
			for p in &mut found_paths {
				p.insert(0, n.clone());
				if entry == "start" {
					p.insert(0, entry.clone());
				}
			}

			paths.append(&mut found_paths)
		}

		paths
	}
}

struct RunP2<'a> {
	graph: &'a Graph,
	special_cave: (String, i32),
	visited_small_caves: HashSet<String>,
}

impl<'a> RunP2<'a> {
	fn new(graph: &'a Graph, special_cave_name: String) -> Self {
		Self {
			graph,
			special_cave: (special_cave_name, 0),
			visited_small_caves: HashSet::new(),
		}
	}

	fn run_pathfinding(&mut self, entry: String, exit: String) -> Vec<Vec<String>> {
		let mut paths = Vec::new();

		if is_little_cave(entry.clone()) {
			self.visited_small_caves.insert(entry.clone());
			if *entry == self.special_cave.0 {
				self.special_cave.1 += 1;
			}
		}

		for n in self.graph.neighbors(entry.clone()).unwrap() {
			if *n == self.special_cave.0 {
				if self.special_cave.1 >= 2 {
					continue;
				}
			} else {
				if n == "start" || self.visited_small_caves.contains(n) {
					continue;
				}
			}

			if *n == exit {
				paths.push([exit.clone()].into());
				continue;
			}

			let mut r = Self::new(&self.graph, self.special_cave.0.clone());
			r.visited_small_caves = self.visited_small_caves.clone();
			r.special_cave.1 = self.special_cave.1;

			let mut found_paths = r.run_pathfinding(n.clone(), exit.clone());
			for p in &mut found_paths {
				p.insert(0, n.clone());
				if entry == "start" {
					p.insert(0, entry.clone());
				}
			}

			paths.append(&mut found_paths)
		}

		paths
	}
}

fn main() -> std::io::Result<()> {
	let f = File::open("./input.txt")?;
	let r = BufReader::new(f);
	let mut g = Graph::default();

	for line in r.lines() {
		let line = line?;
		let (a, b) = line.split_once('-').unwrap();
		g.insert_edge(a.into(), b.into());
	}

	let mut paths = HashSet::new();

	for cave in g.nodes.keys() {
		if is_little_cave(cave.clone()) {
			let r = Run::new(&g).run_pathfinding(String::from("start"), String::from("end"));
			// let r = RunP2::new(&g, cave.clone()).run_pathfinding(String::from("start"), String::from("end"));
			for path in r {
				paths.insert(path.join(","));
			}
		}
	}

	// let r = Run::new(&g).run_pathfinding(String::from("start"), String::from("end"));
	// for path in r {
	// 	paths.insert(path.join(","));
	// }

	dbg!(paths);

	Ok(())
}
