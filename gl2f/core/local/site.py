import os
import re, json
from . import fs, content
from ..config import data as config

def declare_js_string_constant(name, value):
	return f'const {name} = "{value}";\n'

def install_to(dst, link_type):
	import shutil, socket

	src = fs.package_data('site')

	if os.path.exists(dst):
		print(f'reinstalling {dst} that already exists')
		rm = shutil.rmtree if os.path.isdir(dst) else os.remove
		rm(dst)

	cp = shutil.copytree if os.path.isdir(src) else shutil.copyfile
	cp(src, dst)

	if link_type == 'symbolic':
		contents_path = 'contents'
		index_path = 'index.js'
		os.symlink(fs.refdir('contents'), os.path.join(dst, 'contents'))
		os.symlink(os.path.join(fs.home(), 'index.js'), os.path.join(dst, 'index.js'))
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
			path = os.path.join(fs.refdir_untouch('site'), 'index.js')
			with open(path, encoding='utf-8') as f:
				raw = f.read()
			return json.loads(re.sub(r'^.+?=', '', raw))

		except:
			return {}


	@staticmethod
	def value(i):
		from .. import board, article

		item = content.load(i)
		media = [i for i, _ in article.ptn_media.findall(item['values']['body'])]
		return {
			'title': item['values']['title'],
			'board': board.get('id', item['boardId'])['page'],
			'author': item.get('category', {'name':''})['name'],
			'date': item['openingAt'],
			'media': [''.join(x) for x in sorted(
				filter(lambda x:x[0] in media,
					(os.path.splitext(i) for i in fs.listdir(os.path.join('contents', i)))
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
			site = fs.refdir_untouch('site')

		if not site:
			print('site not installed. return')
			return

		if full:
			table = index.create_table(content.get_ids())
		else:
			prev = index.load()
			contents = list(set(content.get_ids()).difference(prev.keys()))
			table = prev | index.create_table(contents)

		out = os.path.join(fs.home(), 'index.js')
		with open(out, 'w', encoding='utf-8') as f:
			print(f'const table={json.dumps(table, separators=(",", ":"), ensure_ascii=False)}', file=f)

		print(f'saved {out}')


def build_body(item):
	from .. import article

	i = item['contentId']
	media_list = fs.listdir(f'contents/{i}')

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