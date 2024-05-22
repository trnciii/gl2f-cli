import os
from .core import lister, pretty, util, local
from .ayame import terminal as term

def build_body_embedded(item):
	from .core import article, auth

	boardId = item['boardId']
	contentId = item['contentId']
	xauth = auth.update(auth.load())

	def up(match):
		mediaId, t = match.groups()
		meta, _ = article.dl_medium(boardId, contentId, mediaId, head=True, xauth=xauth)
		url = meta['originalUrl'] if t == 'video' else meta['accessUrl']

		if t == 'image':
			return f'<img src="{url}"></img>'
		elif t == 'video':
			return f'<video controls autoplay muted loop src="{url}"></video>'
		else:
			return ''

	return article.ptn_media.sub(up, item['values']['body'])


def cached_url(item):
	from .core.local import site

	cache_dir = local.fs.refdir('cache')
	body = build_body_embedded(item)
	page_path = os.path.join(cache_dir, f'{item["contentId"]}.html')

	title = item['values']['title']
	author = item.get('category', {'name':''})['name']
	date = util.to_datetime(item['openingAt']).strftime('%Y/%m/%d')
	with open(local.fs.package_data('site/style.css')) as f:
		css = f.read()

	with open(page_path, 'w', encoding='utf-8') as f:
		f.write(f'''<style>
{css}
img, video{{
  display: block;
  margin: 8px auto;
  max-width: 100%;
  max-height: calc(100vh - 150px);
}}
.header-title{{
  width: 820px;
}}
/* Media query for narrow screens (adjust the max-width as needed) */
@media screen and (max-width: 960px) {{
  .blog-header {{
    flex-direction: column; /* Stack sections vertically on narrow screens */
    align-items: stretch; /* Stretch sections to full width */
  }}
  .header-title{{
    width: 100%; /* Take full width on narrow screens */
  }}
}}
</style>''')
		f.write(f'''<header class="blog-header">
  <nav id=links class="header-links"></nav>
  <div class="header-title">
    <h1>{title}</h1>
    {author}&nbsp;{date}&nbsp;
  </div>
</header>''')
		f.write(f'<main><div style="max-width:800px;margin:auto;">{body}</div></main>')

	return page_path

def open_url(item, cached=False):
	import webbrowser
	from .core import board
	webbrowser.register("termux-open '%s'", None)

	if cached:
		webbrowser.open(cached_url(item), new=0, autoraise=True)
	else:
		webbrowser.open(board.content_url(item), new=0, autoraise=True)


def subcommand(args):
	items = lister.list_contents(args)
	fm = pretty.from_args(args, items)

	if args.all:
		for i in items:
			fm.print(i)
			open_url(i, args.cached)
	elif args.pick:
		for i in util.pick(items, args.pick):
			fm.print(i)
			open_url(i, args.cached)
	else:
		for i in term.selected(items, fm.format):
			open_url(i, args.cached)

def add_to():
	return 'gl2f', 'open'

def add_args(parser):
	parser.description = 'Open pages in the browser'

	lister.add_args(parser)
	pretty.add_args(parser)
	parser.set_defaults(format='author:title')
	parser.add_argument('-a', '--all', action='store_true',
		help='open all items')
	parser.add_argument('--cached', action='store_true',
		help='download and open the local file')
	parser.add_argument('--pick', type=int, nargs='+',
		help='select articles to show')

	parser.set_defaults(handler=subcommand)

def set_compreply():
	return '__gl2f_complete_list_args'
