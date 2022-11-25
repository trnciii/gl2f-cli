import requests
from .. import auth
from . import board, member
from .date import in24h
import datetime, os, json


def fetch(boardId, size, page, order='reservedAt:desc', categoryId=None, template='texts', dump=False, xauth=None):
	response = requests.get(
		f'https://api.fensi.plus/v1/sites/girls2-fc/{template}/{boardId}/contents',
		params={
			'size': str(size),
			'page': str(page),
			'order': str(order),
			'categoryId': categoryId
		},
		cookies={},
		headers={
			'origin': 'https://girls2-fc.jp',
			'x-from': 'https://girls2-fc.jp',
			'x-authorization': xauth if xauth else auth.update(auth.load()),
		})

	if not response.ok:
		return

	if dump:
		filename = board.get()[boardId]['page']
		if categoryId:
			name, _ = member.from_id(categoryId)
			filename += f'-{name}'

		now = datetime.datetime.now().strftime('%y%m%d%H%M%S')

		path = os.path.join(dump,  f'{filename}-{now}.json')
		with open(path, 'w', encoding='utf-8') as f:
			json.dump(response.json(), f, indent=2, ensure_ascii=False)
		print('saved', path)

	return response.json()


def list_multiple_boards(boardId, args):
	# only returns the 'list' value of boards.
	# category id and template are fixed.
	from concurrent.futures import ThreadPoolExecutor

	xauth = auth.update(auth.load())
	with ThreadPoolExecutor() as executor:
		futures = [executor.submit(fetch, i, 10, 1, xauth=xauth, dump=args.dump) for i in boardId]

	return sum((f.result()['list'] for f in futures), [])


def get_IDs(domain, m, g):
	data = member.get()[m]
	group_list = data['group']
	group = g if g in group_list else group_list[0]

	if domain == 'blog':
		return board.blogs(group), data['categoryId'][domain]
	elif domain == 'radio':
		return board.radio(group), data['categoryId'][domain]


def add_args(parser):
	parser.add_argument('board', type=str,
		help='board and group or member name')

	parser.add_argument('-n', '--number', type=int, default=10,
		help='number of articles in [1, 99]')

	parser.add_argument('-p', '--page', type=int, default=1,
		help='page number')

	parser.add_argument('--order', type=str, default='reservedAt:desc',
		help='order. {reservedAt, name} × {asc, desc}. default = reservedAt:desc.')

	parser.add_argument('--group', type=str,
		help='specify group when name is a member.')

	parser.add_argument('--dump', type=str, nargs='?', const='.',
		help='dump response from server as ./response.json')


def filter_today(li):
	return list(filter(lambda i:in24h(i['openingAt']), li))


def listers(args):
	key, *sub = args.board.split('/')

	pages = {
		'gtube':'gtube',
		'cm':'commercialmovie',
		'others':'others',
		'shangrila':'ShangrilaPG',
		'cl':'CLsplivepg',
		'lovely2live':'lovely2Live2021Diary',
		'garugakulive':'garugakuliveDiary',
		'chuwapane':'chuwapaneDiary',
		'onlinelive2020':'onlineliveDiary',
		'enjoythegooddays':'EnjoyTheGoodDaysBackstage',
		'wallpaper': 'wallpaper',
		'brandnewworld':{
			'photo': 'Lucky2FirstLivePG',
			'cheer': 'FirstLiveCheerForL2'
		},
		'daijoubu':{
			'photo': '3rdAnnivPG',
			'cheer': '3rdAnnivCheerForG2'
		},
		'fm':{
			'girls2':'G2fcmeetingpg',
			'lucky2':'L2fcmeetingpg'
		},
		'famitok':{
			'girls2': 'Girls2famitok',
			'lucky2': 'Lucky2famitok'
		},
	}


	if key == 'blogs':
		skey = sub[0]
		if member.is_group(skey):
			boardId = board.blogs(skey)
			return fetch(boardId, args.number, args.page, args.order, dump=args.dump)['list']

		elif member.is_member(skey):
			boardId, categoryId = get_IDs('blog', skey, args.group)
			return fetch(boardId, args.number, args.page, args.order, categoryId=categoryId, dump=args.dump)['list']

		elif skey == 'today':
			return filter_today(list_multiple_boards([board.blogs(i) for i in ['girls2', 'lucky2']], args))


	elif key == 'radio':
		skey = sub[0]
		if member.is_group(skey):
			boardId = board.radio(skey)
			return fetch(boardId, args.number, args.page, args.order, dump=args.dump)['list']

		elif member.is_member(skey):
			boardId, categoryId = get_IDs('radio', skey, args.group)
			return fetch(boardId, args.number, args.page, args.order, categoryId=categoryId, dump=args.dump)['list']


	elif key == 'news':
		skey = sub[0]
		if skey == 'today':
			return filter_today(fetch(board.news('family'), size=10, page=1, dump=args.dump)['list'])

		else:
			boardId = board.news(skey)
			return fetch(boardId, args.number, args.page, args.order, dump=args.dump)['list']


	elif key == 'today':
		ret = list_multiple_boards([
			board.blogs('girls2'),
			board.blogs('lucky2'),
			board.news('family'),
			board.radio('girls2'),
			board.radio('lucky2'),
			board.from_page('gtube'),
			board.from_page('commercialmovie'),
			board.from_page('ShangrilaPG'),
			board.from_page('wallpaper'),
		], args)
		return sorted(filter_today(ret), key=lambda i:i['openingAt'], reverse=True)


	elif key in pages.keys():
		v = pages[key]
		if isinstance(v, dict):
			return fetch(
				board.from_page(v[sub[0]]),
				args.number, args.page, args.order, dump=args.dump
			)['list']
		else:
			return fetch(
				board.from_page(v),
				args.number, args.page, args.order, dump=args.dump
			)['list']

	else:
		print('key not found')
		return []
