from addict import Dict

URLS = Dict()
URLS.local.rdbs = 'postgresql+psycopg2://postgres:daleria@localhost:5432/account_service'
URLS.container.rdbs = 'postgresql+psycopg2://postgres:daleria@dukedoms-rdbs:5432/account_service'

URLS.local.game_service = 'http://127.0.0.1:5003'
URLS.container.game_service='http://game-service:5003'
