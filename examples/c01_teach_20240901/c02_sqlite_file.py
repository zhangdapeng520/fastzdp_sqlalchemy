from sqlalchemy import create_engine

engine = create_engine('sqlite:///sqlite3.db')
print(engine)
