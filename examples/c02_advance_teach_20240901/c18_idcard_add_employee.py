import enum
from datetime import datetime
from decimal import Decimal
from typing import List, Optional
import sqlalchemy
from sqlalchemy import create_engine, DateTime, func, String, select, ForeignKey
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
    job_time: Mapped[datetime] = mapped_column(DateTime, nullable=True, comment="入职时间")

    # 部门外键
    department_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("department.id"), comment="部门ID", nullable=True)
    department: Mapped[Optional['Department']] = relationship("Department", back_populates="employees")
    # 身份证外键
    idcard_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("idcard.id"), comment="身份证ID", nullable=True)
    idcard: Mapped[Optional["IdCard"]] = relationship("IdCard", back_populates="employee")


class Department(BaseModel):
    """部门模型，对应部门表"""
    __tablename__ = 'department'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(36), name="name", unique=True, nullable=False, comment="部门名称")
    city: Mapped[str] = mapped_column(String(36), name="city", unique=True, nullable=False, comment="所在城市")
    employees: Mapped[List['Employee']] = relationship("Employee", back_populates="department")

    # 自关联
    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey("department.id"), nullable=True, comment="上级部门ID")
    children: Mapped[List["Department"]] = relationship("Department", back_populates="parent")
    # remote_side=[id] 用来区分上下级关系，必须要加
    parent: Mapped[Optional["Department"]] = relationship("Department", back_populates="children", remote_side=[id])


class IdCard(BaseModel):
    """身份证模型类"""
    __tablename__ = 'idcard'
    card_id: Mapped[str] = mapped_column(sqlalchemy.String(18), unique=True, nullable=False, comment="身份证号")
    origin: Mapped[Optional[str]] = mapped_column(sqlalchemy.String(36), nullable=True, comment="籍贯")

    # 员工一对一关联
    employee: Mapped[Optional["Employee"]] = relationship("Employee", back_populates="idcard")


class UserRole(BaseModel):
    """用户与角色的关系模型"""
    __tablename__ = 'user_role'
    user_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("user.id"), nullable=False, comment="用户ID")
    role_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("role.id"), nullable=False, comment="角色ID")


class User(BaseModel):
    """用户模型类"""
    __tablename__ = 'user'
    username: Mapped[str] = mapped_column(sqlalchemy.String(36), unique=True, nullable=False, index=True,
                                          comment="账号")
    password: Mapped[str] = mapped_column(sqlalchemy.String(128), nullable=False, comment="密码")

    # 一个可以有多个角色
    # secondary=UserRole.__table__ 指定第三张中间表，不能少
    roles: Mapped[Optional[List["Role"]]] = relationship("Role", back_populates="users", secondary=UserRole.__table__)


class Role(BaseModel):
    """角色模型类"""
    __tablename__ = 'role'
    name: Mapped[str] = mapped_column(sqlalchemy.String(36), unique=True, index=True, comment="角色名称")
    nickname: Mapped[Optional[str]] = mapped_column(sqlalchemy.String(36), nullable=True, comment="角色昵称")

    # 一个角色可以关联多个用户
    users: Mapped[Optional[List["User"]]] = relationship("User", back_populates="roles", secondary=UserRole.__table__)


if __name__ == '__main__':
    with sessionmaker(engine).begin() as session:
        idcard = IdCard(card_id="188888888888888888", origin="北京")

        department = session.get(Department, 2)

        ls = Employee(name="李四", age=34, salary=30000, job_time="2022-09-01", gender=GenderEnum.MALE.value)
        ls.idcard = idcard
        ls.department = department

        session.add(ls)
