# Experiment-Scheduler
Running Same Experiments is boring, Kuberenetes is hard to install.   
For whom needs easily usable multiple-experiment environment, here's <b>experiment-scheduler</b>

# About Experiment-Scheduler
Experiment-Scheduler is open-source, for automating repeated experiments.   
In some environments like where k8s is not supported, where you can only use is ssh servers with python, repeatedly running same experiments with different parameters would be annoying and boring.    
By minimum settings and minimum effort, we provide distributed multi-experiment environment without affecting your already-completed server setting.    
Our goal is make you only concentrate on experiment by providing easily, fastly constructable experiment tool.   

# Quick Start
## Installation
```shell
pip3 install experiment-scheduler
```
## Set address of master and task_manager 
(by default, it starts as local) <!-- must changed later -->
```python3
# experiment_scheduler.cfg
[default]
master_address = "localhost:50052"
task_manager_address = ["localhost:50051"]
```
## Write your own experiment yaml <!-- must added more detailed yaml -->
```yaml
# sample.yaml
name: sample
tasks:
- cmd: torch train --lr 0.01
  condition:
    gpu: 1
  name: hpo_1
- cmd: torch train --lr 0.02
  condition:
    gpu: 1
  name: hpo_2
```
## Run master and task manager
``` shell
exs init_master
exs init_task_manager
```

## Run experiement scheduler
```shell
exs run -f sample.yaml
```

# Roadmap

What we are going to work on from v0.1 on the next few months :
## Done
  - [ ] not yet
## In Progress
  - [ ] RUD on experiment   (Start: _Oct 3 2022_)
  - [ ] Register in Pypi (Start: _Oct 3 2022_)
  - [ ] Apply Celery (Start: _Oct 3 2022_)
  - [ ] All comments on codes for future docs (Start: _Oct 3 2022_)
  - [ ] More Specific yaml example (Start: _Oct 3 2022_)

## To Do

**Web Page for Experiment Tracking**

- Create Web Page Running on localhost to check current status of master, task_manager.    
- Home, Logs, Status, Experiments pages will be served.

**Autotesting for further development and dockerization**

