"""
    QuaO Project backend.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""

from ..callback.update_job_metadata import update_job_metadata
from ...async_tasks.export_circuit_task import CircuitExportTask
from ...component.device.device_selection import DeviceSelection
from ...config.logging_config import logger
from ...config.thread_config import circuit_exporting_pool
from ...config.thread_config import circuit_running_pool
from ...data.async_task.circuit_export.backend_holder import BackendDataHolder
from ...data.async_task.circuit_export.circuit_holder import CircuitDataHolder
from ...data.backend.backend_information import BackendInformation
from ...data.device.circuit_running_option import CircuitRunningOption
from ...data.request.invocation_request import InvocationRequest
from ...data.response.authentication import Authentication
from ...data.response.job_response import JobResponse
from ...data.response.project_header import ProjectHeader
from ...enum.invocation_step import InvocationStep
from ...enum.media_type import MediaType
from ...enum.sdk import Sdk
from ...enum.status.job_status import JobStatus
from ...enum.status.status_code import StatusCode
from ...factory.device_factory import DeviceFactory
from ...factory.provider_factory import ProviderFactory
from ...util.circuit_utils import CircuitUtils


class Invocation:
    def __init__(self, request_data: InvocationRequest):
        self.sdk: Sdk = Sdk.resolve(request_data.sdk)
        self.input = request_data.input
        self.device_id = request_data.device_id
        self.backend_information: BackendInformation
        self.authentication: Authentication = request_data.authentication
        self.project_header: ProjectHeader = request_data.project_header
        self.options = CircuitRunningOption(shots=request_data.shots,
                                            processing_unit=request_data.processing_unit,
                                            executor=circuit_running_pool,
                                            max_job_size=1)
        self.device_selection_url: str = request_data.device_selection_url
        self.circuit_export_url: str = request_data.circuit_export_url
        self.callback_dict: dict = {
            InvocationStep.PREPARATION: request_data.preparation,
            InvocationStep.EXECUTION: request_data.execution,
            InvocationStep.ANALYSIS: request_data.analysis,
            InvocationStep.FINALIZATION: request_data.finalization
        }

    def submit_job(self, circuit_preparation_fn, post_processing_fn):
        """

        @param post_processing_fn: Post-processing function
        @param circuit_preparation_fn: Circuit-preparation function
        @return: Job result
        """
        logger.debug("[Invocation] Invoke job")

        circuit = self.__pre_execute(circuit_preparation_fn)

        if circuit is None:
            return

        self.__execute(circuit, post_processing_fn)

    def __pre_execute(self, circuit_preparation_fn):
        """

        @param circuit_preparation_fn: Circuit preparation function
        """
        circuit = self.__prepare_circuit(circuit_preparation_fn)

        if circuit is None:
            return None

        self.__prepare_backend_data(circuit)

        if not Sdk.TYTAN.__eq__(self.sdk):
            self.__export_circuit(circuit)

        return circuit

    def __execute(self, circuit, post_processing_fn):
        """

        @param circuit: Circuit was run
        @param post_processing_fn: Post-processing function
        @return: Job response
        """

        logger.debug('[Invocation] Execute job')

        try:
            if self.backend_information is None:
                raise Exception("Backend is not found")

            device_name = self.backend_information.device_name
            provider_tag = self.backend_information.provider_tag
            backend_authentication = self.backend_information.authentication

            logger.debug('[Invocation] Execute job with provider tag: {0}'.format(provider_tag.value))
            provider = ProviderFactory.create_provider(
                provider_type=provider_tag,
                sdk=self.sdk,
                authentication=backend_authentication)

            logger.debug('[Invocation] Execute job with device name: {0}'.format(device_name))
            device = DeviceFactory.create_device(provider=provider,
                                                 device_specification=device_name,
                                                 authentication=backend_authentication,
                                                 sdk=self.sdk)

        except Exception as exception:
            job_response = JobResponse(job_status=JobStatus.ERROR.value,
                                       content_type=MediaType.APPLICATION_JSON,
                                       status_code=StatusCode.ERROR,
                                       authentication=self.authentication,
                                       project_header=self.project_header,
                                       job_result={"error": str(exception)})
            update_job_metadata(
                job_response=job_response,
                callback_url=self.callback_dict.get(InvocationStep.EXECUTION).on_error)

            return

        device.run_circuit(circuit=circuit,
                           post_processing_fn=post_processing_fn,
                           options=self.options,
                           callback_dict=self.callback_dict,
                           authentication=self.authentication,
                           project_header=self.project_header)

    def __prepare_circuit(self, circuit_preparation_fn):
        """

        @param circuit_preparation_fn: Circuit preparation function
        @return: circuit
        """
        logger.debug("[Invocation] Prepare circuit")

        job_response = JobResponse(status_code=StatusCode.DONE,
                                   authentication=self.authentication,
                                   project_header=self.project_header)
        update_job_metadata(
            job_response=job_response,
            callback_url=self.callback_dict.get(InvocationStep.PREPARATION).on_start)

        try:
            circuit = circuit_preparation_fn(self.input)

            if circuit is None:
                raise Exception("Invalid circuit")

            update_job_metadata(
                job_response=job_response,
                callback_url=self.callback_dict.get(InvocationStep.PREPARATION).on_done)

            return circuit

        except Exception as exception:
            job_response.job_result = JobStatus.ERROR.value
            job_response.content_type = MediaType.APPLICATION_JSON
            job_response.status_code = StatusCode.ERROR
            job_response.job_result = {"error": str(exception)}

            update_job_metadata(
                job_response=job_response,
                callback_url=self.callback_dict.get(InvocationStep.PREPARATION).on_error)

            return None

    def __prepare_backend_data(self, circuit):
        """

        @param circuit: Circuit was run
        """

        required_qubit_amount = CircuitUtils.get_qubit_amount(circuit)

        device_selection = DeviceSelection(required_qubit_amount,
                                           self.device_id,
                                           self.authentication.user_token,
                                           self.device_selection_url)

        self.backend_information = device_selection.select()

    def __export_circuit(self, circuit):
        """

        @param circuit: Circuit was exported
        """

        circuit_export_task = CircuitExportTask(
            circuit_data_holder=CircuitDataHolder(circuit, self.circuit_export_url),
            backend_data_holder=BackendDataHolder(self.backend_information,
                                                  self.authentication.user_token))

        circuit_exporting_pool.submit(circuit_export_task.do)
