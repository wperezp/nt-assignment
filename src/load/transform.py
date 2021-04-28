import pandas as pd
import sqlalchemy
import schemas


def build_fincidents(df_source: pd.DataFrame) -> pd.DataFrame:
    df_fincidents = df_source.loc[:, schemas.fincidents_cols]
    df_fincidents = df_fincidents.drop_duplicates(['Incident Number'])
    return df_fincidents


def build_dgeography(df_source: pd.DataFrame) -> pd.DataFrame:
    pass


def build_dbuildings(df_source: pd.DataFrame) -> pd.DataFrame:
    pass


def transform_data(df_source: pd.DataFrame, db_engine:sqlalchemy.engine.Engine):
    df_source['Incident Number'] = df_source['Incident Number'].astype(int)

    db_conn = db_engine.connect()
    result = db_conn.execute('SELECT MAX("Incident Number") FROM analytics.dwh_fincidents')
    max_incident_number = 0
    for row in result:
        if row['max'] is not None:
            max_incident_number = row['max']
    print(max_incident_number)

    df_new_incidents = df_source.loc[df_source['Incident Number'] > max_incident_number,]

    dwh_fincidents = build_fincidents(df_new_incidents)
    dwh_fincidents.to_sql(con=db_engine, name='dwh_fincidents', schema='staging', index=False, method='multi', dtype=str, if_exists='replace')


