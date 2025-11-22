IMAGE_VERSION = 0.1.0
IMAGE_NAME = image_name
CONTAINER_NAME = container_name
REPO_URL = repo_url

build:
	docker build --platform linux/amd64 -t ${REPO_URL}/${IMAGE_NAME}:${IMAGE_VERSION} .

run:
	docker run -d --rm --platform linux/amd64 --name ${CONTAINER_NAME} -p 3000:3000 ${REPO_URL}/${IMAGE_NAME}:${IMAGE_VERSION}

stop:
	docker stop ${CONTAINER_NAME}

push:
	@make build
	docker push ${REPO_URL}/${IMAGE_NAME}:${IMAGE_VERSION}

test:
	@make build
	@make -i stop
	@make run