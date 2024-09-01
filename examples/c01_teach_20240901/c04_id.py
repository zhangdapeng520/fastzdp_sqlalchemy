from sqlalchemy import create_engine
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

engine = create_engine('mysql+pymysql://root:zhangdapeng520@127.0.0.1:3306/fastzdp_sqlalchemy?charset=utf8')


class BaseModel:
    """基础模型"""


class Employee(BaseModel):
    """员工模型，对应员工表"""
    __tablename__ = 'employee'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
