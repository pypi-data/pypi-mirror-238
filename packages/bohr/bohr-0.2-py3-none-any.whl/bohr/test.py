from database import Database
from mdm import MarketDataManager
import psycopg2.extras as extras
import pandas as pd


mdm = MarketDataManager('http://localhost:5000','luis','admin')
df = mdm.get_ncc(payload={})
print(df)