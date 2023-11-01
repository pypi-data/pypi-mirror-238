"""
    QuaO Project ibm_cloud_provider.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_ibm_runtime.accounts import ChannelType

from ...enum.provider_tag import ProviderTag
from ...model.provider.provider import Provider
from ...config.logging_config import *


class IbmCloudProvider(Provider):

    def __init__(self, api_key, crn):
        super().__init__(ProviderTag.IBM_CLOUD)
        self.api_key = api_key
        self.crn = crn
        self.channel = 'ibm_cloud'

    def get_backend(self, device_specification: str):
        logger.debug('[IBM Cloud] Get backend')

        provider = self.collect_provider()

        return provider.get_backend(name=device_specification)

    def collect_provider(self):
        logger.debug('[IBM Cloud] Connect to provider')

        return QiskitRuntimeService(channel= self.channel,
                                    token=self.api_key,
                                    instance=self.crn)
