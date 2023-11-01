
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
    from os import path, getcwd
    from sqlalchemy import text

    __location__ = path.realpath(path.join(getcwd(), path.dirname(__file__)))
    sql_file = open(path.join(__location__, file_path),'r')
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

