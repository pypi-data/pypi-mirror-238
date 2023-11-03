
def create_engine(creds_file_path):

    from sqlalchemy import create_engine
    from json import load

    try:
        creds_json = open(creds_file_path)
        creds_data = load(creds_json)
        creds_json.close()
    except Exception as e:
        print("There was an error with the requested credential path.")
        print(e)

    if creds_data['db_type'] == 'postgresql15':
        connection_string = f"postgresql://{creds_data['user']}:{creds_data['pass']}@{creds_data['host']}:{creds_data['port']}/{creds_data['dbname']}"
    
    engine = create_engine(connection_string)

    return engine


def run_sql(engine, file_path):
    # Will run a sql file starting from the files base directory.
    from sqlalchemy import text
    sql_file = open(file_path)
    sql = sql_file.read()
    sql_file.close()
    sqlcommands = sql.split(';')

    while("" in sqlcommands):
        sqlcommands.remove("")

    with engine.connect() as conn:
        if len(sqlcommands)>1:
            for command in sqlcommands:
                conn.execute(text(command))
            conn.commit()
        else:
            result = conn.execute(text(sql))
            conn.commit()
            return result
        
def clean_df_objects(df):
    for column in df:
        if df[column].dtype == "object":
            bad_characters = ['\x00','\t','\n','\r','\x0a']
            for char in bad_characters:
                try:
                    df[column] = df[column].str.replace(char,'', regex=True)
                except:
                    pass
    return df

def create_stage(engine,endpoint):
    import pandas as pd
    from os import path, getcwd
    from json import loads, dumps
    from .titanpy_tools import standardize_name
    from sqlalchemy import text

    endpoint_name = endpoint
    default_json_file = f"{endpoint_name}.json"
    file_path = f"../defaults/types/{default_json_file}"
    import os
    this_dir, this_filename = os.path.split(__file__)
    DATA_PATH = os.path.join(this_dir, file_path)
    type_file = open(DATA_PATH)
    default_type = loads(type_file.read())
    type_file.close()
    default_df = pd.json_normalize(default_type, sep='_', max_level=None)
    default_df["tenant_id"] = 0
    default_df = default_df[0:0]
    with engine.connect() as conn:
        
        default_df.to_sql(f"st_src_{endpoint_name}_stage", conn, if_exists='replace', schema='atlas', index=False)

def stage_then_merge(engine, df_dict):

    from sqlalchemy import text
    from pandas import read_sql
    import logging

    for name in df_dict:
        logging.basicConfig(filename=f"atlas.log", force=True, level=logging.INFO)
        source_name = f"st_src_{name}"
        logging.info(f"Creating {source_name} staging table...")
        df = df_dict[name]
        df = clean_df_objects(df)
        df.dropna(how='all', axis=1, inplace=True)
        if len(df.index) == 0:
            logging.info(f"No data returned for endpoint {source_name}")
            pass
        else:
            with engine.connect() as conn:
                create_stage(engine, name)
                df.to_sql(f"{source_name}_stage", conn, if_exists='append', schema='atlas', index=False)

                conn.execute(text(f"CREATE TABLE IF NOT EXISTS atlas.{source_name} AS select * from atlas.{source_name}_stage"))
                conn.commit()

                df2 = read_sql(text(f"select * from atlas.{source_name}"), engine)
                df = read_sql(text(f"select * from atlas.{source_name}_stage"), engine)
                df_columns = ''.join(f'stage_table."{col}", ' for col in df.columns.values.tolist())
                df_columns = df_columns[:-2]
                df2_columns = ''.join(f'"{col}", ' for col in df2.columns.values.tolist())
                df2_columns = df2_columns[:-2]
                update_string = ''.join(f'"{col}" = stage_table."{col}", ' for col in df2.columns.values.tolist())
                update_string = update_string[:-2]

                logging.info(f"Merging into source table...")
                conn.execute(text(f"merge into atlas.{source_name} source_table using atlas.{source_name}_stage stage_table on source_table.id = stage_table.id when matched then update set {update_string} when not matched then insert ({df2_columns}) values ({df_columns});"))
                conn.commit()
                logging.info(f"Completed merge!")
