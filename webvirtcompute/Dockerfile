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

FROM rockylinux:8

COPY src /src

RUN dnf install -y epel-release && \
    dnf install -y python3-pip \
                   python3-lxml \
                   python3-devel \
                   python3-jinja2 \
                   python3-libvirt \
                   python3-paramiko \
                   python3-firewall \
                   python3-libnmstate \
                   python3-libguestfs

RUN python3 -m pip install -U pip wheel setuptools && \
    python3 -m pip install -r /src/requirements/build.txt
