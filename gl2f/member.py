table = {
	'yuzuha': {
		'group': ['girls2'],
		'fullname': '小田柚葉',
		'color':{'girls2': {'foreground': [255, 255, 255], 'background': [0, 190, 243]}},
		'categoryId': '271548290024080549'
	},
	'momoka': {
		'group': ['girls2'],
		'fullname': '隅谷百花',
		'color':{'girls2': {'foreground': [255, 255, 255], 'background': [31, 82, 209]}},
		'categoryId': '271548304888693925'
	},
	'misaki': {
		'group': ['girls2'],
		'fullname': '鶴屋美咲',
		'color':{'girls2': {'foreground': [255, 255, 255], 'background': [247, 117, 0]}},
		'categoryId': '271548319161909900'
	},
	'youka': {
		'group': ['girls2'],
		'fullname': '小川桜花',
		'color':{'girls2': {'foreground': [255, 255, 255], 'background': [119, 52, 196]}},
		'categoryId': '271548334819247269'
	},
	'kurea': {
		'group': ['girls2'],
		'fullname': '増田來亜',
		'color':{'girls2': {'foreground': [255, 255, 255], 'background': [157, 157, 157]}},
		'categoryId': '271548349729997452'
	},
	'minami': {
		'group': ['girls2'],
		'fullname': '菱田未渚美',
		'color':{'girls2': {'foreground': [255, 255, 255], 'background': [255, 80, 159]}},
		'categoryId': '271548364363924645'
	},
	'kira': {
		'group': ['girls2'],
		'fullname': '山口綺羅',
		'color':{'girls2': {'foreground': [255, 255, 255], 'background': [229, 182, 15]}},
		'categoryId': '271548377827639948'
	},
	'toa': {
		'group': ['girls2'],
		'fullname': '原田都愛',
		'color':{'girls2': {'foreground': [255, 255, 255], 'background': [32, 203, 115]}},
		'categoryId': '271548392222491813'
	},
	'ran': {
		'group': ['girls2'],
		'fullname': '石井蘭',
		'color':{'girls2': {'foreground': [255, 255, 255], 'background': [255, 46, 46]}},
		'categoryId': '271548406038528652'
	},

	'miyu': {
		'group': ['lovely2'],
		'fullname': '渡辺未優',
		'color':{'lovely2': {'foreground': [255, 255, 255], 'background': [243, 111, 163]}},
		'categoryId': '436713148108505915'
	},
	'yui': {
		'group': ['lovely2'],
		'fullname': '山下結衣',
		'color':{'lovely2': {'foreground': [255, 255, 255], 'background': [95, 189, 225]}},
		'categoryId': '436714399051285307'
	},

	'rina': {
		'group': ['lucky2', 'lovely2'],
		'fullname': '山口莉愛',
		'color':{
			'lucky2': {'foreground': [255, 255, 255], 'background': [0, 190, 243]},
			'lovely2': {'foreground': [255, 255, 255], 'background': [119, 52, 196]}
		},
		'categoryId': '436713912444912481'
	},
	'yura': {
		'group': ['lucky2', 'lovely2'],
		'fullname': '杉浦優來',
		'color':{
			'lucky2': {'foreground': [255, 255, 255], 'background': [31, 82, 209]},
			'lovely2': {'foreground': [255, 255, 255], 'background': [247, 117, 0]}
		},
		'categoryId': '443306956518589243'
	},

	'tsubaki': {
		'group': ['lucky2'],
		'fullname': '永山椿',
		'color':{'lucky2': {'foreground': [255, 255, 255], 'background': [31, 82, 209]}},
		'categoryId': '540078282813473595'
	},
	'hiro': {
		'group': ['lucky2'],
		'fullname': '深澤日彩',
		'color':{'lucky2': {'foreground': [255, 255, 255], 'background': [119, 52, 196]}},
		'categoryId': '540080651374691131'
	},
	'yuwa': {
		'group': ['lucky2'],
		'fullname': '比嘉優和',
		'color':{'lucky2': {'foreground': [255, 255, 255], 'background': [255, 80, 159]}},
		'categoryId': '540080829989127105'
	},
	'kanna': {
		'group': ['lucky2'],
		'fullname': '佐藤栞奈',
		'color':{'lucky2': {'foreground': [255, 255, 255], 'background': [157, 157, 157]}},
		'categoryId': '540081291836523457'
	},
	'ririka': {
		'group': ['lucky2'],
		'fullname': '上村梨々香',
		'color':{'lucky2': {'foreground': [255, 255, 255], 'background': [229, 182, 15]}},
		'categoryId': '661170107531133993'
	},
	'akari': {
		'group': ['lucky2'],
		'fullname': '森朱里',
		'color':{'lucky2': {'foreground': [255, 255, 255], 'background': [32, 203, 115]}},
		'categoryId': '661169466536625193'
	},
	'kiki': {
		'group': ['lucky2'],
		'fullname': '佐藤妃希',
		'color':{'lucky2': {'foreground': [255, 255, 255], 'background': [255, 46, 46]}},
		'categoryId': '661168410020807520'
	},

	'lovely2staff': {
		'group' : [],
		'fullname': "スタッフ",
		'color':{'lovely2': {'foreground': [255, 255, 255], 'background': [157, 157, 157]}},
		'categoryId': "436714547944883137",
	}
}


def is_group(group):
	return group in {'girls2', 'lovely2', 'lucky2'}

def is_member(member):
	return member in table.keys()


def belongs_to(member, group=None):
	if group:
		return group in table[member]['group']
	else:
		return table[member]['group']


def full_name(name):
	return table[name]['fullname']


def from_id(i):
	for k, v in table.items():
		if v['categoryId'] == i:
			return k, v

def id_to_name(i):
	for k, v in table.items():
		if v['categoryId'] == i:
			return k
	print('not found')


def name_width():
	return max(len(i['fullname']) for i in table.values())


if __name__ == '__main__':
	assert is_group('yuzuha') == False
	assert is_group('girls2') == True

	assert is_member('miyu') == True
	assert is_member('lovely2') == False


	assert belongs_to('miyu') == ['lovely2']
	assert belongs_to('rina') == ['lucky2', 'lovely2']

	assert belongs_to('yui', 'lovely2') == True
	assert belongs_to('yura', 'lovely2') == True
	assert belongs_to('yura', 'lucky2') == True
	assert belongs_to('yura', 'girls2') == False


	assert full_name('momoka') == '隅谷百花'