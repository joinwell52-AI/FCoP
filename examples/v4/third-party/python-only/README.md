# Python-only unpublished RC demonstration

This directory is copyable outside FCoP's checkout. It uses only the installed
public `fcop.Project` and `fcop.errors.FcopError` interfaces plus Python's
standard library. Packaged rule data is read through importlib.resources.

Install the verified local `fcop-4.0.0rc1` wheel or sdist in a new venv.
Do not resolve the unpublished candidate from PyPI and do not use editable
installation or PYTHONPATH for acceptance.

The automated consumer runs `app.py hold <fresh-directory>`, waits for the
COMMITTED signal from the transport witness, kills that actual process, then
runs `app.py inspect <same-directory>` in a new interpreter. The directory must
be new, caller-owned and outside any existing workspace.

The example performs sequential completion, a one-level Branch family and
explicit convergence, response-loss retry, conflicting-operation rejection,
static Codex profile selection, missing/damaged/oversized rule rejection,
explicit adoption, a zero-write plan, deployment and rollback. It compares
persisted states, event chains, task/report/review bytes, family identity and
adopted/deployed rule context across process restart.

The trusted startup Profile is deliberately educational: a fixed demo string
is not production credential verification. Business requests never provide
their own evaluator. No Host discovery, network access or Runtime adoption
claim occurs. `runtime_consumption_verified` remains unknown.

`--source` exists only for explicitly labelled source parity checks. It does
not satisfy clean-room acceptance. This is an unpublished candidate example,
not an authorization to deploy into an existing project or to publish FCoP.
