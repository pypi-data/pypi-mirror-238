from conftest import df
from pyspark.sql import Dataframe
from motordecalidad.rules import *
def test_nulls (df: Dataframe):
    data, errorDf = validateNull(df,"id",3,"TEST","100")
    assert data[-1] == 0