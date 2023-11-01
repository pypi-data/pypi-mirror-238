"""
    QuaO Project quao_qiskit_device.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""

from qiskit import transpile, QiskitError

from ...config.logging_config import logger
from ...data.device.circuit_running_option import CircuitRunningOption
from ...model.device.quao_device import QuaoDevice


class QuaoQiskitDevice(QuaoDevice):
    def _create_job(self, circuit, options: CircuitRunningOption):
        logger.debug('[Quao Qiskit] Create job with {0} shots'.format(options.shots))

        self.device.set_options(device=options.processing_unit.value,
                                shots=options.shots,
                                executor=options.executor,
                                max_job_size=options.max_job_size)
        transpiled_circuit = transpile(circuits=circuit, backend=self.device)

        return self.device.run(transpiled_circuit)

    def _produce_histogram_data(self, job_result) -> dict:
        logger.debug('[Quao Qiskit] Produce histogram')

        try:
            histogram_data = job_result.get_counts()
        except QiskitError as qiskit_error:
            logger.debug("Can't produce histogram with error: {0}".format(str(qiskit_error)))
            histogram_data = None

        return histogram_data

    def _get_provider_job_id(self, job) -> str:
        logger.debug('[Quao Qiskit] Get provider job id')

        return job.job_id()

    def _get_job_status(self, job) -> str:
        logger.debug('[Quao Qiskit] Get job status')

        return job.status().name

    def _calculate_execution_time(self, job_result):
        logger.debug('[Quao Qiskit] calculate execution time')

        if "metadata" not in job_result:
            return None

        metadata = job_result["metadata"]

        if (
                metadata is None
                or not bool(metadata)
                or "time_taken_execute" not in metadata
        ):
            return None

        self.execution_time = metadata["time_taken_execute"]

        logger.debug('[Quao Qiskit] Execution time calculation was: {0} seconds'
                     .format(self.execution_time))
