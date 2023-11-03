# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# ¬¬¬NOTE FOR FUTURE MAINTAINERS¬¬¬
# We're importing the various Airflow-descended modules inside the test
# functions because Airflow performs a lot of setup on first setup, including
# polluting the user's $HOME. We want to avoid this setup until we've got
# various temp folders in place - hence imports inside fixtures + tests

from pendulum import datetime
import os
import pytest
from approvaltests.approvals import verify
from contextlib import nullcontext as does_not_raise
from itertools import combinations
from conftest import TEST_NOTEBOOK_DIR, TEST_STATIC_DIR, TEST_TEMPLATE_DIR

from flowpytertask import (
    BadParameterError,
)  # I don't think this will violate the above....

TASK_ID = "test_task"
EXECUTION_DATE = datetime(2023, 1, 29)


@pytest.fixture()
def default_folder_params(tmp_out_dir, tmp_data_dir):
    yield {
        "host_notebook_dir": str(TEST_NOTEBOOK_DIR),
        "host_data_dir": str(tmp_data_dir),
        "host_notebook_out_dir": str(tmp_out_dir),
    }


@pytest.fixture
def base_dag(dag_setup, default_folder_params):
    from airflow import DAG

    dag = DAG(
        start_date=EXECUTION_DATE,
        dag_id="simple_test_dag",
        schedule="@daily",
        catchup=False,
        default_args=default_folder_params,
    )

    def failure_callback(context):
        pytest.fail("DAG did not run to completion")

    dag.on_failure_callback = failure_callback
    return dag


@pytest.fixture()
def fp_op_with_defaults(default_folder_params):
    from flowpytertask import FlowpyterOperator

    class FpOpWithDefaults(FlowpyterOperator):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **default_folder_params, **kwargs)

    yield FpOpWithDefaults


def test_dag(base_dag, tmp_out_dir, default_folder_params: dict):
    """
    Tests the dag runs to the end
        Caution - if there is something wrong with the callback invocation, this test will show passing
    """
    from flowpytertask import FlowpyterOperator

    FlowpyterOperator(notebook_name="test_nb.ipynb", dag=base_dag, task_id="first_task")
    run = base_dag.test(
        execution_date=EXECUTION_DATE,
    )

    run.get_task_instance(task_id="first_task")
    assert (
        tmp_out_dir
        / "2023-01-29"
        / "simple_test_dag__first_task__manual__2023-01-29T00:00:00+00:00"
        / "simple_test_dag__first_task__manual__2023-01-29T00:00:00+00:00__test_nb.ipynb"
    ).exists()


def test_parameterised_dag(base_dag, tmp_out_dir, fp_op_with_defaults):
    """
    Tests the dag runs to the end
        Caution - if there is something wrong with the callback invocation, this test will show passing
    """
    fp_op_with_defaults(
        dag=base_dag,
        task_id="first_task",
        notebook_name="test_nb.ipynb",
        nb_params={"input": "DEADBEEF"},
    )
    run = base_dag.test(
        execution_date=EXECUTION_DATE,
    )

    run.get_task_instance(task_id="first_task")
    assert (
        "DEADBEEF"
        in (
            tmp_out_dir
            / "2023-01-29"
            / "simple_test_dag__first_task__manual__2023-01-29T00:00:00+00:00"
            / "simple_test_dag__first_task__manual__2023-01-29T00:00:00+00:00__test_nb.ipynb"
        ).read_text()
    )


def test_local_import(base_dag, tmp_out_dir, fp_op_with_defaults):
    """
    Tests that a notebook can import a local utils file
    """
    fp_op_with_defaults(
        dag=base_dag,
        task_id="first_task",
        notebook_name="dependency_nb.ipynb",
    )
    run = base_dag.test(
        execution_date=EXECUTION_DATE,
    )

    run.get_task_instance(task_id="first_task")
    assert (
        "DEADBEEF"
        in (
            tmp_out_dir
            / "2023-01-29"
            / "simple_test_dag__first_task__manual__2023-01-29T00:00:00+00:00"
            / "simple_test_dag__first_task__manual__2023-01-29T00:00:00+00:00__dependency_nb.ipynb"
        ).read_text()
    )


def test_static_asset_mount(base_dag, tmp_out_dir, fp_op_with_defaults):
    """
    Tests static asset injection runs correctly
    """
    fp_op_with_defaults(
        dag=base_dag,
        task_id="first_task",
        notebook_name="static_nb.ipynb",
        read_only_mounts={"static_dir": str(TEST_STATIC_DIR)},
    )
    run = base_dag.test(
        execution_date=EXECUTION_DATE,
    )

    run.get_task_instance(task_id="first_task")
    assert (
        "DEADBEEF"
        in (
            tmp_out_dir
            / "2023-01-29"
            / "simple_test_dag__first_task__manual__2023-01-29T00:00:00+00:00"
            / "simple_test_dag__first_task__manual__2023-01-29T00:00:00+00:00__static_nb.ipynb"
        ).read_text()
    )


def test_dependency_dag(base_dag, tmp_out_dir, fp_op_with_defaults):
    first_nb = fp_op_with_defaults(
        dag=base_dag,
        task_id="first_task",
        notebook_name="glue_nb.ipynb",
        nb_params={"artifact_out": "test_artifact.txt"},
    )
    second_nb = fp_op_with_defaults(
        dag=base_dag,
        task_id="second_task",
        notebook_name="read_nb.ipynb",
        nb_params={"artifact_in": "test_artifact.txt"},
    )
    first_nb >> second_nb

    base_dag.test(execution_date=EXECUTION_DATE)

    out_path = (
        tmp_out_dir
        / "2023-01-29"
        / "simple_test_dag__second_task__manual__2023-01-29T00:00:00+00:00"
        / "simple_test_dag__second_task__manual__2023-01-29T00:00:00+00:00__read_nb.ipynb"
    )
    assert "DEADBEEF" in out_path.read_text()


def test_ipynb_check(base_dag, tmp_out_dir, fp_op_with_defaults):
    from flowpytertask import NotebookExtensionError

    with pytest.raises(NotebookExtensionError):
        _ = fp_op_with_defaults(
            dag=base_dag, task_id="fail_task", notebook_name="test_nb"
        )


def test_reserved_param_check(base_dag, fp_op_with_defaults):
    from flowpytertask import ReservedParameterError

    with pytest.raises(ReservedParameterError):
        _ = fp_op_with_defaults(
            dag=base_dag,
            task_id="fail_task",
            notebook_name="test_nb.ipynb",
            nb_params={"data_dir": "should_not_pass"},
        )


param_cases = [
    ("space param", True),
    ("class", True),  # Reserved word param check
    (5, True),  # Non-string param check
    ("a_fine_param", False),
    ("another_fine_param", False),
]


def param_factory():
    for combination in combinations(param_cases, 2):
        params, is_bad = zip(*combination)
        if any(is_bad):
            scenario = pytest.raises(BadParameterError)
        else:
            scenario = does_not_raise()
        yield {p: "dummy_param_value" for p in params}, scenario


@pytest.mark.parametrize(("param_dict", "expectation"), param_factory())
def test_bad_nb_param_check(param_dict, expectation):
    from flowpytertask import FlowpyterOperator

    with expectation:
        FlowpyterOperator._injected_key_check(param_dict)


def test_bad_param_dag(base_dag, default_folder_params):
    from flowpytertask import FlowpyterOperator, BadParameterError

    with pytest.raises(BadParameterError):
        FlowpyterOperator(
            dag=base_dag,
            task_id="bad_param_task",
            **default_folder_params,
            notebook_name="test_nb.ipynb",
            nb_params={"no good": "dummy"}
        )


def test_bad_mount_dag(base_dag, default_folder_params):
    from flowpytertask import FlowpyterOperator, BadParameterError

    with pytest.raises(BadParameterError):
        FlowpyterOperator(
            dag=base_dag,
            task_id="bad_param_task",
            **default_folder_params,
            notebook_name="test_nb.ipynb",
            read_only_mounts={"no good": "dummy"}
        )


def test_template_operator(base_dag, tmp_data_dir, default_folder_params):
    """
    Tests the template operator
    """
    from flowpytertask import FlowpyterOperator

    FlowpyterOperator(
        dag=base_dag,
        task_id="first_task",
        **default_folder_params,
        notebook_name="template_nb.ipynb",
        nb_params={"test_var": "DEADBEEF"},
        read_only_mounts={"template_dir": str(TEST_TEMPLATE_DIR)}
    )
    run = base_dag.test(
        execution_date=EXECUTION_DATE,
    )

    run.get_task_instance(task_id="first_task")
    rendered_template = (
        tmp_data_dir
        / "2023-01-29"
        / "simple_test_dag__manual__2023-01-29T00:00:00+00:00"
        / "example_template_rendered.html"
    ).read_text()
    assert "DEADBEEF" in rendered_template
    verify(rendered_template)


def test_make_dir_with_docker(monkeypatch, tmp_path, base_dag):
    import flowpytertask
    from flowpytertask import FlowpyterOperator

    monkeypatch.setattr(flowpytertask, "is_running_on_docker", lambda: True)

    foo = FlowpyterOperator(
        notebook_name="_.ipynb",
        host_notebook_dir="_",
        host_notebook_out_dir="_",
        host_data_dir="_",
        task_id="_",
    )
    foo.notebook_uid = os.getuid()
    foo.notebook_gid = os.getgid()
    foo.create_path_on_host(tmp_path, "new_file")
    assert (tmp_path / "new_file").exists()
