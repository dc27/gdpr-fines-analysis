import pandas as pd
from pandas.testing import assert_frame_equal
from scripts.wrangling_funs import filter_for_positives, strip_text_col
import pytest

# happy path
def test_filter_for_positives()->None:
    df = pd.DataFrame(dict(id = [1, 2, 3, 4, 5], balance = [-99.9, 100.0, 0.0, 0.0, 79.1]))
    df_positive = pd.DataFrame(dict(id = [2, 5], balance = [100.0, 79.1]))

    assert_frame_equal(filter_for_positives(df, "balance"), df_positive)

def test_filter_for_psotives_bad_input()->None:
    """
    GIVEN    a column of non-numeric type
     WHEN    function executed
     THEN    should raise appropriate error
    """
    df = pd.DataFrame(
        dict(
            id = [1, 2, 3, 4, 5], balance = [-99.9, 100.0, 0.0, 0.0, 79.1], bools = [True, True, True, True, True],
            text = ["A", "B", "C", "D", "D"]
            )
        )
    
    with pytest.raises(TypeError):
        filter_for_positives(df, "text")
    
    with pytest.raises(TypeError):
        filter_for_positives(df, "bools")

# happy path
def test_strip_text_col()->None:
    df = pd.DataFrame(dict(id = [1, 2, 3, 4], bank = ["super bank ", " mega bank", "awesome  ", "super bank"]))
    df_stripped = pd.DataFrame(dict(id = [1, 2, 3, 4], bank = ["super bank", "mega bank", "awesome", "super bank"]))

    assert_frame_equal(strip_text_col(df, "bank"), df_stripped)


def test_strip_text_col_bad_input()->None:
    """
    GIVEN    a column of non-str type
     WHEN    function executed
     THEN    should raise appropriate error
    """
    df = pd.DataFrame(dict(id = [1, 2, 3, 4], bank = ["super bank ", " mega bank", "awesome  ", "super bank"]))
    
    with pytest.raises(TypeError):
        strip_text_col(df, "id")
