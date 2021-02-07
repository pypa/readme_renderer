language: python
python: 3.6

matrix:
  include:
    - python: 2.7
      env: TOXENV=py27
    - python: 3.5
      env: TOXENV=py35
    - python: 3.6
      env: TOXENV=py36
    - python: 3.7
      env: TOXENV=py37
      dist: xenial
    - python: 3.8
      env: TOXENV=py38
      dist: xenial
    - python: 3.9-dev
      env: TOXENV=py39
      dist: xenial
    - python: pypy
      env: TOXENV=pypy
    - env: TOXENV=pep8
    - python: 2.7
      env: TOXENV=py2pep8
    - env: TOXENV=packaging
    - python: 3.6
      env: TOXENV=noextra

install: pip install tox

script: tox

notifications:
  irc:
    channels:
      - "irc.freenode.org#pypa-dev"
    use_notice: true
    skip_join: true
