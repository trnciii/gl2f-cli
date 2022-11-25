def get():
	return {
		# blogs
		'271474317252887717': {
			'group': 'girls2',
			'page': 'blogs',
		},

		'436708526618837819': {
			'group': 'lovely2',
			'page': 'lovely2blogs',
		},

		'540071536506176315': {
			'group': 'lucky2',
			'page': 'lucky2blogs',
		},

		# news
		'540067120025699131': {
			'page': 'familyNews',
		},

		'270441012457899173': {
			'group': 'girls2',
			'page': 'news',
		},

		'415001844964656065': {
			'group': 'lovely2',
			'page': 'lovely2news',
		},
		'540071356465677115': {
			'group': 'lucky2',
			'page': 'lucky2news',
		},

		'270810062216233612': {
			'group': 'mirage2',
			'page': 'mirage2news',
		},

		# radio
		'455630760846558145': {
			'group': 'girls2',
			'page': 'girls2radio',
		},

		'540071136604455739': {
			'group': 'lucky2',
			'page': 'lucky2radio',
		},

		# gtube
		'270809837141492901': {
			'page': 'gtube',
		},

		# commercial movie
		'504468501197489089':{
			'page': 'commercialmovie',
		},


		'297314731440473169':{
			'page': 'others',
		},

		# Shangri-la
		'689409591506633568': {
			'page': 'ShangrilaPG',
		},

		# Brand New World!
		'666819802651689824':{
			'page': 'FirstLiveCheerForL2',
		},

		'664746725843403713':{
			'page': 'Lucky2FirstLivePG',
		},

		# daijoubu
		'660050132594590761':{
			'page': '3rdAnnivPG',
		},

		'653506325782725569':{
			'page': '3rdAnnivCheerForG2',
		},

		# CL special live
		'639636551948567355':{
			'page': 'CLsplivepg',
		},

		# fan meeting
		'613606146413953985':{
			'group': 'girls2',
			'page': 'G2fcmeetingpg',
		},

		'613607790937637825':{
			'group': 'lucky2',
			'page': 'L2fcmeetingpg',
		},

		# enjoy the good days
		'558593359405384641':{
			'group': 'girls2',
			'page': 'EnjoyTheGoodDaysBackstage',
		},

		# famitok
		'550521936032039739':{
			'group': 'girls2',
			'page': 'Girls2famitok',
		},

		'550521867736187707':{
			'group': 'lucky2',
			'page': 'Lucky2famitok',
		},

		# lovely2 special live
		'527414639852520385':{
			'page': 'lovely2Live2021Diary',
		},

		# garugaku live
		'499846974107812667':{
			'page': 'garugakuliveDiary',
		},

		# chuwapane
		'357805845389509857':{
			'page': 'chuwapaneDiary',
		},

		# onlinelive
		'449506330521109545':{
			'page': 'onlineliveDiary',
		},

		# wallpaper
		'516921408022905897':{
			'page': 'wallpaper'
		},
	}


def from_page(p):
	return {v['page']:k for k, v in get().items()}[p]


def blogs(key):
	return {
		'girls2': from_page('blogs'),
		'lovely2': from_page('lovely2blogs'),
		'lucky2': from_page('lucky2blogs')
	}[key]

def news(key):
	return {
		'family': from_page('familyNews'),
		'girls2': from_page('news'),
		'lovely2': from_page('lovely2news'),
		'lucky2': from_page('lucky2news'),
		'mirage2': from_page('mirage2news'),
	}[key]

def radio(key):
	return{
		'girls2': from_page('girls2radio'),
		'lucky2': from_page('lucky2radio'),
	}[key]


def content_url(item):
	page = get()[item['boardId']]['page']
	content = item['contentId']
	return f'https://girls2-fc.jp/page/{page}/{content}'
