import itertools
import matplotlib.pyplot as plt
import numpy as np
from helpers import plotting_utils as plotutils


def create_compare_trade_subplots(before_teams_to_contracts: dict, after_teams_to_contracts: dict) -> None:
    """Create subplots comparing trade details before and after.

    Args:
        before_teams_to_contracts (dict): Dictionary mapping teams to their contract details before the trade.
        after_teams_to_contracts (dict): Dictionary mapping teams to their contract details after the trade.
    """
    # Determine teams involved in both before and after trades
    teams = set(before_teams_to_contracts.keys()) & set(after_teams_to_contracts.keys())
    team_itr = itertools.cycle(teams)

    # Create subplots for each team's trade comparison
    fig, big_axes = plt.subplots(figsize=(15.0, 15.0), nrows=len(teams), ncols=2, sharey=True)
    fig.suptitle('Trade Recap', fontsize=12)

    # Set titles for each column in the subplot grid
    labels = ["Before", "After"]
    for ax, col in zip(big_axes[0], labels):
        ax.set_title(col)

    # Turn off tick marks for the right column of subplots
    for ax, col in zip(big_axes[:, 1], teams):
        plotutils.turn_off_tick_marks(ax)

    # Set team names as y-axis labels for the left column of subplots
    for ax, team in zip(big_axes[:, 0], teams):
        plotutils.turn_off_tick_marks(ax)
        ax.set_ylabel(team, rotation=0, size='large')

    # Keep count of numnber of subplots
    plot_count = 1

    # Began to create subplots for all teams involved in the trade
    for row in range(len(teams)):
        team = next(team_itr)
        # Only two subplot per row
        for col in range(2):
            # First column is for players and their contracts BEFORE the trade
            if col == 0:
                players_to_contracts = {player: contract[0] for player, contract in
                                        sorted(before_teams_to_contracts[team].players.items(),
                                               key=lambda item: item[1], reverse=True)}
                traded_players = set(before_teams_to_contracts[team].players.keys()).difference(
                    set(after_teams_to_contracts[team].players.keys()))
            # Any other column is for players and their contracts AFTER the trade   
            else:
                players_to_contracts = {player: contract[0] for player, contract in
                                        sorted(after_teams_to_contracts[team].players.items(),
                                               key=lambda item: item[1], reverse=True)}
                traded_players = set(after_teams_to_contracts[team].players.keys()).difference(
                    set(before_teams_to_contracts[team].players.keys()))

            # Add a subplot for the current team and trade status
            ax = fig.add_subplot(len(teams), 2, plot_count)
            ax.pie(
                x=np.fromiter(players_to_contracts.values(), dtype=int),
                startangle=75,
                labels=players_to_contracts.keys(),
                rotatelabels=25,
                labeldistance=1.0,
                textprops={'fontsize': 6},
                autopct=lambda p: '{:.1f}%'.format(p) if p > 0 else '',
                shadow=False
            )
            
            # Add a legend to the subplot with player names and their contracts
            leg = ax.legend(
                loc='right',
                prop={'size': 7.5},
                bbox_to_anchor=(1.70, 0.5),
                borderaxespad=1,
                labels=['%s - ${0:,.0f}'.format(s) % l for l, s in zip(players_to_contracts.keys(), players_to_contracts.values())]
            )

            # Mark traded players in the legend
            for text in leg.get_texts():
                res = [ele for ele in traded_players if (ele in text.get_text())]
                if res:
                    text.set_fontweight("semibold")
                    text.set_color("blue")

            plot_count += 1

    # Display
    plt.show()


def create_info_bar_plot(before_teams_to_contracts: dict, after_teams_to_contracts: dict, season: str) -> None:
    """
    Create a bar plot showing salary breakdown before and after a trade.

    Args:
        before_teams_to_contracts (dict): Dictionary mapping teams to their contract details before the trade.
        after_teams_to_contracts (dict): Dictionary mapping teams to their contract details after the trade.
        season (str): The season for which the salary breakdown is displayed.
    """
    # Determine teams involved in both before and after trades
    teams = set(before_teams_to_contracts.keys()) & set(after_teams_to_contracts.keys())

    # Create iterator for all teams involved in the trade
    team_itr = itertools.cycle(teams)

    bar_width = 0.40
    fig, ax = plt.subplots()

    # Create a dictionary to map the traded players to their respective contracts
    players_to_contracts = dict()

    # Extract contract details for the first team after the trade
    sorted_players_to_contracts1 = {player: contract[0] for player, contract in
                                    sorted(after_teams_to_contracts[next(team_itr)].players.items(),
                                           key=lambda item: item[1], reverse=True)}

    # Update players_to_contracts and create a bar plot for the first team after the trade
    players_to_contracts.update(sorted_players_to_contracts1)
    ind1 = np.arange(len(sorted_players_to_contracts1.keys()))
    bar1 = ax.bar(ind1, sorted_players_to_contracts1.values(), bar_width)

    # Extract contract details for the second team after the trade
    sorted_players_to_contracts2 = {player: contract[0] for player, contract in
                                    sorted(after_teams_to_contracts[next(team_itr)].players.items(),
                                           key=lambda item: item[1], reverse=True)}

    # Update players_to_contracts and create a bar plot for the second team after the trade
    players_to_contracts.update(sorted_players_to_contracts2)
    ind2 = np.arange(len(sorted_players_to_contracts2.keys()))
    bar2 = ax.bar(ind2 + bar_width, sorted_players_to_contracts2.values(), bar_width)

    # Add salary values on top of the bars
    for rect in bar1 + bar2:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(),
                 '${0:,.0f}'.format(int(height)),
                 fontsize=7,
                 ha='center', va='bottom')

    # Create labels
    ax.set_title("New Roster Salary Breakdown: {}".format(season))
    ax.set_xlabel("Players")
    ax.set_ylabel("Salary ($)")
    ax.legend((bar1[0], bar2[0]), (next(team_itr), next(team_itr)))

    # Format y-axis to display currency
    plotutils.format_y_axis_to_currency(ax)

    # Combine x-tick locations and labels
    ind = np.concatenate((ind1, ind2 + bar_width))
    ax.set_xticks(ind, minor=False)
    ax.set_xticklabels(list(sorted_players_to_contracts1.keys()) + list(sorted_players_to_contracts2.keys()),
                       rotation=90, minor=False, ha='center', fontdict={'fontsize': 7})

    # Display plot with grid
    plt.grid(True)
    plt.show()


def create_line_plot(teams_to_contracts: dict) -> None
    """Create line plots showing salary trends for each team.

    Args:
        teams_to_contracts (dict): Dictionary mapping teams to their contract details.
    """
    # Iterate over each team in involved in the trade
    for team in teams_to_contracts.keys():
        fig, ax = plt.subplots()

        # Iterate over each player and their contracts for the current team
        for player, contracts in sorted(teams_to_contracts[team].players.items(), key=lambda x: x[1], reverse=True):
            plt.plot(plotutils.get_future_seasons(2020, 21)[1:len(contracts) + 1], contracts,
                     marker='', linewidth=2, alpha=0.9, label=player)

        # Set y-axis minimum limit to 0
        ax.set_ylim(ymin=0)

        # Adjust y-axis ticks to display in millions
        start, end = ax.get_ylim()
        ax.yaxis.set_ticks(np.arange(start, end, step=1000000))

        # Format y-axis to display currency
        plotutils.format_y_axis_to_currency(ax)

        # Create labels
        plt.title("{}".format(team), fontsize=14)
        plt.xlabel("Season")
        plt.ylabel("Salary")

        # Add legend
        plt.legend(loc='best')

        # Display plot with grig
        plt.grid(True)
        plt.show()


def generate_trade_plots(plot: str, pre_trade_teams: dict, post_trade_teams: dict) -> None:
    """
    Generate trade plots based on the specified plot type.

    Args:
        plot (str): The type of plot to generate. Supported values: 'pie', 'bar', 'line'.
        pre_trade_teams (dict): Dictionary of pre-trade teams data.
        post_trade_teams (dict): Dictionary of post-trade teams data.
    """
    match plot:
        case 'pie':
            create_compare_trade_subplots(pre_trade_teams, post_trade_teams)
        case 'bar':
            create_info_bar_plot(pre_trade_teams, post_trade_teams, "2020-21")
        case 'line':
            create_line_plot(post_trade_teams)


