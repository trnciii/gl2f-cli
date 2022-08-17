import argparse
from .util import member
from .ls import Lister, make_main


def core(args):
	lister = Lister('news', debug=args.dump_response)
	return lister.list_group(args.name, args.number, args.page, args.order)


main = make_main(core)