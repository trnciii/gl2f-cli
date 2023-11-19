import time
from gl2f import command_builder

class New_Subcommand:
	@staticmethod
	def add_to():
		return 'gl2f', 'new'

	@staticmethod
	def add_args(parser):
		parser.set_defaults(handler = lambda _:'new command')

class Overwright_Subcommand:
	@staticmethod
	def add_to():
		return 'gl2f', 'auth'

	@staticmethod
	def add_args(parser):
		parser.set_defaults(handler = lambda _:'overwritten auth')

class Overwright_Nested_Subcommand:
	@staticmethod
	def add_to():
		return 'gl2f.local', 'serve'

	@staticmethod
	def add_args(parser):
		parser.set_defaults(handler = lambda _:'overwritten local.serve')


def run_command(parser, arg_string, expected):
	args = parser.parse_args(arg_string)
	if hasattr(args, 'handler'):
		ret = args.handler(args)
		return expected == ret
	return False

def has_subcommand(tree, command, subcommand):
	return subcommand in tree[command].choices.keys()


def test_builtin_command_tree():
	parser, tree = command_builder.build(command_builder.builtin)
	assert {'gl2f', 'gl2f.auth', 'gl2f.config', 'gl2f.local'} == tree.keys()
	assert {
		'sixel', 'auth', 'cat', 'completion', 'config',
		'dl','local','ls','open','search',
	} ==  tree['gl2f'].choices.keys()
	assert {'login', 'remove', 'set-token', 'update'} == tree['gl2f.auth'].choices.keys()
	assert {'create', 'path', 'view', 'edit'} == tree['gl2f.config'].choices.keys()
	assert {
		'clear-cache', 'dir', 'export', 'import', 'index',
		'install', 'ls', 'open', 'stat', 'serve'
	} == tree['gl2f.local'].choices.keys()

def test_addons():
	registrars = [
		New_Subcommand,
		Overwright_Subcommand,
		Overwright_Nested_Subcommand
	]
	parser, tree = command_builder.build(command_builder.builtin + registrars)


	assert has_subcommand(tree, 'gl2f', 'new')
	assert run_command(parser, ['new'], 'new command')

	assert has_subcommand(tree, 'gl2f', 'auth')
	assert run_command(parser, ['auth'], 'overwritten auth')

	assert has_subcommand(tree, 'gl2f.local', 'serve')
	assert run_command(parser, ['local', 'serve'], 'overwritten local.serve')

def test_build_time():
	t0 = time.time()
	parser, tree = command_builder.build(command_builder.builtin)
	t1 = time.time()
	duration = t1 - t0
	assert duration < 0.02
