"""
    QuaO Project device_factory.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
from ..enum.provider_tag import ProviderTag
from ..enum.sdk import Sdk
from ..model.device.aws_braket_device import AwsBraketDevice
from ..model.device.ibm_cloud_device import IbmCloudDevice
from ..model.device.ibm_quantum_device import IbmQuantumDevice
from ..model.device.quao_braket_device import QuaoBraketDevice
from ..model.device.quao_qiskit_device import QuaoQiskitDevice
from ..model.device.quao_tytan_device import QuaoTytanDevice
from ..model.provider.provider import Provider


class DeviceFactory:
    @staticmethod
    def create_device(provider: Provider,
                      device_specification: str,
                      authentication: dict,
                      sdk: Sdk):
        """
        @param sdk:
        @param provider:
        @param device_specification:
        @param authentication:
        @return:
        """

        provider_type = ProviderTag.resolve(provider.get_provider_type().value)

        if ProviderTag.QUAO_QUANTUM_SIMULATOR.__eq__(provider_type):
            if Sdk.QISKIT.__eq__(sdk):
                return QuaoQiskitDevice(provider, device_specification)

            if Sdk.BRAKET.__eq__(sdk):
                return QuaoBraketDevice(provider, device_specification)

            if Sdk.TYTAN.__eq__(sdk):
                return QuaoTytanDevice(provider, device_specification)

        if ProviderTag.IBM_QUANTUM.__eq__(provider_type):
            return IbmQuantumDevice(provider, device_specification)

        if ProviderTag.IBM_CLOUD.__eq__(provider_type):
            return IbmCloudDevice(provider, device_specification)

        if ProviderTag.AWS_BRAKET.__eq__(provider_type):
            return AwsBraketDevice(provider,
                                   device_specification,
                                   authentication.get('bucketName'),
                                   authentication.get('prefix'))

        raise Exception("Unsupported device!")
