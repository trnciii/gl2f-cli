from .core import local, board, member
import os


def page_first():
	boards = {k + ('/' if len(v)>0 else '') for k, v in board.tree().items()}

	return f'''
    COMPREPLY=( $(compgen -W "{' '.join(boards)}" -- ${{cur}}) )
'''

def page_second():
	return ''.join(f'''
      {k})
        COMPREPLY=( $(compgen -W "{' '.join(set(v))}" -P "${{prefix}}/" -- ${{realcur}}) )
        ;;
'''
		for k, v in board.tree().items() if len(v)>0)


def generate():
	with open(local.package_data('completion.bash')) as f:
		source = f.read()

	source = source\
		.replace('## REPLACE_PAGES_FIRST', page_first())\
		.replace('## REPLACE_PAGES_SECOND', page_second())

	return source


def add_args(parser):
	parser.set_defaults(handler=lambda _:print(generate()))
