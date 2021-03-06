"""
test functions related to getting the output of a job.
"""

import os
import re
import json
import shutil
import tempfile

from pytest import raises, mark
import unittest.mock as mock
from requests_mock import Mocker

from .decorators import request_context
from .fixtures import demo_app as app  # flake8: noqa
from routes import JobOutputApi, JobStatusApi
import operations

from posixpath import join


MIDDLEWARE_URL = "http://middleware:5000"


@request_context(
    "/job/1/status",
    method="PATCH",
    content_type="application/json",
    data='{"status":"FINALIZING"}',
)
def test_get_token(app):
    with Mocker() as m:
        m.put(MIDDLEWARE_URL + "/job/1/status", json="data")
        # thread hangs if the following is not mocked
        operations.post.check_create_blob_container = mock.MagicMock(
            return_value="openfoam-test-output"
        )
        result = JobStatusApi().dispatch_request(1)
        print(result)
        assert result["status"] == 200
        assert result["data"]["token"] is not None
        assert result["data"]["container"] is not None


@request_context(
    "/job/2/status",
    method="PATCH",
    content_type="application/json",
    data='{"status":"COMPLETED"}',
)
def test_job_completed(app):

    with Mocker() as m:

        status_url = join(MIDDLEWARE_URL, "job/2/status")
        output_url = join(MIDDLEWARE_URL, "job/2/output")

        m.put(status_url, json="mock")
        m.post(output_url, json="mock")
        result = JobStatusApi().dispatch_request(2)
        assert result["status"] == 200


@mark.skip("Assumes existing connection to middleware")
@request_context("/job/3/output", method="GET")
def test_get_output(app):
    result = JobOutputApi().dispatch_request(3)
    assert len(result) == 1
    assert "type" in result[0].keys()
    assert "destination" in result[0].keys()
