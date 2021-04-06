# Grid Demo | cats-and-dogs
In this demo example, you'll train a classifier on the classic cats and dogs dataset. 

If you haven't already set up the Grid CLI, follow this [1 minute guide](https://app.gitbook.com/@grid-ai/s/grid-cli/start-here/typical-workflow-cli-user#step-0-install-the-grid-cli) on how to install the Grid CLI.

**TLDR:** 
`pip install lightning-grid --upgrade`

`grid login`

## Overview 
This example involves three steps: 
1. Downloading the dataset from Kaggle
2. Uploading the data to Grid using datastores
3. Training the `run.py` script on the `cats_and_dogs` dataset

## Download the datatset
First, you'll need to download the cats and dogs dataset and remove the 1590 corrupt images that unfortunately are shipped with the dataset from Microsoft.

```
python get_data.py
```
## Upload data to Grid
Now that you have some data, let's upload that as a Grid Datastore

```
grid datastores create --source cats_and_dogs_data/PetImages --name cats-and-dogs-ds
```

Here the `--source` represents the path to the data which will be uploaded. The `--name` will be used as the datastore name in Grid. 

## Submit a training run with Grid**

Training Parameters
Here are the parameters we'll specify to `grid train`:

**Grid flags:**
1. **--grid_name:** specifies a name for your training run
2. **--grid_instance_type:** defines number of GPUs and memory
3. **--grid_gpus:** the number of GPUs per experiment
4. **--grid_datastore_name:** the name of the datastore (created above) that you'd like to attach to this training run
5. **--grid_datastore_version:** the version of the datatstore to attach to this training run (defaults to 1)

Then we'll specify the script we're using to train our model followed by the script arguments. 

**Script:** `run.py`

These are the arguments defined by the `run.py` script:

**Script arguments:**
1. data_dir
2. gpus
3. precision
4. max_epochs

Cool! Now we can spin up a Grid Train run.

Submit the command below: 

```
grid train  \
  --grid_name cats-v-dogs \
  --grid_instance_type g3.4xlarge  \
  --grid_gpus 1  \
  --grid_datastore_name cats-and-dogs-ds\
  --grid_datastore_version 1 \
  run.py \
  --data_dir /opt/datastore \
  --gpus 1 \
  --precision 16 \
  --max_epochs 10
```
You can use the `grid status` command to check on the status of the run. To view progess in the Grid UI, use `grid view`. 
