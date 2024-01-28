from enum import Enum

class MidLevelExceptionNonTaxPayer(Enum):
    """
    The non-taxpayer mid-level exception is the primary tool available for over-the-cap teams to add free agents.
    As long as a team hasn't dipped below the cap to use cap space and doesn't go over the tax apron ($138,928,000) at all,
    it can use this MLE, which runs for up to four years with 5% annual raises.
    """
    Year0 = 9258000    # 2020-21
    Year1 = 9720900    # 2021-22
    Year2 = 10183800   # 2022-23
    Year3 = 10646700   # 2023-24


class MidLevelExceptionTaxPayer(Enum):
    """
    If a team uses more than $5,718,000 of its mid-level exception, it is forbidden from surpassing the tax apron at any time
    during the league year. So even if a team isn't above the apron when it uses its MLE, it might make sense to play it safe
    by avoiding using the full MLE and imposing a hard cap.
    """
    Year0 = 5718000    # 2020-21
    Year1 = 6003900    # 2021-22
    Year2 = 6289800    # 2022-23


class RoomException(Enum):
    """
    If a club goes under the cap, it loses its full mid-level exception, but gets this smaller room exception,
    which allows the team to go over the cap to sign a player once the team has used up all its cap space.
    It can be used to sign players for up to two years, with a 5% raise for the second season.
    """
    Year0 = 4767000    # 2020-21
    Year1 = 5005350    # 2021-22
