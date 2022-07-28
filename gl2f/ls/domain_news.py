name = 'radio'

def request_url(group):
	url = {
		'family': 'https://api.fensi.plus/v1/sites/girls2-fc/news/familyNews/contents',
		'girls2': 'https://api.fensi.plus/v1/sites/girls2-fc/news/270441012457899173/contents',
		'lovely2': 'https://api.fensi.plus/v1/sites/girls2-fc/news/415001844964656065/contents',
		'lucky2': 'https://api.fensi.plus/v1/sites/girls2-fc/news/lucky2News/contents'
	}
	return url[group]


def contents_url(group):
	url = {
		'family': 'https://girls2-fc.jp/page/familyNews',
		'girls2': 'https://girls2-fc.jp/page/news',
		'lovely2': 'https://girls2-fc.jp/page/lovely2news',
		'lucky2': 'https://girls2-fc.jp/page/lucky2news',
	}
	return url[group]
