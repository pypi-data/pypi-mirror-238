def verify_endpoint(endpoint, df):
    from os import path, getcwd
    import pandas as pd
    from json import loads
    endpoint_name = endpoint.lower().replace("/", "_")

    default_json_file = f"{endpoint_name}.json"

    __location__ = path.realpath(path.join(getcwd(), path.dirname(__file__)))
    file_path = f"../defaults/types/{default_json_file}"
    type_file = open(path.join(__location__, file_path),'r')
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

def titanpy_dataframe(endpoint_list, st_creds_path):
    
    from Titanpy import Titanpy
    import pandas as pd

    tp = Titanpy()
    tp.Connect(cred_path = st_creds_path)

    if isinstance(endpoint_list, list):
        pass
    else:
        endpoint_list = [endpoint_list]

    df_dict = {}
    for endpoint in endpoint_list:

        result = tp.Get(endpoint)
        result_json = result.json()

        data = result_json['data']
        has_more = result_json['hasMore']
        continue_from = result_json['continueFrom']
        print(has_more)

        df = pd.json_normalize(data, sep="_")
        verify_endpoint(endpoint, df)

        df["tenant_id"] = tp.tenant_id
        df_dict[endpoint] = df

    print(df_dict['export/jobs'])


    