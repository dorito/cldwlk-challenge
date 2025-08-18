#!/bin/sh

docker exec cldwlk-test-credit-manager-api alembic upgrade head
docker exec cldwlk-test-emotion-processor-api alembic upgrade head
docker exec cldwlk-test-public-gateway-api alembic upgrade head