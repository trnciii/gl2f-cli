def to_group(i):
	return {
		'271474317252887717': 'girls2',
		'436708526618837819': 'lovely2',
		'540071536506176315': 'lucky2',

		'455630760846558145': 'girls2',
		'540071136604455739': 'lucky2',
	}[i]


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


def pagenames():
	return {
		'271474317252887717': 'blogs',
		'436708526618837819': 'lovely2blogs',
		'540071536506176315': 'lucky2blogs',

		'540067120025699131': 'familyNews',
		'270441012457899173': 'news',
		'415001844964656065': 'lovely2news',
		'540071356465677115': 'lucky2news',

		'455630760846558145': 'girls2radio',
		'540071136604455739': 'lucky2radio',

		'689409591506633568': 'ShangrilaPG',
	}


def content_url(item):
	page = pagenames()[item['boardId']]
	content = item['contentId']
	return f'https://girls2-fc.jp/page/{page}/{content}'
