
class Atlas:

    def __init__(self, tp=None):
        self.tp = tp

    def Build(self, type, db_cred_path, st_credential_paths*):

        from Titanpy.titanpy import Titanpy

        # Connect to database
        import sqlalchemy
        # Create Schema
        # Loop through connections and build database
        self.tp = Titanpy()
        self.tp.Connect(st_credential_paths)

    def Update(self, type, db_cred_path, st_credential_paths*):
        pass


