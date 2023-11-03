# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import subprocess
from pathlib import Path
from time import sleep

import pytest
import os


@pytest.fixture()
def tmp_env_vars(monkeypatch, tmp_out_dir, tmp_data_dir):
    out = dict()

    # out["AIRFLOW_VAR_HOST_NOTEBOOK_DIR"] = conftest.TEST_NOTEBOOK_DIR
    # out["AIRFLOW_VAR_HOST_TEMPLATE_DIR"] = conftest.TEST_TEMPLATE_DIR
    # out["AIRFLOW_VAR_HOST_STATIC_DIR"] = conftest.TEST_STATIC_DIR
    out["HOST_NOTEBOOK_OUT_DIR"] = str(tmp_out_dir)
    out["HOST_DATA_DIR"] = str(tmp_data_dir)
    out["HOST_DAGS_DIR"] = str(Path(__file__).parent)
    out["NOTEBOOK_UID"] = str(os.getuid())
    out["NOTEBOOK_GID"] = str(os.getgid())
    yield out


@pytest.fixture()
def tmp_env_file(tmp_env_vars, tmp_path):
    out = (Path(__file__).parent / ".env").read_text()
    out += "\n".join(f"{key}={value}" for key, value in tmp_env_vars.items())
    (tmp_path / "tmp_env").write_text(out)
    print("injecting the following env file:")
    print(out)
    yield tmp_path / "tmp_env"


@pytest.fixture()
def celery_compose_path():
    yield Path(__file__).parent / "celery-compose.yml"


def poll_celery():
    print("Polling for celery containers...")
    try:
        result = subprocess.run(
            "docker compose ls", shell=True, capture_output=True, text=True
        ).stdout
        if not result:
            return False
        result_line = next((c for c in result.split("\n") if "celery-compose" in c), None)
        return "running(7)" in result_line
    except StopIteration:
        return False


@pytest.fixture()
def celery_compose_file(tmp_env_file, celery_compose_path):
    print("Starting celery worker")
    subprocess.run(
        f"docker compose --env-file {tmp_env_file} -f {celery_compose_path} -p fpt_int_test up --build --detach",
        shell=True,
    )
    timeout = 0
    while not poll_celery():
        timeout += 1
        sleep(3)
        if timeout >= 5:
            pytest.exit("Celery worker setup timed out")

    yield
    print("Stopping docker file ")
    subprocess.run(
        f"docker compose -f {celery_compose_path} -p fpt_int_test down --volumes",
        shell=True,
    )


def set_airflow_variable(key, value):
    subprocess.run("docker exec flowpyter_task_scheduler ")


def test_example_dag(celery_compose_file, tmp_out_dir):
    subprocess.run("docker exec flowpyter_task_scheduler airflow dags test example_dag", shell=True)
    assert len(list(tmp_out_dir.glob("**/*.ipynb"))) == 3
