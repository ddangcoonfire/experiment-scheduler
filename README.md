# Experiment-Scheduler
Running Same Experiments is boring, Kuberenetes is hard to install.   
For whom needs easily usable multiple-experiment environment, here's <b>experiment-scheduler</b>

# About Experiment-Scheduler
Experiment-Scheduler is open-source, for automating repeated experiments.   
In some environments like where k8s is not supported, where you can only use is ssh servers with python, repeatedly running same experiments with different parameters would be annoying and boring.    
By minimum settings and minimum effort, we provide distributed multi-experiment environment without affecting your already-completed server setting.    
Our goal is make you only concentrate on experiment by providing easily, fastly constructable experiment tool.   

![image](https://user-images.githubusercontent.com/17878758/216975570-f302f017-d9c8-43b4-a6ee-1ffbb054c1d2.png)


# Quick Start
## Installation
```shell
pip3 install experiment-scheduler
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
# How to write your own yaml file
Currently we support only a few reserved words. You can refer all of them in below example.

```
name : This is an experiment name
tasks : list of tasks
    - cmd : sh command you want to run
      name : task name
```

# exs [command] explanation
  - exs execute -f(--file) : Request experiments to run. You should execute it with `-f(--file)` argument which is the yaml file depicting experiments.
  - exs delete -t(--task) : Delete a single task. It needs `-t(--task)` argument.
  - exs list : list all experiment. To list specific experiment, use `-e(--experiment)` argument with experiment id. Id values are truncated by default. For non-truncated value, use `-v(--verbose)` argument.
  - exs status : Get status of tasks. It needs `-t(--task)` argument with task id.
  - exs init_master : Run master server. When executing the command, master server logs are printed continously. To run it as daemon, use `-d(--daemon)` argument.
  - exs init_task_manager : Run a task manager server. If there are more than one server, you need to execute it on each of them. Same as master, task manager server logs are printed as default. To run it as daemon, use `-d(--daemon)` argument.

# How to set experiment_scheduler.cfg
Each server needs address to communicate with other servers. Although default setting exists, you can modify them.
Currently, two elements are available:

  - master_address : "IP:port"
  - task_manager_address : ["IP:port", "IP:port", ...]

Experiement scheduler uses [ConfigParser](https://docs.python.org/3/library/configparser.html). So, you should write `[default]` at head. `task_manager_addresses` should be wrapped by square brackets even if you use a single node.

Below is default setting.

```
[default]
master_address = "localhost:50052"
task_manager_address = ["localhost:50051"]
```

# Roadmap

What we are going to work on from v0.3 on the next few months :
## Done
  - [x] RUD on experiment   (Start: _Oct 3 2022_, End: _Dec 31 2022_)
  - [x] Register in Pypi (Start: _Oct 3 2022_, End: _Dec 31 2022_)
  - [x] All comments on codes for future docs (Start: _Oct 3 2022_, End: _Dec 31 2022_)
  - [x] Detailed README.md (_Feb 6 2023_)
## In Progress
  - [ ] Detailed --help command (Start: _Feb 6 2023_)
  - [ ] Set local DB for master  (Start: _Feb 6 2023_)
  - [ ] Refined GPU selection algorithm (Start: _Feb 6 2023_)
  - [ ] Additional yaml file syntax (Start: _Feb 6 2023_)
  - [ ] Support multiple gRPC versions (Start: _Feb 6 2023_)
  - [ ] Single execution for `exs excute` (Start: _Feb 6 2023_)
  - [ ] Specify package version. (Start: _Feb 6 2023_)

## To Do
  - Support multi node environment (v0.4)
  - Improve test code coverage (v0.4)
  - Detailed error log (v0.4)

**Web Page for Experiment Tracking**

- Create Web Page Running on localhost to check current status of master, task_manager.    
- Home, Logs, Status, Experiments pages will be served.

**Autotesting for further development and dockerization**

