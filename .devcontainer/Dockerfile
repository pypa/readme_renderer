FROM ghcr.io/astral-sh/uv:trixie-slim

# uv writes to UV_PYTHON_INSTALL_DIR/.temp and UV_CACHE_DIR during install
# operations, and the runtime user has to be able to write there too. We
# can't chown to a fixed UID — devcontainer's `updateRemoteUserUID` remaps
# vscode to the host user's UID at start — so the parent dirs get sticky-bit
# world-write, the UID-agnostic version of /tmp.
#
# /opt locations are chosen because:
#   - UV_TOOL_DIR: the uv image defaults to /root/.local/share/uv/tools,
#     which is unreadable to non-root users (/root is mode 700).
#   - UV_CACHE_DIR: lives somewhere devcontainer.json can persist via a
#     named Docker volume across rebuilds.
ENV UV_PYTHON_INSTALL_DIR=/opt/python \
    UV_TOOL_DIR=/opt/uv/tools \
    UV_CACHE_DIR=/opt/uv/cache

# Pre-install the CPython interpreters the tox matrix uses, plus tox
# itself (with tox-uv for fast env creation). --default makes 3.14 the
# system `python` / `python3`.
#
# PyPy is intentionally omitted: nh3's Rust extension has no prebuilt
# PyPy wheel for aarch64 and source builds fail. CI still tests PyPy
# on x86_64 where wheels exist.
ARG PYTHON_VERSIONS="3.10 3.11 3.12 3.13 3.14"
RUN uv python install --default 3.14 \
    && uv python install ${PYTHON_VERSIONS} \
    && uv tool install tox --with tox-uv \
    # The build populated /opt/python/.temp and /opt/uv/cache as root.
    # Clear both: uv recreates .temp at runtime under the new perms, and
    # an empty cache lets the named volume initialize cleanly on first
    # mount (otherwise root-owned wheels get copied into it).
    && rm -rf /opt/python/.temp /opt/uv/cache \
    && mkdir -p /opt/uv/cache \
    && chmod 1777 /opt/python /opt/uv/cache
