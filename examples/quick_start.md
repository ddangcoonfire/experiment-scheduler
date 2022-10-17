# Quick Start

This quick start guide will help you learn how to use **experiment scheduler** with a small example.

If you have experienced conducting numerous experiments, you should know that it's annoying to execute command for every experiment you need to conduct. experiment scheduler is a tool for that situation. It help you execute commands for experiment easily.

Let's assume that we have a deep learning model and we need to optimizize hyper parameters of the model.
We select a grid search as optimization method and have four GPU resources which are needed to train model.
So, how should we use GPU resources efficiently?
Maybe we can divide grid space into four spaces and allocate each spaces to the GPU resources.
It looks so easy, right? But there are so many variables we can't see.
If some hyper parameter effects train time, then some part of grid space needs longer time than others.
Then how about estimate time and make each divided space use same time?
So we estimate time and calcuate how to divide search space and then, train models on each GPU resources.
But at that time, you relize that one GPU resource has smaller GPU memory so that it can't train our model.
That's so terrible.

But you don't worry about that with experiment scheduler.
You just need to make just single yaml file.
And then, experiment scheduler train models by checking resource and scheduling training by itself.

Let's take a look bellow yaml file.

```
# hp_optimization.yaml
name: hyper_parameter_optimization
resource:
- available_cuda: "0,1,2,3"

# tasks to execute are here
tasks:
- cmd: ./train_model.sh --lr 0.01 --bs 16
  condition:
    gpu: 1
  name: train_default_hp
- cmd: ./train_model.sh --lr 0.02 --bs 16
  condition:
    gpu: 1
  name: test_previous_best_hp
```

Let's look at each part in detail.

```
name: hyper_parameter_optimization
```

First, file has experiment name which it as first line.
experiment scheduler manage experiments by it's name.
So you can get a progress of experiments, stop it or edit experiments.
```
resource:
- available_cuda: "0,1,2,3"
```
At next line, resource information are written.
You can select which resource to use for the experimetns.

```
task:
- cmd: ./train_model.sh --lr 0.01 --bs 16
  condition:
    gpu: 1
  name: train_default_hp
  repitition: 3
```
task contains which commands and how to execute for optimization one by one.
What attributes means is as bellow.
- cmd : cmd is command to execute on terminal for experiments.
- condition : condition means requirment for execuing command. It could be resource or others.
- name : name is how single command is called. It's used for logging.

If you finish to write yaml file which depict how to run experiment,
you can run experiment by executing bellow command.

```
$ ~/ exs run hp_optimization.yaml
```

That's it. For now, experiment scheduler execute command if there are avilable resource for it.
What you need to do is just waiting until all experiment is done.
