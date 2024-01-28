import sys

def get_future_seasons(current_season: int, future_season: int) -> list:
    """Generate a list of future seasons based on the current season and a specified future season.

    Parameters:
        current_season (int): The starting year of the current season.
        future_season (int): The starting year of the future season.

    Returns:
        list: A list of future season strings.
    """
    return [
        "Guaranteed",
        str(current_season)   + '-' + str(future_season),
        str(current_season+1) + '-' + str(future_season+1),
        str(current_season+2) + '-' + str(future_season+2),
        str(current_season+3) + '-' + str(future_season+3),
        str(current_season+4) + '-' + str(future_season+4),
        str(current_season+5) + '-' + str(future_season+5)
    ]


def get_team_list() -> list:
    """Returns a list of tuples containing team abbreviations and full team names."""
    return [
             ("ATL", "Atlanta Hawks"),          ("BOS", "Boston Celtics"),     ("BRK", "Brooklyn Nets"), 
             ("CHO", "Charlotte Hornets"),      ("CHI", "Chicago Bulls"),      ("CLE", "Cleveland Cavaliers"), 
             ("DAL", "Dallas Mavericks"),       ("DEN", "Denver Nuggets"),     ("DET", "Detroit Pistons"), 
             ("GSW", "Golden State Warriors"),  ("HOU", "Houston Rockets"),    ("IND", "Indiana Pacers"),
             ("LAC", "Los Angeles Clippers"),   ("LAL", "Los Angeles Lakers"), ("MEM", "Memphis Grizzlies"),
             ("MIA", "Miami Heat"),             ("MIL", "Milwaukee Bucks"),    ("MIN", "Minnesota Timberwolves"),
             ("NOP", "New Orleans Pelicans"),   ("NYK", "New York Knicks"),    ("OKC", "Oklahoma City Thunder"),
             ("ORL", "Orlando Magic"),          ("PHI", "Philadelphia 76ers"), ("PHO", "Phoenix Suns"),
             ("POR", "Portland Trail Blazers"), ("SAC", "Sacramento Kings"),   ("SAS", "San Antonio Spurs"),
             ("TOR", "Toronto Raptors"),        ("UTA", "Utah Jazz"),          ("WAS", "Washington Wizards"),
            ]


def get_team_full_name(team_abr: str) -> str:
    """Returns the full team name corresponding to the given abbreviation.

    Parameters:
        team_abr (str): Abbreviation of the team.

    Returns:
        str: Full name of the team.

    Raises:
        SystemExit: If the team abbreviation is invalid.
    """
    for abr, full_name in get_team_list():
        if team_abr == abr:
            return full_name

    sys.exit('Invalid Team Abbreviation!')


