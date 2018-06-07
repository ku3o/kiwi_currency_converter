from optparse import OptionParser
from json     import dumps as json_dumps

from app.core.manager import convert 
from app.app          import create_app


def get_cmd_args():
    parser = OptionParser()

    parser.set_defaults(dst_cur = None)

    parser.add_option('--amount', action = 'store',
                                  type   = 'float',
                                  dest   = 'amount',
                                  help   = 'amount which we want to convert - float')

    parser.add_option('--input_currency', action = 'store',
                                          type   = 'string',
                                          dest   = 'src_cur',
                                          help   = 'input currency - 3 letters name or currency symbol')

    parser.add_option('--output_currency', action = 'store',
                                           type   = 'string',
                                           dest   = 'dst_cur',
                                           help   = 'requested/output currency - 3 letters name or currency symbol')
    return parser.parse_args()


def main():
    try:
        (options, args) = get_cmd_args()

        app = create_app('../configs/development.py')

        with app.app_context():
            print(json_dumps(convert(options.src_cur,
                                     options.dst_cur,
                                     options.amount),
                             indent    = 4,
                             sort_keys = True))
        return 0

    except Exception as e:
        print(str(e))
        return 1


if __name__ == '__main__':
    exit(main())
