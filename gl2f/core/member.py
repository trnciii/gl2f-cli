def default():
	G2_members = [
		{ 'id': 'yuzuha',
			'categoryId': '271548290024080549',
			'fullname': '小田柚葉',
			'foreground': [255, 255, 255], 'background': [0, 190, 243]},
		{ 'id': 'momoka',
			'categoryId': '271548304888693925',
			'fullname': '隅谷百花',
			'foreground': [255, 255, 255], 'background': [31, 82, 209]},
		{ 'id': 'misaki',
			'categoryId': '271548319161909900',
			'fullname': '鶴屋美咲',
			'foreground': [255, 255, 255], 'background': [247, 117, 0]},
		{ 'id': 'youka',
			'categoryId': '271548334819247269',
			'fullname': '小川桜花',
			'foreground': [255, 255, 255], 'background': [119, 52, 196]},
		{ 'id': 'kurea',
			'categoryId': '271548349729997452',
			'fullname': '増田來亜',
			'foreground': [255, 255, 255], 'background': [157, 157, 157]},
		{ 'id': 'minami',
			'categoryId': '271548364363924645',
			'fullname': '菱田未渚美',
			'foreground': [255, 255, 255], 'background': [255, 80, 159]},
		{ 'id': 'kira',
			'categoryId': '271548377827639948',
			'fullname': '山口綺羅',
			'foreground': [255, 255, 255], 'background': [229, 182, 15]},
		{ 'id': 'toa',
			'categoryId': '271548392222491813',
			'fullname': '原田都愛',
			'foreground': [255, 255, 255], 'background': [32, 203, 115]},
		{ 'id': 'ran',
			'categoryId': '271548406038528652',
			'fullname': '石井蘭',
			'foreground': [255, 255, 255], 'background': [255, 46, 46]},
	]
	G2_pages = ['271474317252887717', '455630760846558145']
	yield from _add_by_product(G2_members, G2_pages, 'girls2')

	L2_members = [
		{ 'id': 'rina',
			'categoryId': '436713912444912481',
			'fullname': '山口莉愛',
			'foreground': [255, 255, 255], 'background': [119, 52, 196]},
		{ 'id': 'yura',
			'categoryId': '443306956518589243',
			'fullname': '杉浦優來',
			'foreground': [255, 255, 255], 'background': [157, 157, 157]},
		{ 'id': 'hiro',
			'categoryId': '540080651374691131',
			'fullname': '深澤日彩',
			'foreground': [255, 255, 255], 'background': [0, 190, 243]},
		{ 'id': 'yuwa',
			'categoryId': '540080829989127105',
			'fullname': '比嘉優和',
			'foreground': [255, 255, 255], 'background': [255, 46, 46]},
		{ 'id': 'kanna',
			'categoryId': '540081291836523457',
			'fullname': '佐藤栞奈',
			'foreground': [255, 255, 255], 'background': [31, 82, 209]},
		{ 'id': 'ririka',
			'categoryId': '661170107531133993',
			'fullname': '上村梨々香',
			'foreground': [255, 255, 255], 'background': [255, 80, 159]},
		{ 'id': 'akari',
			'categoryId': '661169466536625193',
			'fullname': '森朱里',
			'foreground': [255, 255, 255], 'background': [32, 203, 115]},
		{ 'id': 'kiki',
			'categoryId': '661168410020807520',
			'fullname': '佐藤妃希',
			'foreground': [255, 255, 255], 'background': [229, 182, 15]},
	]
	L2_pages = ['540071536506176315', '540071136604455739']
	yield from _add_by_product(L2_members, L2_pages, 'lucky2')
	yield {
		'boardId': '540071536506176315',
		'categoryId': '540078282813473595',
		'id': 'tsubaki',
		'fullname': '永山椿',
		'group': 'lucky2',
		'foreground': [255, 255, 255], 'background': [247, 117, 0]
	}
	yield {
		'boardId': '540071136604455739',
		'categoryId': '562927300052517691',
		'id': 'tsubaki',
		'fullname': '永山椿',
		'group': 'lucky2',
		'foreground': [255, 255, 255], 'background': [247, 117, 0]
	}

	l2_members = [
		{ 'id': 'miyu',
			'categoryId': '436713148108505915',
			'fullname': '渡辺未優',
			'foreground': [255, 255, 255], 'background': [243, 111, 163]},
		{ 'id': 'rina',
			'categoryId': '436713912444912481',
			'fullname': '山口莉愛',
			'foreground': [255, 255, 255], 'background': [119, 52, 196]},
		{ 'id': 'yui',
			'categoryId': '436714399051285307',
			'fullname': '山下結衣',
			'foreground': [255, 255, 255], 'background': [95, 189, 225]},
		{ 'id': 'yura',
			'categoryId': '443306956518589243',
			'fullname': '杉浦優來',
			'foreground': [255, 255, 255], 'background': [247, 117, 0]},
		{ 'id': 'lovely2staff',
			'categoryId': '436714547944883137',
			'fullname': 'スタッフ',
			'foreground': [255, 255, 255], 'background': [157, 157, 157]}
	]
	l2_pages = ['436708526618837819']
	yield from _add_by_product(l2_members, l2_pages, 'lovely2')

def _add_by_product(members, pages, group):
	import itertools
	for c, b in itertools.product(members, pages):
		yield c | {'boardId': b, 'group': group}
