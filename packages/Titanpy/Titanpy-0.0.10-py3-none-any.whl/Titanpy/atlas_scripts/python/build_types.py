# This script contains functions that Atlas uses to created different types of source datasets and initializes the database using sqlalchemy.

def Default(sql_creds_path, st_creds_path):
    
    from database_tools import create_engine, run_sql
    from titanpy_tools import titanpy_dataframe

    endpoint_list = [
        'export/jobs',
        'export/customers'
    ]

    titanpy_dataframe(endpoint_list, st_creds_path)

    # engine = create_engine(sql_creds_path)
    # run_sql(engine, '../sql/create_atlas_schema.sql')
    # run_sql(engine, "../sql/create_test_table.sql")


if __name__ == "__main__":
    Default("./credentials/postgresql_credentials.json", "./credentials/servicetitan_credentials.json")