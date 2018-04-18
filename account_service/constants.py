from addict import Dict

URLS = Dict()
URLS.local.rdbs = 'postgresql+psycopg2://dukedoms:daleria@localhost:5432/account_service'
URLS.container.rdbs = 'postgresql+psycopg2://dukedoms:daleria@dukedoms-rdbs:5432/account_service'

URLS.local.game_service = 'http://game-service:5000'
URLS.container.game_service='http://game-service:5000'
