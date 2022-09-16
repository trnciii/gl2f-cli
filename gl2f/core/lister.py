import requests
from .. import auth
from . import board, member
from .date import in24h
import datetime, os, json


def fetch(boardId, size, page, order='reservedAt:desc', categoryId=None, template='texts', dump=False):
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
			'x-authorization': auth.update(auth.load()),
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
		with open(path, 'w') as f:
			json.dump(response.json(), f, indent=2)
		print('saved', path)

	return response.json()


def list_multiple_boards(boardId, args):
	# only returns the 'list' value of boards.
	# category id and template are fixed.
	from concurrent.futures import ThreadPoolExecutor

	with ThreadPoolExecutor() as executor:
		futures = [executor.submit(fetch, i, 10, 1, dump=args.dump) for i in boardId]

	return sum((f.result()['list'] for f in futures), [])


def get_IDs(domain, args):
	data = member.get()[args.name]
	group_list = data['group']
	group = args.group if args.group in group_list else group_list[0]

	if domain == 'blog':
		return board.blogs(group), data['categoryId'][domain]
	elif domain == 'radio':
		return board.radio(group), data['categoryId'][domain]


def add_args(parser):
	parser.add_argument('name', type=str, nargs='?',
		help='group or member name')

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


def blogs(args):
	if member.is_group(args.name):
		boardId = board.blogs(args.name)
		return fetch(boardId, args.number, args.page, args.order, dump=args.dump)['list']

	elif member.is_member(args.name):
		boardId, categoryId = get_IDs('blog', args)
		return fetch(boardId, args.number, args.page, args.order, categoryId=categoryId, dump=args.dump)['list']

	elif args.name == 'today':
		return filter_today(list_multiple_boards([board.blogs(i) for i in ['girls2', 'lucky2']], args))


def news(args):
	if args.name == 'today':
		return filter_today(fetch(board.news('family'), size=10, page=1, dump=args.dump)['list'])

	else:
		boardId = board.news(args.name)
		return fetch(boardId, args.number, args.page, args.order, dump=args.dump)['list']


def radio(args):
	if member.is_group(args.name):
		boardId = board.radio(args.name)
		return fetch(boardId, args.number, args.page, args.order, dump=args.dump)['list']

	elif member.is_member(args.name):
		boardId, categoryId = get_IDs('radio', args)
		return fetch(boardId, args.number, args.page, args.order, categoryId=categoryId, dump=args.dump)['list']


def make_simple_lister(page):
	if isinstance(page, str):
		boardId = board.from_page(page)
		return lambda args: fetch(boardId, args.number, args.page, args.order, dump=args.dump)['list']
	else:
		boardId = {k:board.from_page(v) for k, v in page.items()}
		return lambda args: fetch(boardId[args.name], args.number, args.page, args.order, dump=args.dump)['list']


def today(args):
	boardId = [
		board.blogs('girls2'),
		board.blogs('lucky2'),
		board.news('family'),
		board.radio('girls2'),
		board.radio('lucky2'),
		board.from_page('gtube'),
		board.from_page('commercialmovie'),
		board.from_page('ShangrilaPG')
	]
	ret = list_multiple_boards(boardId, args)
	return sorted(filter_today(ret), key=lambda i:i['openingAt'], reverse=True)



def listers():
	return {
		'blogs': blogs,
		'radio': radio,
		'news': news,
		'gtube': make_simple_lister('gtube'),
		'cm': make_simple_lister('commercialmovie'),
		'shangrila': make_simple_lister('ShangrilaPG'),
		'brandnewworld': make_simple_lister({'photo': 'Lucky2FirstLivePG', 'cheer': 'FirstLiveCheerForL2'}),
		'daijoubu': make_simple_lister({'photo': '3rdAnnivPG', 'cheer': '3rdAnnivCheerForG2'}),
		'cl': make_simple_lister('CLsplivepg'),
		'fm': make_simple_lister({'girls2': 'G2fcmeetingpg', 'lucky2': 'L2fcmeetingpg'}),
		'enjoythegooddays': make_simple_lister('EnjoyTheGoodDaysBackstage'),
		'famitok': make_simple_lister({'girls2':'Girls2famitok', 'lucky2': 'Lucky2famitok'}),
		'lovely2live': make_simple_lister('lovely2Live2021Diary'),
		'garugakulive': make_simple_lister('garugakuliveDiary'),
		'chuwapane': make_simple_lister('chuwapaneDiary'),
		'onlinelive2020': make_simple_lister('onlineliveDiary'),
		'today': today,
	}


def add_args_boardwise(parser, cmd):
	subparsers = parser.add_subparsers()
	for k in listers().keys():
		cmd.add_args(subparsers.add_parser(k), k)