use anyhow::Result;
use std::{
	fs::read_to_string,
	io::{BufRead, BufReader},
};

use bitreader::BitReader;

#[derive(Debug)]
enum Op {
	Sum,
	Product,
	Min,
	Max,
	Gt,
	Lt,
	Eq,
}

#[derive(Debug)]
struct Header {
	version: u8,
	id: u8,
}

#[derive(Debug)]
enum PacketData {
	Value(u64),
	Operator {
		op: Op,
		len_type: bool,
		length: u16,
		packets: Vec<Packet>,
	},
}

#[derive(Debug)]
struct Packet {
	header: Header,
	data: PacketData,
}

impl Packet {
	fn value(&self) -> u64 {
		if let PacketData::Value(v) = self.data {
			return v as u64;
		};

		if let PacketData::Operator { op, packets, .. } = &self.data {
			let mut values = packets.iter().map(|p| p.value());

			match op {
				Op::Sum => values.sum(),
				Op::Product => values.product(),
				Op::Min => values.min().unwrap(),
				Op::Max => values.max().unwrap(),
				Op::Gt => {
					if values.next() > values.next() {
						1
					} else {
						0
					}
				}
				Op::Lt => {
					if values.next() < values.next() {
						1
					} else {
						0
					}
				}
				Op::Eq => {
					if values.next() == values.next() {
						1
					} else {
						0
					}
				}
			}
		} else {
			todo!()
		}
	}

	fn from_reader(r: &mut BitReader) -> Result<Self> {
		let header = Header {
			version: r.read_u8(3)?,
			id: r.read_u8(3)?,
		};

		let data = match header.id {
			4 => PacketData::Value(parse_value(r)?), // Literal value
			0..=3 | 5..=7 => {
				let len_type = r.read_bool()?;
				let length = r.read_u16(if len_type { 11 } else { 15 })?;
				let mut packets = vec![];
				if len_type {
					for _ in 0..length {
						packets.push(Packet::from_reader(r)?);
					}
				} else {
					let stop = r.remaining() - length as u64;
					while r.remaining() > stop {
						packets.push(Packet::from_reader(r)?);
					}
				}

				PacketData::Operator {
					op: match header.id {
						0 => Op::Sum,
						1 => Op::Product,
						2 => Op::Min,
						3 => Op::Max,
						5 => Op::Gt,
						6 => Op::Lt,
						7 => Op::Eq,
						_ => todo!(),
					},
					len_type,
					length,
					packets,
				}
			}
			_ => panic!("unexpected id"),
		};

		Ok(Self { header, data })
	}
}

fn parse_value(r: &mut BitReader) -> Result<u64> {
	let mut num = 0;
	loop {
		let cont = r.read_bool()?;
		num <<= 4;
		num |= r.read_u64(4)?;
		if !cont {
			break;
		}
	}

	Ok(num)
}

fn main() -> Result<()> {
	let str = read_to_string("./input.txt")?
		.chars()
		.collect::<Vec<char>>()
		.chunks(2)
		.map(|x| u8::from_str_radix(&x.iter().collect::<String>(), 16).unwrap())
		.collect::<Vec<u8>>();
	let mut r = BitReader::new(&str);

	let p = Packet::from_reader(&mut r)?;

	dbg!(p.value());
	// dbg!(p);

	Ok(())
}

fn version_sum(p: &Packet) -> u32 {
	p.header.version as u32
		+ match &p.data {
			PacketData::Operator { packets, .. } => packets.iter().map(|p| version_sum(p)).sum(),
			_ => 0,
		}
}
