# -*- coding: utf-8 -*-
import os
import logging
import core.beanstalk_utils as bs
from core.utils import powerup


logging.basicConfig()
logger = logging.getLogger('logger')
logger.setLevel(logging.INFO)


def get_default(data, key):
    return data.get(key, os.environ.get(key, None))


@powerup('create_es')
def handler(event, context):
    # get data
    dest_env = get_default(event, 'dest_env')
    dry_run = get_default(event, 'dry_run')

    if not dry_run:
        bs.add_es(dest_env)

    retval = {"type": "create_es",
              "id": dest_env,
              "dry_run": dry_run
              }

    return retval
