"""
    QuaO Project quao_tytan_provider.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
from tytan.sampler import SASampler, GASampler

from ...config.logging_config import logger
from ...model.provider.quao_provider import QuaoProvider


class QuaoTytanProvider(QuaoProvider):

    def get_backend(self, device_specification):
        logger.debug('[Quao Tytan] Get backend')

        backend = self.collect_provider().get(device_specification)

        if backend is None:
            raise Exception('Unsupported device')

        return backend

    def collect_provider(self):
        logger.debug('[Quao Tytan] Connect to provider')

        return {
            'SASampler': SASampler(),
            'GASampler': GASampler()
        }
