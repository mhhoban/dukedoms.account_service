FROM python:3.6
ARG account_service_wheel
COPY ./dist/$account_service_wheel /$account_service_wheel
ARG swagger_wheel
COPY ./swagger_codegen/dist/$swagger_wheel /$swagger_wheel

ARG account_service_wheel
RUN pip3 install /$swagger_wheel && pip3 install /$account_service_wheel
ENV ACCOUNT_SERVICE_ENV=container
CMD ["python", "/usr/local/lib/python3.6/site-packages/account_service/account_service_server.py"]
