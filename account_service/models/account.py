import json

from sqlalchemy import Column, Integer, JSON, String

from account_service.shared.db import Base

class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    email = Column(String(50))
    active_player_ids = Column(JSON)
    pending_player_ids = Column(JSON)
    game_invitations = Column(JSON)

    def __init__(self, email=None):
        self.email = email
        self.active_player_ids = json.dumps({'active_player_ids': []})
        self.pending_player_ids = json.dumps({'pending_player_ids': []})
        self.game_invitations = json.dumps({'game_invitation_ids': []})
