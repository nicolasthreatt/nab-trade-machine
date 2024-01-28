import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Command Line Argument Parser')

    parser.add_argument('--season', dest='season', type=str, metavar='', required=False, default='2019-20',
                        help="Teams' Season")

    parser.add_argument('--players', dest='players', nargs='+', type=str, metavar='', required=False, default=list(),
                        help="Player(s)")

    parser.add_argument('--src', dest='src_teams', nargs='+', type=str, metavar='', required=False, default=list(),
                        help="Abbreviated Origninal Player's Teams")

    parser.add_argument('--dest', dest='dest_teams', nargs='+', type=str, metavar='', required=False, default=list(),
                        help="Abbreviated Destination Trade Teams")

    parser.add_argument('--plot', dest='plot', nargs='?', type=str, metavar='', required=False, default='',
                        const='', choices=('bar', 'line', 'pie', 'compare', ''),
                        help='List of plot types')

    return parser.parse_args()
