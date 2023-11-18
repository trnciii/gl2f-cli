from .core import local, board
from . import command_builder

def generate():
	with open(local.package_data('completion.bash')) as f:
		source = f.read()

	boards = board.tree()
	_, commands = command_builder.build(command_builder.builtin + command_builder.get_addon_registrars())

	source = source.replace('## REPLACE_PAGES_FIRST',
			f'''COMPREPLY=( $(compgen -W "{' '.join({k + ('/' if len(v)>0 else '') for k, v in boards.items()})}" -- ${{cur}}) )'''
		).replace('## REPLACE_PAGES_SECOND', ''.join(f'''
		  {k})
        COMPREPLY=( $(compgen -W "{' '.join(set(v))}" -P "${{prefix}}/" -- ${{realcur}}) )
        ;;'''
			for k, v in sorted(boards.items()) if len(v)>0)
		).replace('## REPLACE_COMMAND_TREE', gen_tree('gl2f'))

	return source

def gen_tree(current_parent):
	commands = command_builder.builtin + command_builder.get_addon_registrars()
	_, tree = command_builder.build(commands)

	cases = []
	for command in commands:
		parent, name = command.add_to()
		if parent != current_parent:
			continue

		if f'{parent}.{name}' in tree.keys():
			cases.append(f'''
    {name})
{gen_tree(f'{parent}.{name}')}
      ;;''')

		elif hasattr(command, 'set_compreply') and command.set_compreply():
			cases.append(f'''
    {name})
      {command.set_compreply()}
      ;;''')


	if current_parent != 'gl2f':
		command = next(c for c in commands if current_parent == '.'.join(c.add_to()))
		if hasattr(command, 'set_compreplies'):
			cases += [f'''
    {k})
      {v}
      ;;''' for k, v in command.set_compreplies().items()]

	depth = current_parent.count('.') + 1
	reply = f'''COMPREPLY=( $(compgen -W '{' '.join(tree[current_parent].choices.keys())}' -- "$cur") )'''
	ret = f'''if [[ $cword == {depth} ]]; then
	{reply}
else
	case ${{words[{depth}]}} in{''.join(cases)}
	esac
fi''' if cases else reply
	return '\n'.join(f'{"      " if depth>1 else "  "}{l}' for l in ret.splitlines())


def add_to():
	return 'gl2f', 'completion'

def add_args(parser):
	parser.set_defaults(handler=lambda _:print(generate()))

def set_compreply():
	return ''
