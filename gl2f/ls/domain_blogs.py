name = 'blog'

def request_url(group):
	url = {
		'girls2': 'https://api.fensi.plus/v1/sites/girls2-fc/texts/271474317252887717/contents',
		'lovely2': 'https://api.fensi.plus/v1/sites/girls2-fc/texts/436708526618837819/contents',
		'lucky2': 'https://api.fensi.plus/v1/sites/girls2-fc/texts/lucky2Blogs/contents'
	}
	return url[group]


def contents_url(group):
	url = {
		'girls2': 'https://girls2-fc.jp/page/blogs',
		'lovely2': 'https://girls2-fc.jp/page/lovely2blogs',
		'lucky2': 'https://girls2-fc.jp/page/lucky2blogs',
	}
	return url[group]