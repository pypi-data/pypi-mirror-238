"""
    QuaO Project quao_braket_provider.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
from braket.devices import LocalSimulator

from ...config.logging_config import logger
from ...model.provider.quao_provider import QuaoProvider


class QuaoBraketProvider(QuaoProvider):
    def get_backend(self, device_specification):
        logger.debug('[Quao Braket] Get backend')

        provider = self.collect_provider()

        device_names = provider.registered_backends()

        if device_names.__contains__(device_specification):
            return LocalSimulator(device_specification)

        raise Exception('Unsupported device')

    def collect_provider(self):
        logger.debug('[Quao Braket] Connect to provider')

        return LocalSimulator()
