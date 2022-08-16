def from_id(i):
	return {
		'271474317252887717': 'https://girls2-fc.jp/page/blogs',
		'436708526618837819': 'https://girls2-fc.jp/page/lovely2blogs',
		'540071536506176315': 'https://girls2-fc.jp/page/lucky2blogs',

		'540067120025699131': 'https://girls2-fc.jp/page/familyNews',
		'270441012457899173': 'https://girls2-fc.jp/page/news',
		'415001844964656065': 'https://girls2-fc.jp/page/lovely2news',
		'540071356465677115': 'https://girls2-fc.jp/page/lucky2news',

		'455630760846558145': 'https://girls2-fc.jp/page/girls2Radio',
		'540071136604455739': 'https://girls2-fc.jp/page/lucky2radio',
	}[i]

def to_group(i):
	return {
		'271474317252887717': 'girls2',
		'436708526618837819': 'lovely2',
		'540071536506176315': 'lucky2',

		# '540067120025699131': 'family',
		# '270441012457899173': 'girls2',
		# '415001844964656065': 'lovely2',
		# '540071356465677115': 'lucky2',

		'455630760846558145': 'girls2',
		'540071136604455739': 'lucky2',
	}[i]


def request_url(domain, group):
	return {
		'blog':{
			'girls2': 'https://api.fensi.plus/v1/sites/girls2-fc/texts/271474317252887717/contents',
			'lovely2': 'https://api.fensi.plus/v1/sites/girls2-fc/texts/436708526618837819/contents',
			'lucky2': 'https://api.fensi.plus/v1/sites/girls2-fc/texts/lucky2Blogs/contents'
		},
		'news': {
			'family': 'https://api.fensi.plus/v1/sites/girls2-fc/news/familyNews/contents',
			'girls2': 'https://api.fensi.plus/v1/sites/girls2-fc/news/270441012457899173/contents',
			'lovely2': 'https://api.fensi.plus/v1/sites/girls2-fc/news/415001844964656065/contents',
			'lucky2': 'https://api.fensi.plus/v1/sites/girls2-fc/news/lucky2News/contents'
		},
		'radio': {
			'girls2': 'https://api.fensi.plus/v1/sites/girls2-fc/texts/girls2Radio/contents',
			'lucky2': 'https://api.fensi.plus/v1/sites/girls2-fc/texts/lucky2Radio/contents'
		}
	}[domain][group]


if __name__ == '__main__':
	boardId = [
		'271474317252887717',
		'436708526618837819',
		'540071536506176315',
		'540067120025699131',
		'270441012457899173',
		'415001844964656065',
		'540071356465677115',
		'455630760846558145',
		'540071136604455739',
	]

	for i in boardId:
		print(from_id(i))


	print()
	for g in ['girls2', 'lovely2', 'lucky2']:
		print(request_url('blog', g))

	print()
	for g in ['girls2', 'lucky2']:
		print(request_url('radio', g))

	print()
	for g in ['family', 'girls2', 'lovely2', 'lucky2']:
		print(request_url('news', g))
