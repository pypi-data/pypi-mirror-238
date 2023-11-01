"""
    QuaO Project provider_factory.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
from ..enum.provider_tag import ProviderTag
from ..enum.sdk import Sdk
from ..model.provider.aws_braket_provider import AwsBraketProvider
from ..model.provider.ibm_cloud_provider import IbmCloudProvider
from ..model.provider.ibm_quantum_provider import IbmQuantumProvider
from ..model.provider.quao_braket_provider import QuaoBraketProvider
from ..model.provider.quao_qiskit_provider import QuaoQiskitProvider
from ..model.provider.quao_tytan_provider import QuaoTytanProvider


class ProviderFactory:
    @staticmethod
    def create_provider(provider_type: ProviderTag,
                        sdk: Sdk,
                        authentication: dict):
        """

        @param sdk:
        @param provider_type:
        @param authentication:
        @return:
        """

        if ProviderTag.QUAO_QUANTUM_SIMULATOR.__eq__(provider_type):
            if Sdk.QISKIT.__eq__(sdk):
                return QuaoQiskitProvider()

            if Sdk.BRAKET.__eq__(sdk):
                return QuaoBraketProvider()

            if Sdk.TYTAN.__eq__(sdk):
                return QuaoTytanProvider()

        if ProviderTag.IBM_QUANTUM.__eq__(provider_type):
            return IbmQuantumProvider(authentication.get("token"))

        if ProviderTag.IBM_CLOUD.__eq__(provider_type):
            return IbmCloudProvider(authentication.get("token"),
                                    authentication.get("crn"))

        if ProviderTag.AWS_BRAKET.__eq__(provider_type):
            return AwsBraketProvider(authentication.get("accessKey"),
                                     authentication.get("secretKey"),
                                     authentication.get("regionName"))

        raise Exception("Unsupported provider!")
