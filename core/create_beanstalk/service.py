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


def process_overrides(event):
    '''tries to find the values we need in _overrides
    assume _overrides to be list of objects
    '''
    # lookups is dict mapping override type to the field that stores
    # the information we want, to the name the field should be in events
    lookups = {'create_rds': ['waitfor_details', 'db_endpoint'],
               'create_es': ['waitfor_details', 'es_url'],
               }

    rides = event.get('_overrides')
    if rides and not isinstance(rides, basestring):
        for item in rides:
            if item:
                lookup = lookups.get(item.get('type'))
                if lookup:
                    event[lookup[1]] = item.get(lookup[0])
    return event


@powerup('create_beanstalk')
def handler(event, context):
    event = process_overrides(event)
    logger.info("after processing")
    logger.info(event)

    dest_env = get_default(event, 'dest_env')
    db_endpoint = get_default(event, 'db_endpoint')
    es_url = get_default(event, 'es_url')
    dry_run = get_default(event, 'dry_run')
    load_prod = get_default(event, 'load_prod')

    if not dry_run:
        res = bs.create_bs(dest_env, load_prod, db_endpoint, es_url)
        logger.info(res)

    retval = {"type": "create_bs",
              "id": dest_env,
              "dry_run": dry_run
              }

    return retval
