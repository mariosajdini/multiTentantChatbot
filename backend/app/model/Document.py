from sqlalchemy import Column, Integer, String, Float, ARRAY
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Document(Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    vector = Column(ARRAY(Float), nullable=False)
    metadata = Column(String, nullable=True)

    def __repr__(self):
        return f"<Document(id={self.id}, content='{self.content[:50]}...', metadata='{self.metadata}')>"
