import re
import os, json
from ..core import pretty, local
from ..core.config import data as config


def ls(args):
	items = [local.load_content(i) for i in sorted(local.listdir('contents'))]
	if args.order:
		a = args.order.split(':')
		items.sort(key=lambda i: i[a[0]], reverse=(len(a)==2 and a[1]=='desc'))

	if not 'page' in args.format:
		args.format = 'page:' + args.format

	fm = pretty.from_args(args, items)
	for i in items:
		fm.print(i, encoding=args.encoding)


def clear_cache():
	if d:=local.refdir_untouch('cache'):
		for i in os.listdir(d):
			os.remove(os.path.join(d, i))

def declare_js_string_constant(name, value):
	return f'const {name} = "{value}";\n'

def install_to(dst, link_type):
	import shutil, socket

	src = local.package_data('site')

	if os.path.exists(dst):
		print(f'reinstalling {dst} that already exists')
		rm = shutil.rmtree if os.path.isdir(dst) else os.remove
		rm(dst)

	cp = shutil.copytree if os.path.isdir(src) else shutil.copyfile
	cp(src, dst)


	if link_type == 'symbolic':
		contents_path = 'contents'
		index_path = 'index.js'
		os.symlink(local.refdir('contents'), os.path.join(dst, 'contents'))
		os.symlink(os.path.join(local.home(), 'index.js'), os.path.join(dst, 'index.js'))
	elif link_type == 'relative':
		contents_path = '../contents'
		index_path = '../index.js'

	else:
		raise RuntimeError('unknown path type')

	index.main(site=dst, full=True)

	with open(os.path.join(dst, 'constants.js'), 'w', encoding='utf-8') as f:
		f.write(declare_js_string_constant('hostname', config['host-name']))
		f.write(declare_js_string_constant('contentsPath', contents_path))
		f.write(declare_js_string_constant('indexPath', index_path))


	print(f'installed site into {dst}')


class index:
	@staticmethod
	def load():
		try:
			path = os.path.join(local.refdir_untouch('site'), 'index.js')
			with open(path, encoding='utf-8') as f:
				raw = f.read()
			return json.loads(re.sub(r'^.+?=', '', raw))

		except:
			return {}


	@staticmethod
	def value(i):
		from ..core import board, article

		item = local.load_content(i)
		media = [i for i, _ in article.ptn_media.findall(item['values']['body'])]
		return {
			'title': item['values']['title'],
			'board': board.get('id', item['boardId'])['page'],
			'author': item.get('category', {'name':''})['name'],
			'date': item['openingAt'],
			'media': [''.join(x) for x in sorted(
				filter(lambda x:x[0] in media,
					(os.path.splitext(i) for i in local.listdir(os.path.join('contents', i)))
				),
				key=lambda x:media.index(x[0])
			)],
			'expired': item.get('closingAt', None),
			'body': build_body(item)
		}


	@staticmethod
	def create_table(contents):
		from concurrent.futures import ThreadPoolExecutor
		with ThreadPoolExecutor() as e:
			values = e.map(index.value, contents)
		return {k:v for k, v in zip(contents, values)}


	@staticmethod
	def main(site=None, full=False):
		if not site:
			site = local.refdir_untouch('site')

		if not site:
			print('site not installed. return')
			return

		if full:
			table = index.create_table(local.listdir('contents'))
		else:
			prev = index.load()
			contents = list(set(local.listdir('contents')).difference(prev.keys()))
			table = prev | index.create_table(contents)

		out = os.path.join(local.home(), 'index.js')
		with open(out, 'w', encoding='utf-8') as f:
			print(f'const table={json.dumps(table, separators=(",", ":"), ensure_ascii=False)}', file=f)

		print(f'saved {out}')


def open_site():
	import webbrowser

	html = os.path.join(local.home(), 'site', 'index.html')

	if not os.path.exists(html):
		if 'n' != input('site not installed. install now? (Y/n)').lower():
			install_to(os.path.join(local.home(), 'site'), 'relative')
		else:
			return
	else:
		index.main()

	webbrowser.open(f'file://{html}')

def build_body(item):
	from ..core import article

	i = item['contentId']
	media_list = local.listdir(f'contents/{i}')

	def up(match):
		m, t = match.groups()
		try:
			p = next(p for p in media_list if p.startswith(m))
		except:
			return ''

		if t == 'image':
			return f'<img src=../contents/{i}/{p}></img>'
		elif t == 'video':
			return f'<video controls autoplay muted loop src=../contents/{i}/{p}></video>'
		else:
			return ''

	return article.ptn_media.sub(up, item['values']['body'])


def get_local_ip():
	import socket
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	try:
		s.connect(('8.8.8.8', 80))
		return s.getsockname()[0]
	except:
		return 'localhost'
	finally:
		s.close()

def serve(port, browse=False):
	import http.server, socketserver, socket, threading
	import webbrowser
	import tempfile

	webbrowser.register("termux-open '%s'", None)

	with tempfile.TemporaryDirectory() as tmp:
		site = os.path.join(tmp, 'site')
		print(site)
		install_to(site, 'symbolic')

		class Handler(http.server.SimpleHTTPRequestHandler):
			def __init__(self, *args, **kwargs):
				super().__init__(*args, directory=site, **kwargs)

			def end_headers(self):
				self.send_header('Accept-Ranges', 'bytes')
				super().end_headers()

		url = f'http://{get_local_ip()}:{port}'
		with socketserver.ThreadingTCPServer(('0.0.0.0', port), Handler) as httpd:
			print(f'serving at {url}')

			server_thread = threading.Thread(target=httpd.serve_forever)
			server_thread.daemon = True
			server_thread.start()

			try:
				if browse:
					webbrowser.open(url)
				server_thread.join()
			except  KeyboardInterrupt:
				pass


def add_to():
	return 'gl2f', 'local'

def add_args(parser):
	parser.description = 'Manage local data'
	from . import archive

	sub = parser.add_subparsers()

	sub.add_parser('clear-cache', description='remove media cache').set_defaults(handler=lambda _:clear_cache())
	sub.add_parser('dir', description='Path of gl2f directory').set_defaults(handler=lambda _:print(local.home()))

	p = sub.add_parser('export', description='Export saved contents to an archive')
	p.add_argument('-o', default='.')
	p.set_defaults(handler=lambda args:archive.export_contents(args.o))

	p = sub.add_parser('import', description='Import contents from an archive')
	p.add_argument('archive')
	p.set_defaults(handler=lambda args:archive.import_contents(args.archive))

	sub.add_parser('index', description='Create index of contents for web viewer').set_defaults(handler = lambda _:index.main(full=True))
	sub.add_parser('install', description='Install static web viewer').set_defaults(handler=lambda _:install_to(os.path.join(local.home(), 'site'), 'relative'))

	p = sub.add_parser('ls', description='List all local contents')
	p.add_argument('--order', type=str,
		help='sort order')
	pretty.add_args(p)
	p.add_argument('--encoding')
	p.set_defaults(handler=ls, format='author:title')

	sub.add_parser('open', description='Open local static web viewer in the browser').set_defaults(handler=lambda _:open_site())
	sub.add_parser('stat', description='Show storage statistics').set_defaults(handler=lambda _:print('\n'.join(f'{k:10} items: {v["count"]}, size: {v["size"]/(1024**3):,.2f} GB' for k, v in local.stat().items())))

	p = sub.add_parser('serve', description='Serve web viewer')
	p.add_argument('-p', '--port', type=int,  default=config['serve-port'],
		help='Set port to host on')
	p.add_argument('--open', action='store_true',
		help='Also open in the browser')
	p.set_defaults(handler=lambda args:serve(args.port, args.open))

	return sub

def set_compreplies():
	from ..completion import if_else
	return {
		'import': '_filedir',
		'export': if_else('$prev == -o', '_filedir'),
		'ls': '''if [ $prev == "-f"  ] || [ $prev == "--format" ]; then
  __gl2f_complete_format
fi'''
	}
