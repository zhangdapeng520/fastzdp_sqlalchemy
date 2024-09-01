from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://root:zhangdapeng520@127.0.0.1:3306/fastzdp_sqlalchemy?charset=utf8')
print(engine)
