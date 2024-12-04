import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest


@pytest.fixture
def generate_data():
    return pd.DataFrame(np.random.randint(0, 100, size=(100, 4)), columns=list("ABCD"))


@pytest.fixture
def generate_mini_data():
    return pd.DataFrame(
        [[2, 1, 3, 6], [4, 5, 10, 19], [6, 6, 13, 25]],
        index=[0, 1, "All"],
        columns=["A", "B", "C", "All"],
    )


@pytest.fixture
def matplotlib_figure(generate_mini_data):
    fig = plt.figure(figsize=(10, 6))
    ax = plt.gca()
    width = 0.8
    x = range(len(generate_mini_data.columns))

    for i, row in enumerate(generate_mini_data.index[:-1]):
        ax.bar(
            [xi + width * i / 2 for xi in x],
            generate_mini_data.loc[row],
            width=width / 2,
            label=f"Group {row}",
        )

    ax.plot(x, generate_mini_data.loc["All"], "r-o", label="All", linewidth=2)

    ax.set_xticks(x)
    ax.set_xticklabels(generate_mini_data.columns)
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.title("Data Comparison by Group")

    return fig
