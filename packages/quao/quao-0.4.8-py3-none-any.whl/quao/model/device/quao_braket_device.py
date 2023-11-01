"""
    QuaO Project braket_device.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""

from ...config.logging_config import logger
from ...data.device.circuit_running_option import CircuitRunningOption
from ...enum.status.job_status import JobStatus
from ...model.device.quao_device import QuaoDevice


class QuaoBraketDevice(QuaoDevice):
    def _create_job(self, circuit, options: CircuitRunningOption):
        logger.debug('[Quao Braket] Create job with {0} shots'.format(options.shots))

        import time

        start_time = time.time()

        job = self.device.run(task_specification=circuit, shots=options.shots)

        self.execution_time = time.time() - start_time

        return job

    def _produce_histogram_data(self, job_result) -> dict:
        logger.debug('[Quao Braket] Produce histogram')

        return dict(job_result.measurement_counts)

    def _get_provider_job_id(self, job) -> str:
        logger.debug('[Quao Braket] Get provider job id')

        return job.id

    def _get_job_status(self, job) -> str:
        logger.debug('[Quao Braket] Get job status')

        job_state = job.state()
        if JobStatus.COMPLETED.value.__eq__(job_state):
            job_state = JobStatus.DONE.value

        return job_state

