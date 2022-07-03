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
        trigger new runner

        :return: runner's id
        """
        return self.id

    def toss_experiment(self,target):
        """
        wake up new runner with params
        toss management of experiment to experiment_connector
        :param target: target experiment_connector
        :return: None
        """
        runner = self._trigger_runner()

    def execute(self):
        """
        run this class as daemon process
        :return:
        """
        pass
