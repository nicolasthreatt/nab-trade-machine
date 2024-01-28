from trade_simulation import evaluate_trade
from helpers.cli import parse_args

if __name__ == "__main__":
    args = parse_args()

    pre_trade_teams, post_trade_teams = evaluate_trade(args.season, args.players, args.src_teams, args.dest_teams)
    if args.plot:
        generate_trade_plots(args.plot, pre_trade_teams, post_trade_teams)
