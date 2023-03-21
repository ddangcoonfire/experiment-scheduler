from typing import Dict

from experiment_scheduler.db_util import Session
from experiment_scheduler.db_util.dao.experiment import Experiment
from experiment_scheduler.db_util.dao.task import Task
from sqlalchemy.orm import Query


class Mixin():

    def __init__(self):
        self._query = None

    def get_query(self, *args, **kwargs) -> Query:
        query = self._query or Session.query(self)
        return query

    def get(self, order_by:str = None, *args, **kwargs):
        query: Query = self.get_query(*args, **kwargs)
        query = query.filter(args) ## 조건문 자체를 args에 넘김
        query = query.filter_by(kwargs) ## a = 'b' kwargs 형태를 넘김

        if order_by:
            query = query.order_by(order_by)
        query.first()






    def convert_to_experiment(id: str, name: str):
        return Experiment(id = id, name = name)

    def convert_to_task(id: str, name: str, command: str, status: str, task_manager_address: str, task_logfile_path: str):
        return Task(
            id=id,
            name=name,
            command=command,
            status=status,
            task_manager_address=task_manager_address,
            task_logfile_path=task_logfile_path,
        )

    def create_experiment_with_tasks(exp: Experiment):
        session.add(exp)
        session.commit()

    def create_task(task: Task):
        session.add(task)
        session.commit()

    def update_experiment(exp_id: str, updated_dict: Dict):
        session.query(Experiment).filter(Experiment.id == exp_id).update(updated_dict)
        session.commit()

    def update_task(task_id: str, updated_dict: Dict):
        session.query(Task).filter(Task.id == task_id).update(updated_dict)
        session.commit()

    def select_all_experiments():
        return session.query(Experiment).all()

    def select_all_tasks():
        return session.query(Task).all()

    def select_experiment_by_id(exp_id: str):
        return session.query(Experiment).filter(Experiment.id == exp_id).one()

    def select_tasks_by_exp_id(exp_id: str):
        return session.query(Task).filter(Task.experiment_id == exp_id)

    def select_task_by_id(task_id: str):
        return session.query(Task).filter(Task.id == task_id).one()