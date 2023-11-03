def standardize_name(endpoint):
    endpoint = endpoint.lower()
    endpoint = endpoint.replace("/", "_")
    endpoint = endpoint.replace("-", "_")
    return endpoint

def verify_endpoint(endpoint, df):
    import pandas as pd
    from json import loads
    
    endpoint_name = standardize_name(endpoint)

    default_json_file = f"{endpoint_name}.json"
    file_path = f"../defaults/types/{default_json_file}"
    import os
    this_dir, this_filename = os.path.split(__file__)
    DATA_PATH = os.path.join(this_dir, file_path)
    type_file = open(DATA_PATH)
    default_type = loads(type_file.read())
    type_file.close()
    
    default_df = pd.json_normalize(default_type, sep="_")
    df_columns_list = df.columns.values.tolist()
    default_df_columns_list = default_df.columns.values.tolist()
    # print(df_columns_list)
    # print(default_df_columns_list)

    error_count = 0
    for column in df_columns_list:
        try:
            default_df_columns_list.index(column)
        except Exception as e:
            print(f"Error trying to find {column} in default for endpoint {endpoint_name}. Please update JSON to include column. ")
            error_count += 1
    print(f"Endpoint {endpoint_name} has been verified. There are a total of {error_count} issues.")

    return default_df


def pull_full_dataframe(engine, st_creds_path, endpoint, titanpy_instance, start_date=None):

    import pandas as pd
    import logging
    from .database_tools import stage_then_merge

    print(f"Saving logs to {standardize_name(endpoint)}.log")
    logging.basicConfig(filename=f"atlas.log", force=True, level=logging.INFO)
    print(f"________________ Getting data from {endpoint} _________________")

    tp = titanpy_instance

    query = {
        "tenant": tp.tenant_id,
        "from": start_date
    }

    result = tp.Get(endpoint,query=query)

    result_json = result.json()
    # print(result_json)
    data = result_json['data']
    has_more = result_json['hasMore']
    continue_from = result_json['continueFrom']
    total_length = 0

    df = pd.json_normalize(data, sep="_")
    verify_endpoint(endpoint, df)
    total_length += len(df)

    df["tenant_id"] = tp.tenant_id
    df_dict = {}
    df_dict[standardize_name(endpoint)] = df
    stage_then_merge(engine, df_dict)

    while has_more==True:
        query["from"] = continue_from
        logging.info(f"More data to request. Continue from code: {continue_from}")
        try:
            result = tp.Get(endpoint,query=query)
            while result.status_code != 200:
                if result.status_code == 401:
                    tp.Connect(cred_path = st_creds_path)
                    result = tp.Get(endpoint,query=query)
                else:
                    from time import sleep
                    logging.info("Waiting 30 seconds due to rate limit")
                    sleep(30)
                    result = tp.Get(endpoint,query=query)
        except Exception as e:
            logging.error(e)
        result_json = result.json()
        data = result_json['data']
        has_more = result_json['hasMore']
        continue_from = result_json['continueFrom']
        df2 = pd.json_normalize(data, sep="_")
        df2["tenant_id"] = tp.tenant_id
        df_dict = {}
        df_dict[standardize_name(endpoint)] = df2
        stage_then_merge(engine, df_dict)
        total_length += len(df2)

        logging.info(f"Total Results ({endpoint}) so far: {total_length}")

def titanpy_dataframe(engine, endpoint_list, st_creds_path, start_date=None):
    
    from Titanpy.titanpy import Titanpy
    from threading import Thread

    tp = Titanpy()
    tp.Connect(cred_path = st_creds_path)

    if isinstance(endpoint_list, list):
        pass
    else:
        endpoint_list = [endpoint_list]

    for endpoint in endpoint_list:
        # pull_full_dataframe(engine,st_creds_path,endpoint,tp,start_date)
        Thread(target = pull_full_dataframe, args=(engine, st_creds_path,endpoint, tp, start_date)).start()



    