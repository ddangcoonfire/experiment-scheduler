import uuid


class ExperimentExecutor:
    def __init__(self):
        """
        experiment_pool calls ExperimentExecutor with resource information.
        Information is saved here.
        """
        self.id = uuid.uuid4()

    def _trigger_runner(self):
        """
        trigger new runner by grpc request to task manager
        trigger new runner by grpc_master request to task manager
        :return: runner's id
        """
        return self.id


    def execute(self):
        """
        call _trigger_runner
        save request to some data
        :return:
        """
        pass
