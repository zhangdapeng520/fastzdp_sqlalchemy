import enum
from datetime import datetime
from decimal import Decimal
from typing import List, Optional
import sqlalchemy
from sqlalchemy import create_engine, DateTime, func, String, select
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column, Session, sessionmaker, relationship

engine = create_engine('mysql+pymysql://root:zhangdapeng520@127.0.0.1:3306/fastzdp_sqlalchemy?charset=utf8', echo=True)


class BaseModel(DeclarativeBase):
    """基础模型"""
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    create_time: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now(), comment="创建时间")
    update_time: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now(), onupdate=func.now(),
                                                  comment="更新时间")


class GenderEnum(enum.Enum):
    MALE = "男"
    FEMALE = "女"


class Employee(BaseModel):
    """员工模型，对应员工表"""
    __tablename__ = 'employee'
    name: Mapped[str] = mapped_column(String(36), index=True, nullable=False, comment="姓名")
    age: Mapped[int] = mapped_column(comment="年龄")
    salary: Mapped[Decimal] = mapped_column(sqlalchemy.DECIMAL, nullable=False, comment="薪资")
    bonus: Mapped[float] = mapped_column(sqlalchemy.FLOAT, default=0, comment="奖金")
    is_leave: Mapped[bool] = mapped_column(sqlalchemy.Boolean, default=False, comment="是否离职")
    gender: Mapped[GenderEnum] = mapped_column(sqlalchemy.String(6), default=GenderEnum.MALE, comment="性别")
    department_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("department.id", ondelete="CASCADE"),
                                               nullable=False, comment="部门ID")
    department: Mapped[Optional['Department']] = relationship("Department", back_populates="employees")


class Department(BaseModel):
    """部门模型，对应部门表"""
    __tablename__ = 'department'
    name: Mapped[str] = mapped_column(String(36), name="name", unique=True, nullable=False, comment="部门名称")
    city: Mapped[str] = mapped_column(String(36), name="city", unique=True, nullable=False, comment="所在城市")
    employees: Mapped[List['Employee']] = relationship("Employee", back_populates="department", passive_deletes=True)


if __name__ == '__main__':
    with sessionmaker(engine).begin() as session:
        employee = session.get(Employee, 1)
        employee.department = None
