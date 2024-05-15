import re
import os, json
from .core import pretty, local
from .core.config import data as config
from .core.local import site, archive

def ls(args):
	items = [local.content.load(i) for i in sorted(local.content.get_ids())]
	if args.order:
		a = args.order.split(':')
		items.sort(key=lambda i: i[a[0]], reverse=(len(a)==2 and a[1]=='desc'))

	if not 'page' in args.format:
		args.format = 'page:' + args.format

	fm = pretty.from_args(args, items)
	for i in items:
		fm.print(i, encoding=args.encoding)


def clear_cache():
	if d:=local.fs.refdir_untouch('cache'):
		for i in os.listdir(d):
			os.remove(os.path.join(d, i))


def open_site():
	import webbrowser

	html = os.path.join(local.fs.home(), 'site', 'index.html')

	if not os.path.exists(html):
		if 'n' != input('site not installed. install now? (Y/n)').lower():
			site.install_to(os.path.join(local.fs.home(), 'site'), 'relative')
		else:
			return
	else:
		site.index.main()

	webbrowser.open(f'file://{html}')


def add_to():
	return 'gl2f', 'local'

def add_args(parser):
	parser.description = 'Manage local data'

	sub = parser.add_subparsers()

	sub.add_parser('clear-cache', description='remove media cache').set_defaults(handler=lambda _:clear_cache())
	sub.add_parser('dir', description='Path of gl2f directory').set_defaults(handler=lambda _:print(local.fs.home()))

	p = sub.add_parser('export', description='Export saved contents to an archive')
	p.add_argument('-o', default='.')
	p.set_defaults(handler=lambda args:archive.export_contents(args.o))

	p = sub.add_parser('import', description='Import contents from an archive')
	p.add_argument('archive')
	p.set_defaults(handler=lambda args:archive.import_contents(args.archive))

	sub.add_parser('index', description='Create index of contents for web viewer').set_defaults(handler = lambda _:site.index.main(full=True))
	sub.add_parser('install', description='Install static web viewer').set_defaults(handler=lambda _:site.install_to(os.path.join(local.fs.home(), 'site'), 'relative'))

	p = sub.add_parser('ls', description='List all local contents')
	p.add_argument('--order', type=str,
		help='sort order')
	pretty.add_args(p)
	p.add_argument('--encoding')
	p.set_defaults(handler=ls, format='author:title')

	sub.add_parser('open', description='Open local static web viewer in the browser').set_defaults(handler=lambda _:open_site())
	sub.add_parser('stat', description='Show storage statistics').set_defaults(handler=lambda _:print('\n'.join(f'{k:10} items: {v["count"]}, size: {v["size"]/(1024**3):,.2f} GB' for k, v in local.content.stat().items())))

	p = sub.add_parser('serve', description='Serve web viewer')
	p.add_argument('-p', '--port', type=int,  default=config['serve-port'],
		help='Set port to host on')
	p.add_argument('--open', action='store_true',
		help='Also open in the browser')
	p.set_defaults(handler=lambda args:site.serve(args.port, args.open))

	return sub

def set_compreplies():
	from .completion import if_else
	return {
		'import': '_filedir',
		'export': if_else('$prev == -o', '_filedir'),
		'ls': '''if [ $prev == "-f"  ] || [ $prev == "--format" ]; then
  __gl2f_complete_format
fi'''
	}
