## Run

```
python extasy-analysis-gromacs.py --Wconfig settings/settings_extasy_chignolin_example.wcfg
```

## Configuration

Adjust values in the following items:

- WALLTIME: job walltime
- NODESIZE: number of compute nodes to request
- num_replicas: replica count, a number of concurrent task per iteration
- num_iterations: iteration count, total task = num_iterations * num_replicas

