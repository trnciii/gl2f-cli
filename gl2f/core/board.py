def get():
	return {
		# blogs
		'271474317252887717': {
			'group': 'girls2',
			'kind': 'blogs',
			'page': 'blogs',
		},

		'436708526618837819': {
			'group': 'lovely2',
			'kind': 'blogs',
			'page': 'lovely2blogs',
		},

		'540071536506176315': {
			'group': 'lucky2',
			'kind': 'blogs',
			'page': 'lucky2blogs',
		},

		# news
		'540067120025699131': {
			'kind': 'news',
			'page': 'familyNews',
		},

		'270441012457899173': {
			'group': 'girls2',
			'kind': 'news',
			'page': 'news',
		},

		'415001844964656065': {
			'group': 'lovely2',
			'kind': 'news',
			'page': 'lovely2news',
		},
		'540071356465677115': {
			'group': 'lucky2',
			'kind': 'news',
			'page': 'lucky2news',
		},

		# radio
		'455630760846558145': {
			'group': 'girls2',
			'kind': 'radio',
			'page': 'girls2radio',
		},

		'540071136604455739': {
			'group': 'lucky2',
			'kind': 'radio',
			'page': 'lucky2radio',
		},

		# gtube
		'270809837141492901': {
			'page': 'gtube',
		},

		# Shangri-la Photo Gallery
		'689409591506633568': {
			'page': 'ShangrilaPG',
		},
	}


def blogs(key):
	return {
		'girls2': '271474317252887717',
		'lovely2': '436708526618837819',
		'lucky2': '540071536506176315'
	}[key]

def news(key):
	return {
		'family': '540067120025699131',
		'girls2': '270441012457899173',
		'lovely2': '415001844964656065',
		'lucky2': '540071356465677115'
	}[key]

def radio(key):
	return{
		'girls2': '455630760846558145',
		'lucky2': '540071136604455739'
	}[key]


def content_url(item):
	page = get()[item['boardId']]['page']
	content = item['contentId']
	return f'https://girls2-fc.jp/page/{page}/{content}'
