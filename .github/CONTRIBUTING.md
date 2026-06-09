# Contributing

Thanks for considering a contribution. Bug reports, fixes, and additions
are all welcome.

## Development setup

### Devcontainer (recommended)

This repo ships a [devcontainer](https://containers.dev/) config in
`.devcontainer/`. Open the project in any tool that understands the
spec — VS Code's Dev Containers extension, GitHub Codespaces, etc. — and
you get a container with [`uv`](https://docs.astral.sh/uv/), `tox` (with
`tox-uv`), and CPython 3.10–3.14 already installed.

GitHub Codespaces availability depends on your account or org's billing.

### Manual

If you'd rather set things up yourself:

1. Fork and clone the repo.
1. Install whichever Python versions you want to test against.
1. Install `tox`.

Depending on your platform you may need extra build tools — `nh3` and
`comrak` are Rust extensions and normally install from prebuilt wheels,
but source builds need a Rust toolchain.

## Running tests

`tox -l` lists the available environments. Run one with `tox -e py313`
(or whatever), or `tox` alone to run them all.

Parallel run across all CPUs:

```
tox -p auto
```

See the [tox parallel mode docs](https://tox.wiki/en/latest/user_guide.html#parallel-mode)
for details.
