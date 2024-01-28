'''
Description:
    - Recreation of ESPN's NBA Trade Machine (http://www.espn.com/nba/tradeMachine)

Notes:
    - When evaluating an NBA trade, it's worth remembering that the two teams can view the deal entirely differently. 
          + One team could consider a trade simultaneous, while the other team breaks the transaction down
            into two separate trades, one simultaneous and one non-simultaneous
    - Team's outgoing salary for matching purposes is the guaranteed salary rather than the total salary
    - When determining whether a team is over the cap or the luxury tax line for traded player exception
      purposes, the team's total salary after the trade is the deciding factor
    - Teams that are under the cap before a trade and go over the cap as a result of the trade 
      can't create a trade exception as a result of that deal
    - For salary-matching purposes, future draft picks or the draft rights to an unsigned player
      aren't taken into consideration

Example:
    python3 main.py --src BRK HOU -players "Spencer Dinwiddie" "P.J. Tucker" —dest HOU BRK —plot bar

TODO:
    - Check for no trade clause, trade kickers, etc.
    - Create interface
'''

import copy
import sys
from classes.draft_info import DraftInfo
from classes.team import Team
from classes.trade_player import TradePlayer
from db import financial as financialDB
from db import draft as draftDB
from enums.minimum_salaries import MinimumSalaries
from enums.mid_level_exceptions import MidLevelExceptionNonTaxPayer
from enums.mid_level_exceptions import MidLevelExceptionTaxPayer
from enums.mid_level_exceptions import RoomException
from enums.bi_annual_exception import BiAnnualException
from helpers import trade_utils as utils
from logs.error_logger import report_error


def evaluate_trade(season: str, players: list, src_teams: list, dest_teams: list) -> tuple:
    """Evaluate trade from user.

    Parameters:
        season (str): Season year.
        players (list): List of player names.
        src_teams (list): List of the player's original team names.
        dest_teams (list): List of destination team names.

    Returns:
        tuple: Pre-trade teams info, post-trade teams info.
    """

    # Convert Abbreviated Original Team Names to Full Team Names
    teams = [utils.get_team_full_name(team) for team in src_teams ]

    # Get Traded Teams Info
    trade_teams = load_trade_teams(season, teams)

    # Determine which teams are classified as a "Tax Paying Team"
    determine_tax_paying_teams("2019-20", trade_teams)

    # Create copy of trade teams before trade is procssed
    pre_trade_teams = copy.deepcopy(trade_teams)

    # Process Trade
    trade_players_to_teams = swap_trade_team_players(trade_teams, players, dest_teams)
    post_trade_teams = process_simultaneous_trade(trade_players_to_teams, trade_teams, teams)

    return tuple(pre_trade_teams, post_trade_teams)


def load_trade_teams(season: str, teams: list) -> dict:
    """Load trade teams.

    Parameters:
        season (str): Season year.
        teams (list): List of team names.

    Returns:
        dict: Trade teams info.
    """

    sql_table_df  = financialDB.read("Players", "Payroll{}".format(season)) # TODO

    season  = "2020-21" # TODO: MAKE GLOBAL VARIABLE
    seasons = get_future_seasons(currentSeason=int(season[:4]), futureSeason=int(season[-2:]))[1:5]

    for season in seasons:
        # TODO: Make into functions in utils.py
        sql_table_df[season] = sql_table_df[season].map(lambda x: x.replace(",", "").replace("$", ""))
        sql_table_df[season] = [ 0 if contract == '' else contract for contract in sql_table_df[season] ]
        sql_table_df[season] = sql_table_df[season].astype(int)

    trade_teams = dict()
    for team in teams:
        trade_teams[team] = Team()

        # Get players and their contracts
        players_seasons_df = sql_table_df[['Player'] + seasons].loc[sql_table_df.Team == team]

        # Store contract to player
        for index, row in players_seasons_df.iterrows():
            trade_teams[team].players[row['Player']] = list()
            for season in seasons:
                if row[season] > 0:
                    trade_teams[team].players[row['Player']].append(row[season])

            # Remove player if there is no data
            if len(trade_teams[team].players[row['Player']]) == 0:
                trade_teams[team].players.pop(row['Player'], None)

    # Draft Info
    get_draft_picks(trade_teams)

    return trade_teams


def get_draft_picks(trade_teams: dict) -> None:
    """Retrieve draft picks information for trade teams from a SQL table.

    This function retrieves draft pick information for each trade team from a SQL table
    containing data about future draft picks. It populates the 'draftPicks' attribute
    of each trade team with the relevant draft information.

    Args:
        trade_teams (dict): Dictionary containing trade team objects.
    """
    # Read draft pick information from the SQL table into a DataFrame
    sql_table_df  = draftDB.read("Draft", "FuturePicks")

    # Iterate over each row in the filtered DataFrame.
    # Create a DraftInfo object and append it to the team's draft picks list.
    for team in trade_teams:
        for index, row in sql_table_df[sql_table_df["Team"] == team].iterrows():
            trade_teams[team].draftPicks.append(DraftInfo(row["Season"], row["Round"], row["PickInfo"]))


def determine_tax_paying_teams(season: str, trade_teams: dict) -> None:
    """Determine tax paying teams.

    Parameters:
        season (str): Season year.
        trade_teams (dict): Trade teams info.
    """

    # Important Numbers (Need to move)
    salay_cap_min = 109140000    # 2019-21 Seasons
    luxury_tax   = 132627000    # 2019-21 Seasons

    sql_table_df = financialDB.read("Teams", "SalaryCapOverview{}".format(season))

    sql_table_df[season] = sql_table_df[season].map(lambda x: x.replace(",", "").replace("$", ""))
    sql_table_df[season] = sql_table_df[season].astype(int)

    for team, data in trade_teams.items():
        if int(sql_table_df[season].loc[sql_table_df.Team == team]) > luxury_tax:
            data.taxPaying = True


def swap_trade_team_players(trade_teams: dict, players: list, dest_teams: list) -> dict:
    """Swap trade team players to their new team.

    Parameters:
        trade_teams (dict): Trade teams info.
        players (list): List of player names.
        dest_teams (list): List of destination team names.

    Returns:
        dict: Trade players to teams mapping.
    """
    dest_teams = [ utils.get_team_full_name(team) for team in dest_teams ]

    trade_players_to_teams = dict()
    for team, data in trade_teams.items():

        trade_players_to_teams[team] = list()
        for (player, destTeam) in zip(players, dest_teams):
    
            # Check if Player is being traded and has not already been traded
            if (player in data.players) and (destTeam != team):

                # Add Traded Player to List of Traded Players
                trade_players_to_teams[team].append( {player: data.players[player]} )

                # Add Traded Player to New Team
                trade_teams[destTeam].players.update( {player: data.players[player]} )

                # Remove Traded Player from Old Team
                trade_teams[team].players.pop(player)

    return trade_players_to_teams


def process_simultaneous_trade(trade_players_to_teams: dict, trade_teams: dict, teams: list) -> dict:
    """Process simultaneous trade.

    Parameters:
        trade_players_to_teams (dict): Trade players to teams mapping.
        trade_teams (dict): Trade teams info.
        teams (list): List of team names.

    Returns:
        dict: Post-trade teams info.

    Raises:
        SystemExit: If the trade cannot be processed due to salary limit constraints.
    """
    contracts_totals = [sum(list(trade_player.values())[0][0] for trade_player in trade_players_to_teams[team]) for team in trade_teams]

    team1_successful = contracts_totals[0] < trade_teams[teams[1]].salaryLimit
    team2_successful = contracts_totals[1] < trade_teams[teams[0]].salaryLimit

    if team1_successful and team2_successful:
        print("Trade Successful.")
        return trade_teams
    elif not team1_successful:
        report_error(teams[1], trade_teams[teams[1]].salaryLimit, contracts_totals[0])
    elif not team2_successful:
        report_error(teams[0], trade_teams[teams[0]].salaryLimit, contracts_totals[1])


def evaluate_non_tax_paying_team_limit(trade_players_contracts_total: float) -> float:
    """Evaluate salary limit for non-taxpaying team.
    
    In a simultaneous trade a NON-TAXPAYING team can trade one or more players and take back...
        - 175% of the outgoing salary (plus $100K), for any amount up to $6,533,333.
        - The outgoing salary plus $5MM, for any amount between $6,533,333 and $19,600,000.
        - 125% of the outgoing salary (plus $100K), for any amount above $19,600,000.

    Parameters:
        trade_players_contracts_total (float): Total contracts sum.

    Returns:
        float: Salary limit.
    """
    min_salary          = 6533333
    min_trade_pct       = 1.75
    min_salary_addition = 100000

    mid_salary_addition = 5000000000

    max_salary          = 19600000
    max_trade_pct       = 1.25
    max_salary_addition = 100000

    if trade_players_contracts_total in range(0, min_salary):
        print("Min Trade Contract")
        return (trade_players_contracts_total * min_trade_pct) + min_salary_addition

    elif trade_players_contracts_total in range(min_salary, max_salary):
        print("Mid-Level Trade Contract")
        return trade_players_contracts_total + mid_salary_addition

    elif trade_players_contracts_total > max_salary:
        print("Max Trade Contract")
        return (trade_players_contracts_total * max_trade_pct) + max_salary_addition

    else:
        sys.exit("Trade unable to be processed")


def evaluate_tax_paying_team_limit(trade_players_contracts_total: float) -> float:
    """Evaluate salary limit for taxpaying team.

    Parameters:
        trade_players_contracts_total (float): Total contracts sum.

    Returns:
        float: Salary limit.
    """
    trade_pct = 1.25
    salary_addition = 100000
    return (trade_players_contracts_total * trade_pct) + salary_addition


def process_non_simultaneous_trade(trade_team: Team, teams: list) -> None:
    """Process non-simultaneous trade.

    In non-simultaneous deals, a team can trade away a single player without immediately taking salary back in return. 
    The team then has up to one year in which it can acquire one or more players whose combined salaries amount to 
    no more than the traded player's salary (plus $100K).
    Trade exceptions created in non-simultaneous trades can't be
        - Combined with another trade exception, any other excptions, or player's salary
        - Used to sign a free agent
        - Traded outright to another team.

    Parameters:
        trade_team (Team): Trade team info.
        teams (list): List of team names.
    """
    salary_addition = 100000

    # Check if the trade involves only one player
    if len(trade_team.players) == 1:
        # Calculate the total salary of the traded player(s) for each team involved in the trade
        trade_players_contracts_total = sum([
            list(trade_player.values())[0][0] for trade_player in trade_players_to_teams[team]
        ])

        # Set the traded player exception for the trade team
        trade_teams[team].traded_player_exception = trade_players_contracts_total + salary_addition
