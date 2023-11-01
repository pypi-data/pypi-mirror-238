"""
    QuaO Project quao_provider.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
from abc import ABC

from ...enum.provider_tag import ProviderTag
from ...model.provider.provider import Provider


class QuaoProvider(Provider, ABC):
    def __init__(self):
        super().__init__(ProviderTag.QUAO_QUANTUM_SIMULATOR)
