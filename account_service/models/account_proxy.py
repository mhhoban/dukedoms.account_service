import json

from account_service.models.account import Account
from account_service.shared.db import get_new_db_session

class AccountProxy():
    """
    proxy object for manipulating Account db entries
    """

    def __init__(self, account_id):
        session = get_new_db_session()
        account = session.query(Account).filter(Account.id == account_id).first()

        self.account_id = account_id
        self.email = account.email
        self.active_player_ids = json.loads(account.active_player_ids)['active_player_ids']
        self.pending_player_ids = json.loads(account.pending_player_ids)['pending_player_ids']
        self.game_invitations = json.loads(account.game_invitations)['game_invitation_ids']

        session.close()

    def get_account_info(self):
        return {
            'email': self.email,
            'accountId': self.account_id,
            'activePlayerIds': self.active_player_ids,
            'pendingPlayerIds': self.pending_player_ids,
            'gameInvitations': self.game_invitations
        }

    def add_pending_player_id(self, player_id):
        self.pending_player_ids.append(player_id)

        session = get_new_db_session()
        session.query(Account).filter(Account.id == self.account_id).update(
            {'pending_player_ids': json.dumps({'pending_player_ids': self.pending_player_ids})}
        )
        session.commit()
        session.close()
