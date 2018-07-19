#!/bin/bash
set -x

SERVICE_NAME="test"
DOC_URL="https://s3-eu-west-1.amazonaws.com/{{ cookiecutter.project_name.lower().replace(' ', '-') }}-{{ cookiecutter.cloudformation_resource_suffix.lower() }}-cfn/docs"

SWAGGER_UI_VERSION='3.17.3'
SWAGGER_UI_URL="https://github.com/swagger-api/swagger-ui/archive/v${SWAGGER_UI_VERSION}.zip"


echo "Install Curl"
apt-get update
apt-get install -y curl

echo "fetch swagger-ui"
curl -o swagger-ui.zip -L ${SWAGGER_UI_URL}
unzip swagger-ui.zip
rm swagger-ui.zip
mv swagger-ui-${SWAGGER_UI_VERSION} swagger-ui

# echo "Update API base url"
# sed -i "s#<<base_url_placeholder>>#${SERVICE_URL}#g" swagger.yaml

echo "remove api-docs endpoint from swagger file"
sed -i '/## API-DOCS ##/,/## END API-DOCS ##/d' swagger.yaml

echo "adding swagger-bami.yaml to swagger-ui"
cp swagger.yaml swagger-ui/dist

echo "replace path in index.html"
sed -i "s#http.*\.json#${DOC_URL}/swagger.yaml#g" swagger-ui/dist/index.html
sed -i "s#./swagger-ui.css#${DOC_URL}/swagger-ui.css#g" swagger-ui/dist/index.html
sed -i "s#./swagger-ui-bundle.js#${DOC_URL}/swagger-ui-bundle.js#g" swagger-ui/dist/index.html
sed -i "s#./swagger-ui-standalone-preset.js#${DOC_URL}/swagger-ui-standalone-preset.js#g" swagger-ui/dist/index.html

