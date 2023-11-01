# visit my page! happy to help: https://github.com/pabboat 
# I recommend using "from titanpy import Titanpy as tp"

# imports
from Titanpy.titanpy import Titanpy
# from Titanpy.atlas import Atlas

# test scripts

if __name__ == "__main__":
    b = Titanpy()

    b.Connect(cred_path="./credentials/servicetitan_credentials.json")

    print(b.Get(endpoint = 'receipts'))
