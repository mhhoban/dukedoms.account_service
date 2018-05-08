from account_service.shared.oas_clients import game_service_client

def send_invite_accept(game_id=None, player_email=None, account_id=None):
    """
    send player acceptance to game service and get welcome packet
    """
    result, status = game_service_client.gameOperations.accept_invite(
        gameInviteAcceptance={
            'gameId': game_id,
            'playerEmail': player_email,
            'accountId': account_id
        }
    ).result()
    return result


def send_invite_decline(game_id=None, player_email=None, account_id=None):
    """
    send player game rejection to game service
    """
    result, status = game_service_client.gameOperations.decline_invite(
        gameInviteRejection={
            'gameId': game_id,
            'playerEmail': player_email,
            'accountId': account_id
        }
    ).result()
