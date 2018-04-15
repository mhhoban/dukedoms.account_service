#!/bin/bash

python setup.py bdist_wheel

account_service_wheel="dukedomsaccountservice-0.0.0-py3-none-any.whl"
swagger_wheel="swagger_server-1.0.0-py3-none-any.whl"

docker build --build-arg account_service_wheel=$account_service_wheel \
  --build-arg swagger_wheel=$swagger_wheel --tag 'mhhoban/dukedoms_account_service:latest' .
