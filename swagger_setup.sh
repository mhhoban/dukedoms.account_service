#!/bin/bash

curl https://raw.githubusercontent.com/mhhoban/dukedoms.account_service_spec/master/dukedoms_account_service_api.yaml -O

mv dukedoms_account_service_api.yaml account_service/swagger/account_service_api.yaml

docker run --rm -v ${PWD}:/local swaggerapi/swagger-codegen-cli generate -i \
./local/account_service/swagger/account_service_api.yaml -l python-flask -o /local/swagger_codegen

cp -r swagger_codegen/swagger_server ./account_service_venv/lib/python3.6/site-packages/
