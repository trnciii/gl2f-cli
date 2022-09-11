import requests
from .. import auth
from . import board, member
from .date import is_today
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


def blogs(args):
	if member.is_group(args.name):
		boardId = board.blogs(args.name)
		return fetch(boardId, args.number, args.page, args.order, dump=args.dump)['list']

	elif member.is_member(args.name):
		boardId, categoryId = get_IDs('blog', args)
		return fetch(boardId, args.number, args.page, args.order, categoryId=categoryId, dump=args.dump)['list']

	elif args.name == 'today':
		return list(filter(
			lambda i: is_today(i['openingAt']),
			sum((fetch(board.blogs(group), size=10, page=1, dump=args.dump)['list'] for group in ['girls2', 'lucky2']), [])
		))


def news(args):
	if args.name == 'today':
		return list(filter(
			lambda i: is_today(i['openingAt']),
			fetch(board.news('family'), size=10, page=1, dump=args.dump)['list']
		))

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


def make_simple_lister(boardId):
	if isinstance(boardId, str):
		return lambda args: fetch(boardId, args.number, args.page, args.order, dump=args.dump)['list']
	else:
		return lambda args: fetch(boardId[args.name], args.number, args.page, args.order, dump=args.dump)['list']


def listers():
	return {
		'blogs': blogs,
		'radio': radio,
		'news': news,
		'gtube': make_simple_lister('270809837141492901'),
		'cm': make_simple_lister('504468501197489089'),
		'shangrila': make_simple_lister('689409591506633568'),
		'brandnewworld': make_simple_lister({'photo': '664746725843403713', 'cheer': '666819802651689824'}),
		'daijoubu': make_simple_lister({'photo': '660050132594590761', 'cheer': '653506325782725569'}),
		'cl': make_simple_lister('639636551948567355'),
		'fm': make_simple_lister({'girls2': '613606146413953985', 'lucky2': '613607790937637825'}),
		'enjoythegooddays': make_simple_lister('558593359405384641'),
		'famitok': make_simple_lister({'girls2':'550521936032039739', 'lucky2': '550521867736187707'}),
		'lovely2live': make_simple_lister('527414639852520385'),
		'garugakulive': make_simple_lister('499846974107812667'),
		'chuwapane': make_simple_lister('357805845389509857'),
		'onlinelive2020': make_simple_lister('449506330521109545'),
	}


def add_args_boardwise(parser, cmd):
	subparsers = parser.add_subparsers()
	for k in listers().keys():
		cmd.add_args(subparsers.add_parser(k), k)