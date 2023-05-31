import pandas

from pipeline import get_brand_datasets, get_federal_state_datasets

def test_get_brand_datasets():
    get_brand_datasets()

    brand_statistics = pandas.read_sql_table('brand-statistics', 'sqlite:///data/data.sqlite')

    assert len(brand_statistics.index) > 0
    assert len(brand_statistics.columns) == 15

def test_get_federal_state_datasets():
    get_federal_state_datasets()
    federal_state_statistics = pandas.read_sql_table('federal-state-statistics', 'sqlite:///data/data.sqlite')

    assert len(federal_state_statistics.index) > 0
    assert len(federal_state_statistics.columns) == 17    