ARG VARIANT=3.13
ARG PYTHON_VERSIONS="3.9 3.10 3.11 3.12 3.13"
FROM mcr.microsoft.com/vscode/devcontainers/python:${VARIANT}

# Install tox
RUN pipx install tox

# Install pyenv
USER vscode
WORKDIR /home/vscode

RUN curl -fsSL https://pyenv.run | bash
ENV PYENV_ROOT="/home/vscode/.pyenv"
ENV PATH="$PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH"

RUN pyenv install 3.9 3.10 3.11 3.12 3.13
RUN pyenv local "${PYTHON_VERSIONS}"
RUN pyenv global ${VARIANT}

# Modify dotfile
RUN echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
RUN echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
RUN echo 'export PATH="$PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
RUN echo 'export PATH="$PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
RUN echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
RUN echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.zshrc

# Restore root user
USER root
