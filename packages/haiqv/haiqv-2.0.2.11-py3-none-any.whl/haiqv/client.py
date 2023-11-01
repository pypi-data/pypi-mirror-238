import os
import json
import tempfile
import requests
import posixpath
import contextlib

from typing import Optional, Any

from .entities import run
from .error.value_error import HaiqvValueError
from .utils.files import guess_mime_type


# Notebook
def get_notebook_info(client_ip: str) -> Any:
    notebook_info = requests.get(f'{os.environ.get("_HAIQV_PLAT_URL")}/platform/resource/get-notebook-info?ip={client_ip}')

    if notebook_info.status_code == 200:
        return notebook_info.json()
    else:
        raise HaiqvValueError(notebook_info.text)


# Run
def create_run(exp_name: str, run_name: str, namespace: str, notebook_id: int, notebook_name: str, owner: str, owner_name: str) -> run.Run:
    data = {
        'exp_name': exp_name,
        'run_name': run_name,
        'namespace': namespace,
        'notebook_id': notebook_id,
        'notebook_name': notebook_name,
        'owner': owner,
        'owner_name': owner_name,
    }

    run_info = requests.post(f'{os.environ.get("_HAIQV_BASE_URL")}/experiment/run',
                             data=json.dumps(data),
                             headers={'Content-Type': 'application/json'})

    if run_info.status_code == 200:
        return run.Run(id=run_info.json()['run_id'], name=run_name)
    else:
        raise HaiqvValueError(run_info.text)


def update_run(
        run_id: str,
        status: Optional[str] = None,
        is_end: Optional[bool] = False,
) -> None:
    res = requests.post(f'{os.environ.get("_HAIQV_BASE_URL")}/experiment/run/update?run_id={run_id}&status={status}&is_end={is_end}')

    if res.status_code != 200:
        raise HaiqvValueError(res.text)


# Parameter
def log_param(run_id: str, key: str, value: Any) -> None:
    data = [
        {
            key: str(value)
        }
    ]
    res = requests.post(f'{os.environ.get("_HAIQV_BASE_URL")}/experiment/logging/batch-params?run_id={run_id}',
                        data=json.dumps(data),
                        headers={'Content-Type': 'application/json'})
    if res.status_code != 200:
        raise HaiqvValueError(res.text)


def log_params(run_id: str, data: Any) -> None:
    res = requests.post(f'{os.environ.get("_HAIQV_BASE_URL")}/experiment/logging/batch-params?run_id={run_id}',
                        data=json.dumps(data),
                        headers={'Content-Type': 'application/json'})
    if res.status_code != 200:
        raise HaiqvValueError(res.text)


# Metric
def log_metric(run_id: str, key: str, value: float, step: int) -> None:
    data = [
        {
            'key': key,
            'value': str(value),
            'step': step
        }
    ]
    res = requests.post(f'{os.environ.get("_HAIQV_BASE_URL")}/experiment/logging/batch-metrics?run_id={run_id}',
                        data=json.dumps(data),
                        headers={'Content-Type': 'application/json'})
    if res.status_code != 200:
        raise HaiqvValueError(res.text)


def log_metrics(run_id: str, data: Any) -> None:
    res = requests.post(f'{os.environ.get("_HAIQV_BASE_URL")}/experiment/logging/batch-metrics?run_id={run_id}',
                        data=json.dumps(data),
                        headers={'Content-Type': 'application/json'})
    if res.status_code != 200:
        raise HaiqvValueError(res.text)


# Artifact
def log_artifact(run_id: str, local_file: str, artifact_path: str) -> None:
    filename = os.path.basename(local_file)
    mime = guess_mime_type(filename)
    with open(local_file, 'rb') as f:
        res = requests.post(
            f'{os.environ.get("_HAIQV_BASE_URL")}/experiment/logging/artifacts?run_id={run_id}&artifact_path={artifact_path}',
            files={'local_file': (filename, f, mime)}
        )
        if res.status_code != 200:
            raise HaiqvValueError(res)


# Requirements
def log_requirements(run_id: str, text: str, requirement_file: str) -> None:
    with _log_artifact_helper(run_id, requirement_file) as tmp_path:
        with open(tmp_path, "w", encoding="utf-8") as f:
            f.write(text)


# metadata
def log_dataset_metadata(run_id: str, name: str, path: str, desc: str = None):
    res = requests.post(f'{os.environ.get("_HAIQV_BASE_URL")}/experiment/logging/metadata-dataset?run_id={run_id}&name={name}&path={path}&description={desc}',
                        headers={'Content-Type': 'application/json'})
    if res.status_code != 200:
        raise HaiqvValueError(res.text)


def log_model_metadata(run_id: str, name: str, path: str, step: int, volume_name: str, volume_path: str, metric: Optional[dict] = None):
    res = requests.post(f'{os.environ.get("_HAIQV_BASE_URL")}/experiment/logging/metadata-model?run_id={run_id}&name={name}&path={path}&step={step}&volume_name={volume_name}&volume_path={volume_path}',
                        data=json.dumps(metric),
                        headers={'Content-Type': 'application/json'})
    if res.status_code != 200:
        raise HaiqvValueError(res.text)


@contextlib.contextmanager
def _log_artifact_helper(run_id, artifact_file):
    norm_path = posixpath.normpath(artifact_file)
    filename = posixpath.basename(norm_path)
    artifact_dir = posixpath.dirname(norm_path)

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = os.path.join(tmp_dir, filename)
        yield tmp_path
        log_artifact(run_id, tmp_path, artifact_dir)

