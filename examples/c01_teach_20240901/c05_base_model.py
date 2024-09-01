from datetime import datetime
from operator import index

from sqlalchemy import create_engine, DateTime, func, String
from sqlalchemy.orm import Mapped, DeclarativeBase
from sqlalchemy.testing.schema import mapped_column

engine = create_engine('mysql+pymysql://root:zhangdapeng520@127.0.0.1:3306/fastzdp_sqlalchemy?charset=utf8')


class BaseModel(DeclarativeBase):
    """基础模型"""
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    create_time: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now(), comment="创建时间")
    update_time: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now(), onupdate=func.now(),
                                                  comment="更新时间")


class Employee(BaseModel):
    """员工模型，对应员工表"""
    __tablename__ = 'employee'
    name: Mapped[str] = mapped_column(String(36), index=True, nullable=False, comment="姓名")
    age: Mapped[int] = mapped_column(comment="年龄")


if __name__ == '__main__':
    BaseModel.metadata.create_all(engine)
