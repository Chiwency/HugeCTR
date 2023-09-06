# HPS Plugin for TensorRT Notebooks

This directory contains a set of Jupyter notebooks that demonstrate how to use the HPS plugin for TensorRT.

## Quickstart

The simplest way to run a one of our notebooks is with a Docker container.
A container provides a self-contained, isolated, and reproducible environment for repetitive experiments.
Docker images are available from the NVIDIA GPU Cloud (NGC).
If you prefer to build the HugeCTR Docker image on your own, refer to [Set Up the Development Environment With Merlin Containers](https://nvidia-merlin.github.io/HugeCTR/master/hugectr_contributor_guide.html#set-up-the-development-environment-with-merlin-containers).

### Pull the Container from NGC

Pull a container based on the modeling framework and notebook that you want to run.

To run the [demo_for_tf_trained_model.ipynb](demo_for_tf_trained_model.ipynb) notebook, pull the Merlin TensorFlow container:

```shell
docker pull nvcr.io/nvidia/merlin/merlin-tensorflow:23.02
```

To run the [demo_for_pytorch_trained_model.ipynb](demo_for_pytorch_trained_model.ipynb) notebook, pull the Merlin PyTorch container:

```shell
docker pull nvcr.io/nvidia/merlin/merlin-pytorch:23.02
```

To run the [demo_for_hugectr_trained_model.ipynb](demo_for_hugectr_trained_model.ipynb) notebook, pull the Merlin HugeCTR container:

```shell
docker pull nvcr.io/nvidia/merlin/merlin-hugectr:23.02
```

The HPS TensorRT plugin is installed in all the containers.

### Clone the HugeCTR Repository

Use the following command to clone the HugeCTR repository:

```shell
git clone https://github.com/NVIDIA-Merlin/HugeCTR
```

### Start the Jupyter Notebook

1. Launch the container in interactive mode (mount the HugeCTR root directory into the container for your convenience) by running the following command.

   ```shell
   docker run --runtime=nvidia --rm -it --cap-add SYS_NICE -u $(id -u):$(id -g) -v $(pwd):/hugectr -w /hugectr -p 8888:8888 nvcr.io/nvidia/merlin/<container-name>:23.02
   ```

2. Start Jupyter using these commands:

   ```shell
   cd /hugectr/hps_trt/notebooks
   jupyter-notebook --allow-root --ip 0.0.0.0 --port 8888 --NotebookApp.token='hugectr'
   ```

3. Connect to your host machine using the 8888 port by accessing its IP address or name from your web browser: `http://[host machine]:8888`

   Use the token available from the output by running the command above to log in. For example:

   `http://[host machine]:8888/?token=aae96ae9387cd28151868fee318c3b3581a2d794f3b25c6b`


## Notebook List

Here's a list of notebooks that you can run:

- [benchmark_tf_trained_large_model.ipynb](benchmark_tf_trained_large_model.ipynb): Provides the steps to benchmark the inference performance of the large model. The model is comprised of one 147GB embedding table and three fully connected layers, for which a TensorRT engine is built with the HPS plugin. Here are the performance metrics at batch size 4096 on different platforms:

| Platform | Interconnect between GPU and CPU | Average per-batch latency in usec @BZ=4096 |
| -------- | -------------------------------- | ---------------------------------- |
| A100-SXM4-80GB + 2 x AMD EPYC 7742 64-Core Processor (2TB CPU Memory) | PCIe Gen4 | 1396 |
| H100-SXM5-80GB + 2 x Intel Xeon Platinum 8480C 56-Core Processor (2TB CPU Memory) | PCIe Gen5 | 773 |
| H100-NVL-94GB + NVIDIA Grace 72-Core Processor (480GB CPU Memory) |  NVLink-C2C  | 210 |

- [demo_for_tf_trained_model.ipynb](demo_for_tf_trained_model.ipynb): Demonstrates how to train with TensorFlow and then build the HPS-integrated TensorRT engine for deployment. The multi-GPU deployment on Triton is demonstrated.

- [demo_for_pytorch_trained_model.ipynb](demo_for_pytorch_trained_model.ipynb): Demonstrates how to train with PyTorch and then build the HPS-integrated TensorRT engine for deployment.

- [demo_for_hugectr_trained_model.ipynb](demo_for_hugectr_trained_model.ipynb): Demonstrates how to train with HugeCTR and then build the HPS-integrated TensorRT engine for deployment.

## System Specifications

The specifications of the system on which each notebook can run successfully are summarized in the table. The notebooks are verified on the system below but it does not mean the minimum requirements.

| Notebook                                                                                   | CPU                             | GPU                                    | #GPUs | Author       |
| ------------------------------------------------------------------------------------------ | ------------------------------- | -------------------------------------- | ----- | ------------ |
| [demo_for_tf_trained_model.ipynb](demo_for_tf_trained_model.ipynb)                         | Intel(R) Xeon(R) CPU E5-2698 v4 @ 2.20GHz<br />512 GB Memory | Tesla V100-SXM2-32GB<br />32 GB Memory | 1     | Kingsley Liu |
| [demo_for_pytorch_trained_model.ipynb](demo_for_pytorch_trained_model.ipynb)               | Intel(R) Xeon(R) CPU E5-2698 v4 @ 2.20GHz<br />512 GB Memory | Tesla V100-SXM2-32GB<br />32 GB Memory | 1     | Kingsley Liu |
| [demo_for_hugectr_trained_model.ipynb](demo_for_hugectr_trained_model.ipynb)               | Intel(R) Xeon(R) CPU E5-2698 v4 @ 2.20GHz<br />512 GB Memory | Tesla V100-SXM2-32GB<br />32 GB Memory | 1     | Kingsley Liu |