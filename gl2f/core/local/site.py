import os
import re, json
from .. import util
from ..config import data as config
from . import fs, content, index

def declare_js_string_constant(name, value):
	return f'const {name} = "{value}";\n'

def update_index_js():
	path = fs.refdir_untouch('site')
	if not os.path.isdir(path):
		return 'site is not installed'

	code = f'const table={util.read_all_text(index.get_path())}'
	util.write_all_text(os.path.join(path, 'index.js'), code)


def install_to(dst, link_type):
	import shutil

	src = fs.package_data('site')

	if os.path.exists(dst):
		print(f'reinstalling {dst} that already exists')
		rm = shutil.rmtree if os.path.isdir(dst) else os.remove
		rm(dst)

	cp = shutil.copytree if os.path.isdir(src) else shutil.copyfile
	cp(src, dst)

	update_index_js()

	if link_type == 'symbolic':
		contents_path = 'contents'
		os.symlink(fs.refdir('contents'), os.path.join(dst, 'contents'))
	elif link_type == 'relative':
		contents_path = '../contents'
	else:
		raise RuntimeError('unknown path type')

	index.main(full=True)

	with open(os.path.join(dst, 'constants.js'), 'w', encoding='utf-8') as f:
		f.write(declare_js_string_constant('hostname', config['host-name']))
		f.write(declare_js_string_constant('contentsPath', contents_path))

	print(f'installed site into {dst}')

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