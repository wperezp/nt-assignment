import pandas as pd
import sqlalchemy
import schemas


def build_fincidents(df_source: pd.DataFrame) -> pd.DataFrame:
    df_fincidents = df_source.loc[:, schemas.fincidents_cols]
    df_fincidents = df_fincidents.drop_duplicates(['Incident Number'])
    return df_fincidents


def build_dgeography(df_source: pd.DataFrame) -> pd.DataFrame:
    df_dgeography = df_source.loc[:, schemas.dgeography_cols]
    df_dgeography = df_dgeography.drop_duplicates(['Incident Number'])
    return df_dgeography


def build_dbuildings(df_source: pd.DataFrame) -> pd.DataFrame:
    df_dbuildings = df_source.loc[:, schemas.dbuildings_cols]
    return df_dbuildings


def transform_data(df_source: pd.DataFrame, db_engine:sqlalchemy.engine.Engine):
    df_source['Incident Number'] = df_source['Incident Number'].astype('int32')

    max_incident_number = 0
    # Get last incident ingested
    with db_engine.connect() as connection:
        result = connection.execute('SELECT MAX("Incident Number") FROM analytics.dwh_fincidents')
        for row in result:
            if row['max'] is not None:
                max_incident_number = row['max']
        print(f"Last incident number in database is: {max_incident_number}")

    # Restrict dataset
    df_new_incidents = df_source.loc[df_source['Incident Number'] > max_incident_number,]

    with db_engine.connect() as connection:
        with connection.begin():
            # Build datasets and upload to staging table
            dwh_fincidents = build_fincidents(df_new_incidents)
            print("Loading dwh_fincidents")
            dwh_fincidents.to_sql(con=connection, name='dwh_fincidents', schema='staging', index=False, method='multi',
                                  dtype=sqlalchemy.types.VARCHAR(length=200), if_exists='replace', chunksize=100)
            print("Loading dwh_dgeography")
            dwh_dgeography = build_dgeography(df_new_incidents)
            dwh_dgeography.to_sql(con=connection, name='dwh_dgeography', schema='staging', index=False, method='multi',
                                  dtype=sqlalchemy.types.VARCHAR(length=200), if_exists='replace', chunksize=100)
            print("Loading dwh_dbuildings")
            dwh_dbuildings = build_dbuildings(df_new_incidents)
            dwh_dbuildings.to_sql(con=connection, name='dwh_dbuildings', schema='staging', index=False, method='multi',
                                  dtype=sqlalchemy.types.VARCHAR(length=200), if_exists='replace', chunksize=100)

    print("Updating analytics tables")
    with db_engine.connect() as connection:
        with connection.begin():
            connection.execute('INSERT INTO analytics.dwh_fincidents SELECT * FROM staging.dwh_fincidents')
            connection.execute('INSERT INTO analytics.dwh_dgeography SELECT * FROM staging.dwh_dgeography')
            connection.execute('INSERT INTO analytics.dwh_dbuildings SELECT * FROM staging.dwh_dbuildings')

    print("Upload finished")


