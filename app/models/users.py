from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..db import Base
from ._many_to_many import user_likes
from ._table_name_provider import TableNameProvider


class User(Base, TableNameProvider):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False)
    auth = Column(String, nullable=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    founder_id = Column(Integer, ForeignKey("founder.id"), nullable=True)
    investor_id = Column(Integer, ForeignKey("investor.id"), nullable=True)
    verified_email = Column(Boolean)
    verification_code = Column(Integer)
    authentication_string = Column(String)
    liked_projects = relationship(
        "Project",
        secondary=user_likes,
        back_populates="liked_by",
    )
