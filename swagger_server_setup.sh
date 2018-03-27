docker run --rm -v ${PWD}:/local swaggerapi/swagger-codegen-cli generate -i \
./local/account_service/swagger/account_service_api.yaml -l python-flask -o /local/swagger_codegen

cp -r swagger_codegen/swagger_server ./account_service_venv/lib/python3.6/site-packages/
