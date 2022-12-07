#!/usr/bin/env python3

import hashlib

filename = '/home/rotivo/P2-11234627-CEN0336/script_getORF.py'
hasher = hashlib.md5()
with open(filename, 'rb') as open_file:
    content = open_file.read()
    hasher.update(content)
print(hasher.hexdigest())

filename2 = '/home/rotivo/P2-11234627-CEN0336/notas.py'
hasher = hashlib.md5()
with open(filename2, 'rb') as open_file:
	content = open_file.read()
	hasher.update(content)
print(hasher.hexdigest())

filename3 = '/home/rotivo/P2-11234627-CEN0336/notas_corrigido.py'
hasher = hashlib.md5()
with open(filename3, 'rb') as open_file:
	content = open_file.read()
	hasher.update(content)
print(hasher.hexdigest())

