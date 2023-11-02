# loadingpy

In this repository, we provide a custom made progress bar for python iterables. This library can be used as is or modified for any purposes (see licence).

## Example
You can install with pip `pip install loadingpy` and use as follows

```python
from loadingpy import pybar

loss = 0.0
accuracy = 0.0
for inputs, labels in pybar(dataset, monitoring=[loss, accuracy], naming=["loss", "accuracy"], base_str="training"):
    # do whatever you please
    loss += 0.0 # update monitoring variables in place
    accuracy += 0.0 # update monitoring variables in place
```

For a more detailed exampel (in torch) check this [tutorial](https://gitlab.com/ey_datakalab/loadingpy/-/blob/main/notebooks/unit_test.ipynb). You can use a global argument in order to disable the verbatim from the loading bars as follows:

```python
from loadingpy import BarConfig

BarConfig["disable loading bar"] = True
```

## Arguments

Here is a list of the arguments and their description
| argument | description | type |
| :---: | :---: | :---: |
| iterable | python object that can be iterated over | can be a list, tuple, range, np.ndarray, torch.Tensor, dataset,... |
| monitoring | a python object (or list of python objects) that will be printed after each iteration using the following format f'{monitoring}'. IF they are updated during the loop, make sure to update inplace, in order to see the changes | an be a tensor, float or list of these |
| naming | if you want to add a descritpion prefix to the monitoring variables | str or list of str |
| total_steps | number of iterations to perform (if you set it to a lower value than the length of the iterable, then the process will stop after the given total_steps) | int |
| base_str | prefix description of the loop we are iterating over | str |
| color | which color to use for the loading bar | str |