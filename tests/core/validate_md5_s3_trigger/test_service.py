from core.validate_md5_s3_trigger.service import handler as validate_md5_s3_trigger
from core.validate_md5_s3_trigger.service import make_input
# from core.validate_md5_s3_trigger.service import STEP_FUNCTION_ARN
import pytest
from ..conftest import valid_env
from datetime import datetime
import mock


def test_build_req_parameters(s3_trigger_event_data):
    params = make_input(s3_trigger_event_data)
    assert params['app_name'] == 'md5'
    input_file = params['input_files'][0]
    assert input_file['bucket_name'] == 'elasticbeanstalk-fourfront-webprod-files'
    assert input_file['object_key'] == '4DNFIXH5OV2H.fastq.gz'
    assert input_file['uuid'] == '74ccc209-564d-49d1-ab87-b5b10a3db92f'


@valid_env
@pytest.mark.webtest
def test_s3_trigger_e2e(s3_trigger_event_data):
    # set a unique name for results, as we will be using same data over and over
    s3_trigger_event_data['run_name'] = "testrun_%s" % datetime.now().strftime("%Y%m%d%H%M%S%f")

    # force this thing to not run, so I don't get the new workflow run
    with mock.patch('core.validate_md5_s3_trigger.service.is_status_uploading') as uploading:
        uploading.return_value = False
        ret = validate_md5_s3_trigger(s3_trigger_event_data, None)
        assert ret
        assert ret['info'] == 'status is not uploading'
