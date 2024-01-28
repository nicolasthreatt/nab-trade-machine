import matplotlib.pyplot as plt
from typing import List, Tuple


def format_y_axis_to_currency(ax: plt.Axes) -> None:
    """Formats y-axis ticks to currency.

    Args:
        ax (matplotlib.axes.Axes): Axes object.

    Returns:
        None
    """
    ax.set_yticks(list(ax.get_yticks()))
    a = ax.get_yticks().tolist()
    a = [f"${val:,.0f}" for val in a]
    ax.set_yticklabels(a)


def turn_off_tick_marks(ax: plt.Axes) -> None:
    """Turns off tick marks.

    Args:
        ax (matplotlib.axes.Axes): Axes object.
    """
    ax.axes.xaxis.set_ticks([])
    ax.axes.yaxis.set_ticks([])
    ax.set_frame_on(False)


def add_text_with_line(plt: plt, ax: plt.Axes, data_df, text: str, value: int, linestyle: str, color: str, text_increment: int = 400000) -> None:
    """Adds text with a line to the plot.

    Args:
        plt: Matplotlib.pyplot module.
        ax (matplotlib.axes.Axes): Axes object.
        data_df: Data dataframe.
        text (str): Text to display.
        value (int): Value to display.
        linestyle (str): Line style.
        color (str): Line color.
        text_increment (int): Text increment value. Default is 400000.
    """
    data_size = len(data_df) - 0.55

    plt.axhline(y=value, linestyle=linestyle, linewidth=1, color=color)
    ax.text(data_size, int(value) + text_increment,
            '{} - ${:,.0f}'.format(text, int(value)),
            fontsize=7,
            horizontalalignment="right")


def get_future_seasons(current_season: int, future_season: int) -> List[str]:
    """Generates future seasons list.

    Args:
        current_season (int): Current season.
        future_season (int): Future season.

    Returns:
        list: List of future seasons.
    """
    return [
        "Guaranteed",
        f"{current_season}-{future_season}",
        f"{current_season + 1}-{future_season + 1}",
        f"{current_season + 2}-{future_season + 2}",
        f"{current_season + 3}-{future_season + 3}",
        f"{current_season + 4}-{future_season + 4}",
        f"{current_season + 5}-{future_season + 5}"
    ]


def bar_color(category: str) -> str:
    """Determines color for bar based on category.

    Args:
        category (str): Category type.

    Returns:
        str: Color.
    """
    if category == 'made':
        return 'green'
    elif category == 'missed':
        return 'red'
    elif category == "percent":
        return 'dodgerblue'
    elif category == "frequency":
        return 'orange'
    else:
        return 'blue'
