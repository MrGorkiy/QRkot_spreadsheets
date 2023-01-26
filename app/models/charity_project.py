from sqlalchemy import Column, String, Text

from .base import CharityProjectAndDonation


class CharityProject(CharityProjectAndDonation):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
