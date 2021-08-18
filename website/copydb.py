print('Initializing...')

import pandas as pd
import sqlalchemy


db1 = sqlalchemy.create_engine(f'sqlite:///test.db')
db2 = sqlalchemy.create_engine(f'sqlite:///testi.db')

print('Writing...')

query = '''SELECT * FROM user'''
df = pd.read_sql(query, db1)
df.to_sql('test_table', db2, schema='', index=False, if_exists='replace')

print('(1) [test_table] copied.')