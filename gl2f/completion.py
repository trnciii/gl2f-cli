from .core import local, board, member
import os


def page_first():
	keys = [i['key'] for i in board.table()] + ['today']
	boards = {k.split('/')[0] + ('/' if '/' in k else '') for k in keys}

	return f'''
    COMPREPLY=( $(compgen -W "{' '.join(boards)}" -- ${{cur}}) )
'''

def page_second():
	keys = [i['key'] for i in board.table()]
	pairs = [k.split('/') for k in keys if '/' in k]
	tree = {
		k:[p[1] for p in pairs if p[0] == k]
		for k in {p[0] for p in pairs}
	}

	mem_G2 = member.of_group('girls2').keys()
	mem_L2 = member.of_group('lucky2').keys()
	mem_l2 = member.of_group('lovely2').keys()

	tree['news'].append('today')
	tree['blogs'] += (mem_G2 | mem_L2 | mem_l2)
	tree['radio'] += (mem_G2 | mem_L2)

	return ''.join(f'''
      {k})
        COMPREPLY=( $(compgen -W "{' '.join(set(v))}" -P "${{prefix}}/" -- ${{realcur}}) )
        ;;
'''
		for k, v in tree.items())


def generate():
	with open(local.package_data('completion.bash')) as f:
		source = f.read()

	source = source\
		.replace('## REPLACE_PAGES_FIRST', page_first())\
		.replace('## REPLACE_PAGES_SECOND', page_second())

	return source


def add_args(parser):
	parser.set_defaults(handler=lambda _:print(generate()))
