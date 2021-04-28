import pandas as pd
import sqlalchemy


def build_fincidents(df_source: pd.DataFrame) -> pd.DataFrame:
    return df_source


def build_dgeography(df_source: pd.DataFrame) -> pd.DataFrame:
    pass


def build_dbuildings(df_source: pd.DataFrame) -> pd.DataFrame:
    pass


def transform_data(df_source: pd.DataFrame, db_engine:sqlalchemy.engine.Engine):
    dwh_fincidents = build_fincidents(df_source)
    db_engine.execute('TRUNCATE TABLE staging.dwh_fincidents;')
    dwh_fincidents.to_sql(con=db_engine, name='dwh_fincidents', schema='staging', index=False, method='multi', dtype=str, if_exists='replace')


