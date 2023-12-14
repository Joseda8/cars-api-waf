# Web Application Firewall
## _A simple implementation of a WAF to secure an API_

This project contains an implementation for a WAF using Python and its framework Flask, the service to be protected is built using NodeJS and Express. 

The WAF works as a proxy between the client and the service, if all the validations made by the WAF pass, then the request gets a green flag to reach the service.


# How to run

## API service

1. This API is a submodule that the user must download by running the next command:
```sh
git submodule update --init --recursive
```

2. Follow the README instructions inside `api-service\README.md`.

## WAF

Follow the instructions inside `waf\README.md`.
