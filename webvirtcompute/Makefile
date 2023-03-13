# Copyright 2022 WebVirtCloud
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

TAG ?= dev
IMAGE ?= webvirtcompute

.PHONY: build
build:
	@echo "==> Building the docker image"
	@docker build --no-cache --platform linux/amd64 -f Dockerfile -t $(IMAGE):$(TAG) .

.PHONY: compile
compile:
	@if [ ! `docker images $(IMAGE):$(TAG) -q` ]; then\
		echo "==> Build docker image first";\
		exit 1;\
	fi
	@echo "==> Compile binary"
	@docker run --rm -it --platform linux/amd64 -v $(PWD)/src:/src -w /src $(IMAGE):$(TAG) bash -c \
		"/usr/local/bin/pyinstaller -p /src --hiddenimport main -F webvirtcompute.py"
	@echo "==> Binary compiled"

.PHONY: package
package:
	@if [ ! -d src/dist ]; then\
		echo "==> Compile the app first";\
		exit 1;\
	fi
	@cp conf/webvirtcompute.ini src/dist/
	@cp conf/webvirtcompute.service src/dist/
	@if [ ! -d release ]; then\
		mkdir release;\
	fi
	@docker run --rm -it --platform linux/amd64 -v $(PWD):/app -w /app $(IMAGE):$(TAG) bash -c \
		"cd src; tar -czf ../release/webvirtcompute-rockylinux8-amd64.tar.gz --transform s/dist/webvirtcompute/ dist"
	@echo "==> Package archived to release directory"

.PHONY: test
test:
	@echo "==> Start testing"
	@docker run --rm -it --platform linux/amd64 -v $(PWD)/src:/src -w /src $(IMAGE):$(TAG) flake8
	@echo "==> Testing complited"

.PHONY: clean
clean:
	@rm -rf release src/build src/dist src/__pycache__ src/webvirtcompute.spec
	@echo "==> Cleaned"
