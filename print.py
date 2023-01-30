import sys
from sys import stdout


c = sys.argv[sys.argv.index('--encoding')+1] if '--encoding' in sys.argv else sys.stdout.encoding

print(sys.stdout.encoding, flush=True)

def print_with_encoding(*ss, end='\n', sep=' ', errors='replace'):
	stdout.buffer.write((sep.join(ss)+end).encode(c, errors=errors))

s = '''
原田都愛 🦆🦆🦆🦆🦆🦆🦆🦆🦆🦆🦆🦆🦆🦆🦆 https://girls2-fc.jp/page/blogs/305718498280080541
原田都愛 🥳🥳🥳🥳🥳                     https://girls2-fc.jp/page/blogs/296237525440136273
原田都愛 🥲😄                           https://girls2-fc.jp/page/blogs/571710357186282433
原田都愛 🥲                             https://girls2-fc.jp/page/blogs/567537622214247465
原田都愛 🥦                             https://girls2-fc.jp/page/blogs/505608708496032705
原田都愛 🤪🤪🤪🤪🤪🤪🤪                 https://girls2-fc.jp/page/blogs/526227849607119675
原田都愛 🤔🤔🤔🤔🤔🤔                   https://girls2-fc.jp/page/blogs/304428618660971677
原田都愛 🟦                             https://girls2-fc.jp/page/blogs/590320261769724865
原田都愛 🟦                             https://girls2-fc.jp/page/blogs/531432161908097851
原田都愛 🟥                             https://girls2-fc.jp/page/blogs/661038676481934273
'''

print_with_encoding(s, s)
