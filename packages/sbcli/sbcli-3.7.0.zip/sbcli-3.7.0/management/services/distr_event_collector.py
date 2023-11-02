# coding=utf-8
import logging
import os

import time
import sys


SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(SCRIPT_PATH, "../.."))

from management import constants, kv_store, utils, rpc_client, storage_node_ops
from management.controllers import events_controller


# configure logging
logger_handler = logging.StreamHandler(stream=sys.stdout)
logger_handler.setFormatter(logging.Formatter('%(asctime)s: %(levelname)s: %(message)s'))
logger = logging.getLogger()
logger.addHandler(logger_handler)
logger.setLevel(logging.DEBUG)

# get DB controller
db_controller = kv_store.DBController()


def process_event(event_id):
    event = db_controller.get_events(event_id)[0]
    if event.event == "device_status":
        if event.message == 'SPDK_BDEV_EVENT_REMOVE':
            node_id = event.node_id
            storage_id = event.storage_id

            nodes = db_controller.get_storage_nodes()
            device_id = None
            device_node_id = None
            for node in nodes:
                for dev in node.nvme_devices:
                    if dev.cluster_device_order == storage_id:
                        if dev.status != "online":
                            logger.info(f"The storage device is not online, skipping. status: {dev.status}")
                            return
                        device_id = dev.get_id()
                        device_node_id = node.get_id()
                        break
            if device_node_id != node_id:
                logger.info(f"The storage device not on this node, skipping. device node: {device_node_id}")
            else:
                if device_id:
                    logger.info(f"Removing storage id: {storage_id} from node: {node_id}")
                    storage_node_ops.device_remove(device_id)
                    event.status = 'processed'
                else:
                    logger.info(f"Device not found!, storage id: {storage_id} from node: {node_id}")
                    event.status = 'device_not_found'
            event.write_to_db(db_controller.kv_store)

        # if event.message == 'error_read':
        # if event.message == 'error_write':
        # if event.message == 'error_unmap':
        # if event.message == 'error_open':



hostname = utils.get_hostname()
logger.info("Starting Distr event collector...")
logger.info(f"Node:{hostname}")
while True:
    time.sleep(constants.DISTR_EVENT_COLLECTOR_INTERVAL_SEC)

    snode = db_controller.get_storage_node_by_hostname(hostname)
    if not snode:
        logger.error("This node is not part of the cluster, hostname: %s" % hostname)
        continue

    client = rpc_client.RPCClient(
        snode.mgmt_ip,
        snode.rpc_port,
        snode.rpc_username,
        snode.rpc_password)

    events = client.distr_status_events_get()
    logger.info(f"Found events: {len(events)}")
    event_ids = []
    for ev in events:
        logger.debug(ev)
        event_type = ev['event_type']
        status = ev['status']
        ev_id = events_controller.log_distr_event(snode.cluster_id, snode.get_id(), event_type, ev, status)
        event_ids.append(ev_id)

    for eid in event_ids:
        logger.info(f"Processing event: {eid}")
        process_event(eid)
