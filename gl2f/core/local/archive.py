import os, json
from . import fs, content
from .. import pretty

def colored_diff_lines(left, right):
	import difflib
	from ...ayame import terminal as term

	try:
		with open(left, encoding='utf-8') as l, open(right, encoding='utf-8') as r:
			return map(lambda l:
					term.mod(l, term.color('green')) if l.startswith('+')
					else term.mod(l, term.color('red')) if l.startswith('-')
					else l,
				difflib.unified_diff(l.readlines(), r.readlines(), fromfile=left, tofile=right)
			)
	except UnicodeDecodeError:
		return [
			'Not text files\n',
			term.mod(f'- {left}\n', term.color('red')),
			term.mod(f'+ {right}\n', term.color('green')),
		]

class ImportChecker:
	def __init__(self, left, right):
		from filecmp import dircmp, cmpfiles

		self.items = os.listdir(right)

		self.common = [i for i in self.items if os.path.isdir(os.path.join(left, i))]
		self.right_only = [i for i in self.items if i not in self.common]
		self.compare = {i:dircmp(os.path.join(left, i), os.path.join(right, i)) for i in self.common}

		self.identical = [k for k, v in self.compare.items() if not v.diff_files]
		self.diff_files = {k:v.diff_files for k, v in self.compare.items() if v.diff_files}
		self.right_only_files = {k: list(filter(
			lambda f: os.path.isfile(os.path.join(right, k, f)),
			v.right_only))
			for k, v in self.compare.items()
		}
		self.unknown = {k: list(filter(
			lambda i:os.path.isdir(os.path.join(right, k, i)),
			v.right_list))
			for k, v in self.compare.items()
		}

	def report(self):
		print(f'{len(self.items)} total contents')
		print('\t', ' '.join(self.items))

		print(f'{len(self.identical)} same contents')
		print('\t', ' '.join(self.identical))

		print(f'{len(self.right_only)} new contents')
		print(' '.join(self.right_only))

		print(f'{sum(map(len, self.right_only_files.values()))} new files')
		print('\n'.join(f'\t{k}\n\t\t{v}' for k, v in self.right_only_files.items() if v))

		print(f'{sum(map(len, self.diff_files.values()))} diff files')
		print('\n'.join(f'\t{k}\n\t\t{v}' for k, v in self.diff_files.items() if v))

		print(f'{sum(map(len, self.unknown.values()))} unchecked subdirs')
		print('\n'.join(f'\t{k}\n\t\t{v}' for k, v in self.unknown.items() if v))

	def all_diff_files(self):
		from itertools import chain
		return chain.from_iterable((os.path.join(c, f) for f in files) for c, files in self.diff_files.items())

	def new_files(self):
		from itertools import chain
		return chain.from_iterable((os.path.join(k, i) for i in v) for k, v in self.right_only_files.items())


def import_contents(src):
	import shutil, tempfile
	from ...ayame import terminal as term

	left = fs.refdir('contents')
	tempdir = tempfile.TemporaryDirectory()
	right = tempdir.name

	print(f'extracting archive ({os.path.getsize(src)/1024**3:.2f} GB).')
	shutil.unpack_archive(src, extract_dir=right)

	checker = ImportChecker(left, right)
	checker.report()

	def view():
		fm = pretty.Formatter(f='id:date-p:author:title', fd='%m/%d')
		for i in os.listdir(right):
			filepath = os.path.join(right, i, f'{i}.json')
			with open(filepath, encoding='utf-8') as f:
				fm.print(json.load(f))

	def copy_new_contents():
		for i in checker.right_only:
			shutil.copytree(os.path.join(right, i), os.path.join(left, i))
			print(f'copied: {i}')
		print()

	def copy_new_files():
		for file in checker.new_files():
			_left = os.path.join(left, file)
			if os.path.exists(_left):
				print(term.mod(f'file already exists {_left}', term.color('red')))
				continue
			shutil.copy2(os.path.join(right, file), _left)
			print(f'copied: {file}')
		print()

	def show_diff():
		nonlocal src
		diffs = [''.join(colored_diff_lines(os.path.join(left, f), os.path.join(right, f))) for f in checker.all_diff_files()]
		for diff in diffs:
			print(diff)

		if 'n' != input('Freeze conflicting files? (Y/n)').lower():
			default = os.path.splitext(f'diff-{os.path.basename(src)}')[0]
			o = input(f'Enter output directory name ({default})')
			if not o:
				o = default

			os.makedirs(o, exist_ok=True)

			with open(os.path.join(o, 'diff'), 'w', encoding='utf-8') as f:
				f.write(term.declip('\n'.join(diffs)))

			for file in checker.all_diff_files():
				src = os.path.join(right, file)
				dst = os.path.join(o, file)
				os.makedirs(os.path.dirname(dst), exist_ok=True)
				shutil.copy(src, dst)

	operations = list(filter(lambda x: x[2](), [
		('view all contents', view, lambda: True),
		('copy new contents', copy_new_contents, lambda: len(checker.right_only)),
		('copy new files', copy_new_files, lambda: any(checker.new_files())),
		('show diff', show_diff, lambda: len(checker.diff_files))
	]))
	selection = term.select([k for k, _, _ in operations])
	for s, (_, o, _) in zip(selection, operations):
		if s: o()

def export_contents(out):
	import shutil
	from datetime import datetime

	contents = fs.refdir_untouch('contents')
	if not contents:
		print('contents not found')
		return

	out = os.path.abspath(out)
	if os.path.isdir(out):
		now = datetime.now().strftime("%Y%m%d%H%M%S")
		base = os.path.join(out, f'gl2f-contents-{now}')
	else:
		par, chi = os.path.split(out)
		if not os.path.isdir(par):
			print(f'{par} is not a directory')
			return

		base = out

	sizeInGb = content.stat()["contents"]["size"]/1024**3
	print(f'zipping contents into {base}.zip ({sizeInGb:.2f} GB)')
	shutil.make_archive(base, 'zip', root_dir=contents)
