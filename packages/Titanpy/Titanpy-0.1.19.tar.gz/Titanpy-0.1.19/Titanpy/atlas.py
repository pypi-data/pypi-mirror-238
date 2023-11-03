# Atlas Class Doc
class Atlas:

    def __init__(self, tp=None):
        self.tp = tp

    def Build(self, sql_creds_path, st_creds_path, type = 'Default', start_date = None):

        from Titanpy.atlas_scripts.python.build_types import Default
        if type == 'Default':
            Default(sql_creds_path, st_creds_path, start_date)

if __name__ == "__main__":
    Atlas().Build("./credentials/postgresql_credentials.json", "./credentials/servicetitan_credentials.json", type = 'Default', start_date = '2023-01-01')