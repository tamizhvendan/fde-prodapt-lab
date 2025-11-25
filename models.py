from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class JobBoard(Base):
  __tablename__ = 'job_boards'
  id = Column(Integer, primary_key=True)
  slug = Column(String, nullable=False, unique=True)
  logo_url = Column(String, nullable=True)

class JobPost(Base):
  __tablename__ = 'job_posts'
  id = Column(Integer, primary_key=True)
  title = Column(String, nullable=False)
  description = Column(String, nullable=False)
  job_board_id = Column(Integer, ForeignKey("job_boards.id"),  nullable=False)
  job_board = relationship("JobBoard")
  is_open = Column(Boolean, nullable=False, default=True)

class JobApplication(Base):
  __tablename__ = 'job_applications'
  id = Column(Integer, primary_key=True)
  job_post_id = Column(Integer, ForeignKey("job_posts.id"),  nullable=False)
  job_post = relationship("JobPost")
  first_name = Column(String, nullable=False)
  last_name = Column(String, nullable=False)
  email = Column(String, nullable=False)
  resume_url = Column(String, nullable=False)