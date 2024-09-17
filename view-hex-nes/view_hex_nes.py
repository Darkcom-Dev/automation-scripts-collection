#!/usr/bin/python3
# -*- coding: utf-8 -*-
import argparse
import subprocess

def main(path):
	"""
	Opens a file and prints its content in hexadecimal format,
	with addresses and decoded text.

	Args:
		path (str): The path to the file to be read.
	"""
	text_lines = []
	with open(path, 'rb') as f:
		content = f.read()
		page = 0
		for i in range(0, len(content), 16):
			# Print a page number header every 256 bytes
			if i % 256 == 0:
				text_lines.append(f'\033[33mPage: {page}\033[0m'.center(80, '-'))
				page += 1

			# Calculate the line number and hex representation
			line_number = i // 16
			line_number_hex = '0x%04x' % line_number

			# Print the line number, address, hex dump and decoded text
			hex_string = ' '.join([f'{x:02x}' for x in content[i:i+16]])
			byte_string = content[i:i+16]
			# Modificar el manejo de la cadena decodificada para evitar caracteres no imprimibles
			decoded_string = ''.join([chr(x) if 32 <= x <= 126 else '.' for x in byte_string])

			text_lines.append(f"{line_number} \t \033[32m{line_number_hex}\033[0m \t {hex_string} \t \033[36m{decoded_string}\033[0m")

	long_text = ('\n'.join(text_lines))
	# Usar subprocess para pasar el texto a less
	process = subprocess.Popen(['less', '-R'], stdin=subprocess.PIPE)
	process.communicate(input=long_text.encode('utf-8'))

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Lee un archivo binario y lo imprime en formato hexadecimal y ASCII.")
	parser.add_argument("path", help="Ruta del archivo binario a leer")
	args = parser.parse_args()
	if args.path == None:
		parser.print_help()
	else:
		main(args.path)
