"""
    QuaO Project quao_qiskit_provider.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
from qiskit_aer import Aer

from ...config.logging_config import logger
from ...model.provider.quao_provider import QuaoProvider


class QuaoQiskitProvider(QuaoProvider):
    def get_backend(self, device_specification):
        logger.debug('[Quao Qiskit] Get backend')

        provider = self.collect_provider()

        device_names = set(map(self.__map_aer_backend_name, provider.backends()))

        if device_names.__contains__(device_specification):
            return provider.get_backend(device_specification)

        raise Exception('Unsupported device')

    def collect_provider(self):
        logger.debug('[Quao Qiskit] Connect to provider')

        return Aer

    @staticmethod
    def __map_aer_backend_name(backend):
        return backend.configuration().backend_name
