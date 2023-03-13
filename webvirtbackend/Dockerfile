FROM rockylinux:9

EXPOSE 8000

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN dnf -y install epel-release && \
    dnf -y install gcc procps-ng findutils bash-completion net-tools telnet \
           python3 python3-devel glibc-langpack-en mariadb-connector-c-devel && \
    dnf clean all

COPY requirements/*.txt .

RUN python3 -m pip install -U pip wheel setuptools
RUN python3 -m pip install -r develop.txt

WORKDIR /app
COPY . /app

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "webvirtcloud.wsgi"]