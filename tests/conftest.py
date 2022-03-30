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
