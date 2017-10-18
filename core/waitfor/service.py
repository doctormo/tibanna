# -*- coding: utf-8 -*-
import os
import logging
import core.beanstalk_utils as bs
from core.utils import powerup


logging.basicConfig()
logger = logging.getLogger('logger')
logger.setLevel(logging.INFO)


class WaitingForBoto3(Exception):
    pass


def get_default(data, key):
    return data.get(key, os.environ.get(key, None))


@powerup
def handler(event, context):
    # get data
    item_id = get_default(event, 'id')
    boto3_type = get_default(event, 'type')
    dry_run = get_default(event, 'dry_run')

    checkers = {'snapshot': bs.is_snapshot_ready,
                'rds': bs.is_db_ready,
                'rds_delete': bs.is_db_delete_done,
                'create_es': bs.is_es_ready}
    # TODO: rds_delete

    if dry_run:
        logger.warn("Dry Run - would have called %s : %s with %s" %
                    (checkers[boto3_type], boto3_type, item_id))
        status = True
        details = "dry_run"
    else:
        status, details = checkers[boto3_type](item_id)
    if not status:
        raise WaitingForBoto3("not ready yet")

    event['waitfor_details'] = details
    return event
