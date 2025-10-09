FROM ubuntu:noble
ARG PYTHON_PACKAGES="python3.13 python3.12 python3.11 python3.10 python3.9 python3.9-distutils python3 python3-pip python3-venv pipx"
RUN apt-get update \
    && apt-get install --no-install-recommends -yq software-properties-common git \
    && add-apt-repository ppa:deadsnakes/ppa && apt-get update \
    && apt-get install -yq --no-install-recommends ${PYTHON_PACKAGES} \
    && pipx ensurepath \
    && pipx install tox
