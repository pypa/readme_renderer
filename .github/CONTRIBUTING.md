# Contributing

The following is a set of guidelines for contributing to this project.
These are just guidelines, not rules.
Use your best judgment, and feel free to propose changes to this document in a pull request.

## Development Setup

### The Easy Way

Use the supplied [Development Container](https://containers.dev/) configuration
to get a development environment up and running quickly.
The configurations can be found in the `.devcontainer` directory.

[GitHub Codespaces](https://github.com/features/codespaces) can provide
a development environment in the cloud.
GitHub Codespaces also provides a prebuilt image for this repository
from the most recent commit on the `main` branch
to speed up the setup process, including many of the Python runtimes
and tools needed to run the tests.

Other tools like Visual Studio Code may use the devcontainer configuration
to provide a consistent development environment locally,
if you have a compatible version of a container runtime.

### The Less-Easy Way

1. Fork the repository and clone it to your local machine.
1. Install any Python runtimes you wish to test against.
1. Install the `tox` test runner

Note: You may need other development tools depending on the environment you are working in.

## Running Tests

Once started up, in a shell, run `tox -l` to see the available test environments.
To run the tests, use `tox -e <environment>`
where `<environment>` is one of the environments listed by `tox -l`.

Alternatively, you can run `tox` without any arguments to run all the tests.

### Parallel Testing

To run all Python tests in parallel on all available CPUs:

    tox -p auto

Read more about [parallel mode](https://tox.wiki/en/latest/user_guide.html#parallel-mode).

## Testing Guidelines

TODO: Explain test fixtures and how to create/update them.
