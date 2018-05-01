"""
test functions related to getting the output of a job.
"""

import os
import re
import json
import shutil
import tempfile

from pytest import raises
import unittest.mock as mock

from .decorators import request_context
from .fixtures import demo_app as app  # flake8: noqa
from routes import JobStatusApi


def mock_put(target):
    """
    mock the request to the middleware.
    """
    return {"status": "Done"}, 200

@request_context("/job/1/status",
                 method="PATCH",
                 content_type='application/json',
                 data='{"job_status":"CLEANUP"}')
def test_get_token(app):
    with mock.patch('requests.put') as MockPut:
        result, status = JobStatusApi().dispatch_request(1)
        assert(status==200)
        assert(result["token"] is not None)
        assert(result["container"] is not None)
        

        
