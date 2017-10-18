# -*- coding: utf-8 -*-
import os
import logging
import core.beanstalk_utils as bs


logging.basicConfig()
logger = logging.getLogger('logger')
logger.setLevel(logging.INFO)


def get_default(data, key):
    return data.get(key, os.environ.get(key, None))


def handler(event, context):
    # get data
    item_id = get_default(event, 'id')
    dry_run = get_default(event, 'dry_run')
    logger.info("Attempting to create rds with event as %s" % (event))

    return event 
