import os
from fixess import Fixess

client = Fixess(api_key=os.getenv('FIXESS_API_KEY'))
client['key'] = 'value'

print(client['key'])