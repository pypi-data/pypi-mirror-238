# Atlas Class Doc
class Atlas:

    def __init__(self, tp=None):
        self.tp = tp

    def Build(self, sql_creds_path, st_creds_path, type = 'Default', start_date = None):

        from atlas_scripts.python.build_types import Default
        if type == 'Default':
            Default(sql_creds_path, st_creds_path, start_date)

