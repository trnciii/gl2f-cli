name = 'radio'

def request_url(group):
	url = {
		'girls2': 'https://api.fensi.plus/v1/sites/girls2-fc/texts/girls2Radio/contents',
		'lucky2': 'https://api.fensi.plus/v1/sites/girls2-fc/texts/lucky2Radio/contents'
	}
	return url[group]


def contents_url(group):
	url = {
		'girls2': 'https://girls2-fc.jp/page/girls2Radio',
		'lucky2': 'https://girls2-fc.jp/page/lucky2radio',
	}
	return url[group]
