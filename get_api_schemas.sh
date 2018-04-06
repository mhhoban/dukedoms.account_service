#!/bin/bash

curl https://raw.githubusercontent.com/mhhoban/dukedoms.account_service_spec/master/dukedoms_account_service_api.yaml -O

mv dukedoms_account_service_api.yaml account_service/swagger/account_service_api.yaml
