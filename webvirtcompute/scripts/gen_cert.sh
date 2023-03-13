#!/usr/bin/env bash
set -e

openssl req -new -x509 -keyout server.pem -out server.pem -days 365 -nodes -subj "/C=EU/ST=Ukraine/L=Zaporozhye/O=webvirtcloud/CN=172.64.0.2"

exit 0
