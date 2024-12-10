IMAGE_NAME = turbmodel_opensuseleap156

build:
	docker build -t $(IMAGE_NAME) .

run:
	docker run --rm -it $(IMAGE_NAME)
