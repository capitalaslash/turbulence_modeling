OPENSUSE_IMAGE = turbmodel_opensuseleap156
UBUNTU_IMAGE = turbmodel_ubuntu2204

build_opensuse:
	docker build -f Dockerfile_OpenSUSE -t $(OPENSUSE_IMAGE) .

build_ubuntu:
	docker build -f Dockerfile_Ubuntu -t $(UBUNTU_IMAGE) .

run_opensuse:
	docker run --rm -it $(OPENSUSE_IMAGE)

run_ubuntu:
	docker run --rm -it $(UBUNTU_IMAGE)

