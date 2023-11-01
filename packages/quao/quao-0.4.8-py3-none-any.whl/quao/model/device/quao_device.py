"""
    QuaO Project quao_device.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
from abc import ABC

from ..device.device import Device
from ..provider.provider import Provider
from ...config.logging_config import logger


class QuaoDevice(Device, ABC):

    def __init__(self, provider: Provider,
                 device_specification: str):
        super().__init__(provider, device_specification)

    def _is_simulator(self) -> bool:
        logger.debug('[Quao] Get device type')

        return True

    def _calculate_execution_time(self, job_result):
        logger.debug('[Quao] Execution time calculation was: {0} seconds'
                     .format(self.execution_time))

    def _get_job_result(self, job):
        logger.debug('[Quao] Get job result')

        return job.result()
