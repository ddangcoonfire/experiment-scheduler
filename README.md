# Experiment-Scheduler
Running Same Experiments is boring, Kuberenetes is hard to install.   
For whom needs easily usable multiple-experiment environment, here's <b>experiment-scheduler</b>

# About Experiment-Scheduler
Experiment-Scheduler is open-source to automate repeated experiments.   
Some environments like where k8s is not supported, where you can only use ssh servers with python, repeatedly running same experiments with different parameters would be annoying and boring.    
With minimum settings and minimum effort, we provide distributed multi-experiment environment without affecting your already-completed server setting.    
Our goal is to make you only concentrate on experiment by providing easily, fastly constructible experiment tool.   

![image](https://user-images.githubusercontent.com/17878758/216975570-f302f017-d9c8-43b4-a6ee-1ffbb054c1d2.png)


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
- cmd: echo "Hi" > ~/exs_test.txt 
  name: test1 
- cmd: echo "exs" >> ~/exs_test.txt
  name: test2
- cmd: python code_to_run.py
  name: test3
  files: ["code_to_run.py","data/to/run/with.parquet"] 
```
## Run master and task manager
Before using experiment-scheduler, you need to run master and task manager server. Run both servers by execute code below:
``` shell
exs init_master
exs init_task_manager
```

## Run experiement scheduler
```shell
exs execute -f sample.yaml
```
# How to write your own yaml file
Currently we support only a few reserved words. You can refer to all of them in below example.

```
name : This is an experiment name
tasks : list of tasks
    - cmd : sh command you want to run
      name : task name
      files : if task manager does not have files for running cmd, you can send it using this option
```

# exs [command] explanation
  - exs execute -f(--file) : Requests the execution of experiments. This command should be executed with the `-f(--file)` argument, which specifies the YAML file that describes the experiments.
  - exs delete -t(--task) or -e(--experiment) : Delete tasks. You can delete a specific task using the `-t(--task)` argument or delete an entire experiment using the `-e(--experiment)` argument.
  - exs list : Lists all experiments. To list a specific experiment, use the `-e(--experiment)` argument followed by the experiment ID. By default, the ID is truncated when displayed. To display the full ID, use the `-v(--verbose)` argument.
  - exs status : Retrieves the status of a task. This command requires the `-t(--task)` argument followed by the task ID.
  - exs init_master : Run master server. When executing the command, master server logs are printed continously. To run it as daemon, use `-d(--daemon)` argument.
  - exs init_task_manager : Runs a task manager server. If there are multiple servers, this command should be executed on each of them. Similar to the master server, the logs of the task manager server are printed by default. To run it as a daemon, use the `-d(--daemon)` argument.
  - exs edit -t(--task-id), -c(--cmd) :  Edits the command of a task. You need to provide the task ID using the -t(--task-id) argument and the new command to run using the -c(--cmd) argument.
  - exs log -t(--task) : Retrieves the logs of a specific task. This command requires the `-t(--task)` argument followed by the task ID. If you want to obtain a log file of the task, you can use the `-f(--file)` argument additionally.
  - exs compile_grpc (experimental) : Recompiles the current proto files. This command is intended for developers.

# How to set experiment_scheduler.cfg
Each server needs addresses to communicate with other servers. Although default setting exists, you can modify them.
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

We are no longer developing this project after v1.1.  
From v0.3, we've been :
## Done
  - [x] RUD on experiment 
  - [x] Register in Pypi 
  - [x] All comments on codes for future docs 
  - [x] Detailed README.md   
  - [x] Detailed --help command 
  - [x] Set local DB for master 
  - [x] Refined GPU selection algorithm 
  - [x] Additional yaml file syntax 
  - [x] Support multiple gRPC versions 
  - [x] Single execution for `exs execute` 
  - [x] Specify package version. 
  - [x] New command added `exs edit` and `exs log`
  - [x] Add logging for Master and Task Manager
  - [x] Add Progress Report
  - [x] Add more detailed test code
  - [x] Configure HA on Master, Task Manager
  - [x] Add `files` option for uploading local files
  - [x] Add dockerfile for simple on/off
## To Contribute
We are currently not maintaining this project. If you want to take this project as maintainer, please contact to "ddangcoonfire@gmail.com".

## Acknowledgement
This Project has been supported by <b>MODULABS</b> and <b>K-digital platforms</b>.

<img src = "https://github.com/ddangcoonfire/experiment-scheduler/assets/52615838/905c31ae-8caa-4f57-8253-a6484c6c2f51" width="35%" height="35%">
