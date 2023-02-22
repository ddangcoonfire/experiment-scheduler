from sqlalchemy import select
from experiment_scheduler.db_util import Session
from experiment_scheduler.db_util.Experiment import Experiment
from experiment_scheduler.db_util.Task import Task
from experiment_scheduler.db_util.util import select_all_experiments, select_all_tasks, select_experiment_by_id, \
    select_tasks_by_exp_id, select_task_by_id

if __name__ == '__main__':

    for row in select_all_experiments():
        print("----------------------------")
        print(row.id)
        print(row.name)
        print(row.created_at)
        print(row.last_updated_date)
        print(row.tasks)
        print("----------------------------")

    # print(select_all_tasks())
    test1 = select_experiment_by_id("3")
    print("----------------------------")
    print(test1.id, test1.name, test1.created_at)
    print("----------------------------")

    for row in select_tasks_by_exp_id("10"):
        print("----------------------------")
        print(row.id)
        print(row.name)
        print(row.created_at)
        print(row.last_updated_date)
        print("----------------------------")

    print(select_task_by_id("task_5"))
    test2 = select_task_by_id("task_5")
    print("----------------------------")
    print(test2.id, test2.name, test2.created_at)
    print("----------------------------")
    # session = Session()
    #
    # newTask1 = Task(
    #     id='task_10',
    #     name='task_name_1',
    #     command='test',
    #     status='status',
    #     task_manager_address='local',
    #     task_logfile_path='file',
    # )
    # newTask2 = Task(
    #     id='task_11',
    #     name='task_name_2',
    #     command='test',
    #     status='status',
    #     task_manager_address='local',
    #     task_logfile_path='file',
    # )
    # newExp = Experiment(
    #     id = 10,
    #     name = 'test',
    #     tasks = [newTask1, newTask2]
    # )
    #
    # session.add(newExp)
    # session.commit()
    #
    # stmt = select(Experiment)
    # result = session.execute(stmt)
    # for row in result.fetchone():
    #     print(f"{row.id} {row.name} {row.created_at} {row.last_updated_date} {row.tasks}")