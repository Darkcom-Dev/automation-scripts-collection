#!/usr/bin/python3
# -*- coding: utf-8 -*-
import argparse


def main(path):
	with open(path, 'rb') as f:
		content = f.read()
		page = 0
		for i in range(0, len(content), 16):
			if i % 256 == 0:
				print(f'\x1b[33mPage: {page}\x1b[0m'.center(80, '-'))
				page += 1
			line_number = i //16
			line_number_hex = '0x%04x' % i
			hex_string = ' '.join([f'{x:02x}' for x in content[i:i+16]])
			byte_string = content[i:i+16]
			decoded_string = byte_string.decode('ascii', 'ignore')
			print(f"\x1b[90m{line_number}\x1b[0m", f"\x1b[33m{line_number_hex}\x1b[0m", hex_string, f"\x1b[31m{decoded_string}\x1b[0m")

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('path', help='Path to the file')
	args = parser.parse_args()
	path = args.path
	main(path)
