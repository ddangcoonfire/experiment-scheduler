from experiment_scheduler.db_util import Session
from experiment_scheduler.db_util.experiment import Experiment
from experiment_scheduler.db_util.task import Task


if __name__ == "__main__":
    print(Experiment.get(id == "1").name)
    task_temp = Task.get(id=3)
    print(type(task_temp))

    with Session() as session:
        task_temp.command = "hello"
        session.commit()

    print(Task.get(id=3).command)
