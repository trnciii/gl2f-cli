table = {
	'yuzuha':  {'group': ['girls2'],           'fullname': '小田柚葉'},
	'momoka':  {'group': ['girls2'],           'fullname': '隅谷百花'},
	'misaki':  {'group': ['girls2'],           'fullname': '鶴屋美咲'},
	'youka':   {'group': ['girls2'],           'fullname': '小川桜花'},
	'kurea':   {'group': ['girls2'],           'fullname': '増田來亜'},
	'minami':  {'group': ['girls2'],           'fullname': '菱田未渚美'},
	'kira':    {'group': ['girls2'],           'fullname': '山口綺羅'},
	'toa':     {'group': ['girls2'],           'fullname': '原田都愛'},
	'ran':     {'group': ['girls2'],           'fullname': '石井蘭'},

	'miyu':    {'group': ['lovely2'],          'fullname': '渡辺未優'},
	'yui':     {'group': ['lovely2'],          'fullname': '山下結衣'},

	'rina':    {'group': ['lucky2', 'lovely2'], 'fullname': '山口莉愛'},
	'yura':    {'group': ['lucky2', 'lovely2'], 'fullname': '杉浦優來'},

	'tsubaki': {'group': ['lucky2'],           'fullname': '永山椿'},
	'hiro':    {'group': ['lucky2'],           'fullname': '深澤日彩'},
	'yuwa':    {'group': ['lucky2'],           'fullname': '比嘉優和'},
	'kanna':   {'group': ['lucky2'],           'fullname': '佐藤栞奈'},
	'ririka':  {'group': ['lucky2'],           'fullname': '上村梨々香'},
	'akari':   {'group': ['lucky2'],           'fullname': '森朱里'},
	'kiki':    {'group': ['lucky2'],           'fullname': '佐藤妃希'},
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