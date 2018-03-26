docker run --rm -v ${PWD}/account_service:/local swaggerapi/swagger-codegen-cli generate -i \
./local/swagger/dukedoms_account_service_api.yaml -l python-flask -o /local/swagger_codegen

touch account_service/swagger_codegen/__init__.py
