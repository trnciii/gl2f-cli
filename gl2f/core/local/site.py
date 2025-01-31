import os
import re, json
from .. import util
from ..config import data as config
from . import fs, content, index


def update_site(full=False):
	site = fs.refdir_untouch('site')
	if not site:
		return 'site is not installed'

	index.main(full=full)

	table_code = f'const table={util.read_all_text(index.get_path())}'
	util.write_all_text(os.path.join(site, 'index.js'), table_code)


def install():
	import shutil

	src = fs.package_data('site')
	dst = fs.refdir('site')

	shutil.copytree(src, dst, dirs_exist_ok=True)

	site_contents = os.path.join(dst, 'contents')
	if os.path.isdir(site_contents):
		os.remove(site_contents)
	os.symlink(fs.refdir('contents'), site_contents)

	const_code = f'const hostname="{config["host-name"]}";'
	util.write_all_text(os.path.join(dst, 'constants.js'), const_code)

	update_site()


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

	install()

	class Handler(http.server.SimpleHTTPRequestHandler):
		def __init__(self, *args, **kwargs):
			super().__init__(*args, directory=fs.refdir('site'), **kwargs)

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
