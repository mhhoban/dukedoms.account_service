from bravado.client import SwaggerClient
from bravado.swagger_model import load_file

from account_service.constants import URLS

config = {
    'also_return_response': True,
    'validate_responses': True,
    'validate_requests': True,
    'validate_swagger_spec': True,
    'use_models': True,
    'formats': []
}

if os.environ.get('ACCOUNT_SERVICE_ENV') == 'local':
    env = 'local'
else:
    env= 'container'

game_service_client = SwaggerClient.from_spec(
    load_file(
        'swagger/dukedoms_game_service_api.yaml',
    ),
    origin_url=context.env_urls.game_service,
    config=config
)
