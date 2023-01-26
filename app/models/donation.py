from sqlalchemy import Column, ForeignKey, Integer, Text

from .base import CharityProjectAndDonation


class Donation(CharityProjectAndDonation):
    comment = Column(Text)
    user_id = Column(Integer, ForeignKey('user.id'))
