include .env
all: deps build publish

deps:
	yarn
build:
	yarn build
publish:
	aws lambda update-function-code \
		--function-name ${AWS_LAMBDA_TARGET} \
		--zip-file fileb://lambda-build.zip  \
		--publish

