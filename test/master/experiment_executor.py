from master.experiment_executor import ExperimentExecutor

test1 = ExperimentExecutor()
assert test1.toss_experiment()
assert test1._trigger_runner()