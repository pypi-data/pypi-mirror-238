from sqlalchemy import Column, Integer, String, create_engine, DateTime
from sqlalchemy.ext.declarative import declarative_base
from tornado_sqlalchemy import SQLAlchemy
import datetime
import os
# 配置SQLAlchemy
# 创建一个会话（Session）工厂
if os.name == "nt":
    os.environ["HOME"] = os.path.expanduser("~")
PID_FILEPATH = os.path.expandvars("$HOME/.yyperf/mydatabase.db")
os.makedirs(os.path.dirname(PID_FILEPATH), exist_ok=True)
engine = create_engine('sqlite:///{}'.format(PID_FILEPATH), echo=True)
Base = declarative_base(bind=engine)


# 创建User模型
class PerfDataRecord(Base):
    __tablename__ = 'data_record'
    id = Column(Integer, primary_key=True)
    start_time = Column(DateTime, default=datetime.datetime.utcnow)
    end_time = Column(DateTime, default=datetime.datetime.utcnow)
    devices = Column(String(50))
    app_name = Column(String(50))
    app_version = Column(String(50))
    app_package = Column(String(50))
    filepath = Column(String(254))
