---
url: https://rapids.ai/
tecnologia: RAPIDS
titulo: RAPIDS | GPU Accelerated Data Science
---

![](https://rapids.ai/images/rapids-logo-whitetxt.svg)

GPU Accelerated Data Science

[Quick Start](https://rapids.ai/#quick-start)

[New: cuML now accelerates scikit-learn](https://rapids.ai/cuml-accel) [New: Polars GPU Engine](https://rapids.ai/polars-gpu-engine) [cuDF now pre-installed in Google Colab](https://developer.nvidia.com/blog/rapids-cudf-instantly-accelerates-pandas-up-to-50x-on-google-colab/?ncid=em-news-294101) [Vector Search now with cuVS](https://rapids.ai/cuvs) [RAPIDS 26.06 Released](https://docs.rapids.ai/install#selector)

## What is RAPIDS

RAPIDS provides unmatched speed with familiar APIs that match the most popular PyData libraries.
Built on state-of-the-art foundations like [NVIDIA CUDA](https://developer.nvidia.com/cuda-toolkit) and [Apache Arrow](https://arrow.apache.org/), it unlocks the speed of GPUs with code you already know.
[Jump to About Section](https://rapids.ai/learn-more/#about)

## Why Use RAPIDS

RAPIDS allows fluid, creative interaction with data for everyone from BI users to AI researchers
on the
cutting edge. GPU acceleration means less time and less cost moving data and training models. [Jump to RAPIDS Use Cases](https://rapids.ai/learn-more/#use-cases)

## Open Source Ecosystem

RAPIDS is Open Source and available on [GitHub](https://github.com/rapidsai).
Our mission is to empower and advance the open-source GPU data science data engineering
ecosystem. [Jump to RAPIDS GitHub](https://github.com/rapidsai)

## Pandas Accelerator Mode for cuDF

Use cuDF pandas Accelerator Mode to speed up pandas workflows with zero code change.
[Learn More on the Accelerator Mode Page](https://rapids.ai/cudf-pandas)

## Polars GPU Engine powered by cuDF

Accelerate Polars by enabling the GPU engine with zero code change.
[Learn More on the Launch Page](https://rapids.ai/polars-gpu-engine)

## Accelerated scikit-learn with cuML

Run machine learning models faster with zero code change.
[Learn More on the Accelerated ML Page](https://rapids.ai/cuml-accel)

## NetworkX Supercharged by cuGraph

Speed up your large-scale graph workflows with zero code change.
[Learn More on the nx-cugraph Page](https://rapids.ai/nx-cugraph)

## Faster Pandas  with cuDF

cuDF accelerates pandas with zero code changes and brings greatly improved performance.

[Run this benchmark yourself](https://github.com/rapidsai/cudf/blob/release/26.06/docs/cudf/source/user_guide/performance-comparisons/performance-comparisons.ipynb)

\\* Benchmark on AMD EPYC 7642 (using 1x 2.3GHz CPU core) w/ 512GB and
NVIDIA A100 80GB (1x GPU) w/ pandas v1.5 and cuDF v23.02

## Faster scikit-learn  with cuML

cuML brings huge speedups to ML modeling with an API that matches scikit-learn.

[Run this benchmark yourself](https://github.com/rapidsai/cuml/tree/release/26.06/python/cuml/cuml/benchmark)

\\* Benchmark on AMD EPYC 7642 (using 1x 2.3GHz CPU core) w/ 512GB and
NVIDIA A100 80GB (1x GPU) w/ scikit-learn v1.2 and cuML v23.02

## Faster NetworkX  with cuGraph

cuGraph accelerates NetworkX with zero code changes for much greater performance at scale.

[Run this benchmark yourself](https://github.com/rapidsai/nx-cugraph/blob/release/26.06/benchmarks/pytest-based)

\\* Benchmark on Intel(R) Xeon(R) w9-3495X w/ 250 GB and
NVIDIA A100 80GB (1x GPU) w/ NetworkX v3.4.1 and cuGraph/nx-cugraph v24.10;
WCC = Weakly Connected Components; Betweenness = Betweenness Centrality with k=100

# Quick Start

## Quick Local Install

RAPIDS offers several installation methods, the quickest is shown below.

For more information, refer to the [RAPIDS Installation Guide](https://docs.rapids.ai/install)

### Requirements

**A.** NVIDIA Volta™ or higher GPU with [compute capability 7.0+](https://developer.nvidia.com/cuda-gpus)

**B.** [Compatible Linux distribution](https://docs.rapids.ai/install/#system-req) or [WSL2 on Windows 11](https://docs.rapids.ai/install#wsl2)

**C.** Recent [CUDA version _and_ NVIDIA driver pairs](https://docs.nvidia.com/deploy/cuda-compatibility/index.html). Check yours with:
`nvidia-smi`

See [System Requirements](https://docs.rapids.ai/install/#system-req) for details.

### Install with Conda

**1.** If not installed, download and run the install script.

This will install the latest miniforge:

```
wget "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-$(uname)-$(uname -m).shCopy
```

**2.** Then quick install RAPIDS with:

```
conda create -n rapids-26.06 -c rapidsai -c conda-forge rapids=26.06 python=3.14 cuda-version=13.1Copy
```

### Install with pip

Install via the NVIDIA PyPI index:

```
pip install \
  --extra-index-url=https://pypi.nvidia.com \
  cudf-cu13==26.6.* \
  dask-cudf-cu13==26.6.* \
  cuml-cu13==26.6.* \
  cugraph-cu13==26.6.*Copy
```

### Install with Docker

Check that you have the [required\\
environment](https://docs.rapids.ai/install#docker) and then use the [install selector](https://docs.rapids.ai/install#selector)

### Install on Windows

Use the Windows [WSL2 installation\\
instructions](https://docs.rapids.ai/install#wsl2)

## RAPIDS Release Selector

Please see the [RAPIDS Installation Guide](https://docs.rapids.ai/install)
for the interactive [release selector](https://docs.rapids.ai/install#install-rapids) with more options,
detailed installation steps, and information about supported platforms.

## Test Drive cuDF

Try out cuDF pandas Accelerator Mode, with a free required account, right now by [launching Google Colab](https://nvda.ws/3yW6j22)

## Try RAPIDS Online

Don't have access to a GPU system right now? Try out all of the RAPIDS libraries with cloud based hardware from one of
these featured channels:

![](https://rapids.ai/_partners/google-colab/logo_hua51de5e707d23163730ff965fb9bc91d_59545_200x0_resize_box_3.png)

### [Google CoLab](https://nvda.ws/3XEO6hK)

Jump right into a GPU enabled RAPIDS notebook environment with a free required account.

![](https://rapids.ai/_partners/amazon-studio-lab/logo_hu7bb3bcda4c006f38dd555958690e4676_43896_200x0_resize_box_3.png)

### [Studio Lab](https://studiolab.sagemaker.aws/)

Enables Amazon Sagemaker notebook based environments in a free trial with required account.

![](https://rapids.ai/_partners/paperspace/logo_hu52e9062176ecc43057f469332ab44125_146247_150x0_resize_box_3.png)

### [Paperspace](https://www.paperspace.com/gpu-cloud)

Use Quick Start Instances through a limited free account.

![](https://rapids.ai/_partners/nvidia-launchpad/logo_hud8b0fbb13efda001246ac6341ffda90d_80057_150x0_resize_box_3.png)

### [NVIDIA Launchpad](https://www.nvidia.com/en-us/launchpad/)

Free short term use to try and learn with hands-on lab environment.

![](https://rapids.ai/_partners/azure/logo_hufff5d38b3d7bf819a0e4d868e87e7a19_22729_150x0_resize_box_3.png)

### [Microsoft Azure](https://azure.microsoft.com/en-us/free/)

Microsoft Azure Cloud infrastructure and services are available with RAPIDS.

![](https://rapids.ai/_partners/oracle/logo_hu599f5c6cc86281b2677332807839282b_26206_150x0_resize_box_3.png)

### [Oracle Cloud](https://www.oracle.com/cloud/)

Oracle Cloud infrastructure and services are available with RAPIDS.

![](https://rapids.ai/_partners/ibm/logo_hu8e299e590191db01a0b820ff5eda479f_10550_150x0_resize_box_3.png)

### [IBM Cloud](https://www.ibm.com/cloud)

IBM Cloud infrastructure and services are available with RAPIDS.

## User Guides and Tutorials

After installing, the best place to start is by looking through our more detailed tutorials and
guides on the [User Guides Page](https://docs.rapids.ai/user-guide)

# Ecosystem

## Hardware

NVIDIA's industry leading hardware provides the platform for RAPIDS high performance. Get
details on the
newest GPUs, server architectures, and cloud offerings in our [Ecosystem\\
Hardware Section](https://rapids.ai/ecosystem)

## Software

Find out details on featured RAPIDS projects like cuDF, cuML, cuGraph, and more. Also learn about
those using our integrated with RAPIDS in our [Ecosystem\\
Software Section](https://rapids.ai/ecosystem#featured-software)

## Developers

Get involved with RAPIDS projects, reach out to its developers, find maintainer and contribution
guides
in our [Ecosystem Developers Section](https://rapids.ai/ecosystem#developers)

## Open Source

RAPIDS would not be possible without the collaboration of these important open source projects. Click on a logo to
learn more:

[![Apache Arrow Logo](https://rapids.ai/_partners/apache-arrow/logo_huf461f9d675a3f29d45a8820b3a8a849e_82572_100x0_resize_box_3.png)](https://github.com/apache/arrow)[![Dask Logo](https://rapids.ai/_partners/dask/logo_huc863545a5309a2b216a140b1702f9450_30807_100x0_resize_box_3.png)](https://github.com/dask/dask)[![NetworkX Logo](https://rapids.ai/_partners/networkx/logo_hub14d76c9070ad876c355e044e28e8d3c_104061_100x0_resize_box_3.png)](https://github.com/networkx/networkx)[![Nuclio Logo](https://rapids.ai/_partners/nuclio/logo_400x_hu2113be7198c878174e136cacd0217266_35345_100x0_resize_box_3.png)](https://github.com/nuclio/nuclio)[![Numba Logo](https://rapids.ai/_partners/numba/logo_hu91ddaf1ddc126b06cb9cfbcb7e4efa42_169187_100x0_resize_box_3.png)](https://github.com/numba/numba)[![scikit-learn Logo](https://rapids.ai/_partners/scikit-learn/logo_huaeb008173a1ad815e7a1f61a853a83f3_123104_100x0_resize_box_3.png)](https://github.com/scikit-learn/scikit-learn)[![XGBoost Logo](https://rapids.ai/_partners/xgboost/logo_hu19e7a5c0caf5925bd81ea752dd3f5fdb_62159_100x0_resize_box_3.png)](https://github.com/dmlc/xgboost)

## Adopters and Contributors

RAPIDS has a strong ecosystem of adopters and contributors in a variety of industries and communities. Click on a logo to learn more:

[![Anyscale Logo](https://rapids.ai/_partners/anyscale/logo_huaad2757d6a6e8159682bad327222d2d3_98158_100x0_resize_box_3.png)](https://github.com/anyscale)[![Booz Allen Hamilton Logo](https://rapids.ai/_partners/booz-allen-hamilton/logo_hu6f0d201140b014a3568a2d5791edf6a8_163999_100x0_resize_box_3.png)](https://github.com/boozallen)[![Databricks Logo](https://rapids.ai/_partners/databricks/logo_hu3a723687581b03bba0dd5e9275ae50c9_74392_100x0_resize_box_3.png)](https://github.com/databricks)[![Graphistry Logo](https://rapids.ai/_partners/graphistry/logo_hu66891bc6154a479967fb6538ed8e698e_48943_100x0_resize_box_3.png)](https://github.com/graphistry)[![H2O.ai Logo](https://rapids.ai/_partners/h2oai/logo_hudac23c277e0fa704e39c0c3f1b94d4a2_13605_100x0_resize_box_3.png)](https://github.com/h2oai)[![IBM Cloud Logo](https://rapids.ai/_partners/ibm/logo_hu8e299e590191db01a0b820ff5eda479f_10550_100x0_resize_box_3.png)](https://github.com/IBM-Cloud)[![Inria Logo](https://rapids.ai/_partners/inria/logo_hu1a51a7b60507fa98020ed7ebf8e6580b_40679_100x0_resize_box_3.png)](https://github.com/INRIA)[![Kinetica Logo](https://rapids.ai/_partners/kinetica/logo_hu75aaba25396c980bcdc112aa99fb38a9_27294_100x0_resize_box_3.png)](https://github.com/kineticadb)[![Paperspace Logo](https://rapids.ai/_partners/paperspace/logo_hu52e9062176ecc43057f469332ab44125_146247_100x0_resize_box_3.png)](https://github.com/Paperspace)

[![Plotly Dash Logo](https://rapids.ai/_partners/plotly-dash/logo_hu10e96c5a7ef1e52a16874b59b39b8f0d_18962_100x0_resize_box_3.png)](https://github.com/plotly)[![Preferred Networks Logo](https://rapids.ai/_partners/preferred-networks/logo_hub0362ad9cb152f1b10160e6b8177df8f_38680_100x0_resize_box_3.png)](https://github.com/pfnet)[![PyTorch Logo](https://rapids.ai/_partners/pytorch/logo_hu89fd5a4b873e7eb7108015b26d181bb7_89515_100x0_resize_box_3.png)](https://github.com/pytorch)[![Ray Logo](https://rapids.ai/_partners/ray/logo_hubef95826c958b4b09a244f4dc0625a7d_141196_100x0_resize_box_3.png)](https://github.com/ray-project)[![Saturn Cloud Logo](https://rapids.ai/_partners/saturn-cloud/logo_hu56c2e80637feb8e86d2d85726f6c9674_56303_100x0_resize_box_3.png)](https://github.com/saturncloud)[![Uber Logo](https://rapids.ai/_partners/uber/logo_hu0e3a4953b47c94693a897f35e340d3c3_73865_100x0_resize_box_3.png)](https://github.com/uber)[![Ursa Labs Logo](https://rapids.ai/_partners/ursa/logo_hu63506f7f7198b3a803f0917495d71c91_72166_100x0_resize_box_3.png)](https://github.com/ursa-labs)

[![Anaconda Logo](https://rapids.ai/_partners/anaconda/logo_hu6531123741a71905c15ea94082ad584e_39774_100x0_resize_box_3.png)](https://github.com/anaconda)[![Capital One Logo](https://rapids.ai/_partners/capital-one/logo_hu6827cd949949a519cde2bc006fa96e5e_171023_100x0_resize_box_3.png)](https://github.com/capitalone)[![Chainer Logo](https://rapids.ai/_partners/chainer/logo_hud6b4c2f74e84e543dd27b261f234be8a_72940_100x0_resize_box_3.png)](https://github.com/chainer)[![CuPy Logo](https://rapids.ai/_partners/cupy/logo_hu782ae4b4be96c79b8ce8c9b83d498e1e_87961_100x0_resize_box_3.png)](https://github.com/cupy)[![Deepwave Digital Logo](https://rapids.ai/_partners/deepwave-digital/logo_hua53ce4b0c82764243e77eb561a21396e_46808_100x0_resize_box_3.png)](https://github.com/deepwavedigital)[![Gunrock Logo](https://rapids.ai/_partners/gunrock/logo_hu2cc83b5c3fa1bc1ff0519d5169c7a2ed_121250_100x0_resize_box_3.png)](https://github.com/gunrock)[![NVIDIA Logo](https://rapids.ai/_partners/nvidia/logo_hu752c78ef8205cb849e89eae4893f9e62_94377_100x0_resize_box_3.png)](https://github.com/NVIDIA)[![Quansight Logo](https://rapids.ai/_partners/quansight/logo_hue2ea11d99176c0f55efc5549f5876937_70501_100x0_resize_box_3.png)](https://github.com/quansight-labs)[![Walmart Logo](https://rapids.ai/_partners/walmart/logo_huf6d1564ead47f2f0885c6b6dd27a0cf3_58990_100x0_resize_box_3.png)](https://github.com/walmartlabs)

# Learn More

## About RAPIDS

Learn more about RAPIDS' start with Apache Arrow and GoAi. Also find an overview of the
capabilities of RAPIDS, as well as featured projects in our
[About Section](https://rapids.ai/learn-more)

## Use Cases

Hear about success stories, resources for integrating RAPIDS workflows in your business, and
deployment strategies in our
[Use Cases Section](https://rapids.ai/learn-more#use-cases)

## Get Involved

Use RAPIDS directly or through [NVIDIA AI Enterprise](https://www.nvidia.com/en-us/data-center/products/ai-enterprise/), which provides extensive optimization, certified
hardware profiles, and direct IT support. Find additional business resources, community
resources, and guides for RAPIDS evangelism in our
[Get Involved Section](https://rapids.ai/learn-more/#get-involved)

# Latest News

## RAPIDS X/Twitter

Follow the latest from the RAPIDS X/Twitter community with [@RAPIDSai](https://twitter.com/RAPIDSai)

## RAPIDS Support Notices

Get the full list of developer updates and notices (RSN) that may affect your projects on the [RSN Docs Page](https://docs.rapids.ai/notices)

## RAPIDS News

Find our highlighted content, including talks, posts, guides and more on the [NVIDIA Dev Blog](https://developer.nvidia.com/blog/) and [RAPIDS Blog](https://developer.nvidia.com/blog/tag/rapids/)

## Latest Posts

[**Reducing CUDA Binary Size to Distribute cuML on PyPI**\\
\\
\\
Starting with the 25.10 release, pip-installable cuML wheels can now be downloaded directly from PyPI. No more complex installation steps or managing Conda...\\
\\
\\
Post by Divye Gala· Dec 15, 2025](https://developer.nvidia.com/blog/reducing-cuda-binary-size-to-distribute-cuml-on-pypi/)

[**How to GPU-Accelerate Model Training with CUDA-X Data Science**\\
\\
\\
In previous posts on AI in manufacturing and operations, we covered the unique data challenges in the supply chain and how smart feature engineering can...\\
\\
\\
Post by Divyansh Jain· Sep 25, 2025](https://developer.nvidia.com/blog/how-to-gpu-accelerate-model-training-with-cuda-x-data-science/)

[**How to Accelerate Community Detection in Python Using GPU-Powered Leiden**\\
\\
\\
Community detection algorithms play an important role in understanding data by identifying hidden groups of related entities in networks. Social network...\\
\\
\\
Post by Rick Ratzel· Sep 23, 2025](https://developer.nvidia.com/blog/how-to-accelerate-community-detection-in-python-using-gpu-powered-leiden/)

[**The Kaggle Grandmasters Playbook: 7 Battle-Tested Modeling Techniques for Tabular Data**\\
\\
\\
Over hundreds of Kaggle competitions, we've refined a playbook that consistently lands us near the top of the leaderboard—no matter if we’re working with...\\
\\
\\
Post by Kazuki Onodera· Sep 18, 2025](https://developer.nvidia.com/blog/the-kaggle-grandmasters-playbook-7-battle-tested-modeling-techniques-for-tabular-data/)

[**NVIDIA RAPIDS 25.08 Adds New Profiler for cuML, Updates to the Polars GPU Engine, Additional Algorithm Support, and More**\\
\\
\\
The 25.08 release of RAPIDS continues to push the boundaries toward making accelerated data science more accessible and scalable with the addition of several...\\
\\
\\
Post by Brian Tepera· Sep 17, 2025](https://developer.nvidia.com/blog/nvidia-rapids-25-08-adds-new-profiler-for-cuml-updates-to-the-polars-gpu-engine-additional-algorithm-support-and-more/)

[**How to Spot (and Fix) 5 Common Performance Bottlenecks in pandas Workflows**\\
\\
\\
Slow data loads, memory-intensive joins, and long-running operations—these are problems every Python practitioner has faced. They waste valuable time and make...\\
\\
\\
Post by Jamil Semaan· Aug 22, 2025](https://developer.nvidia.com/blog/how-to-spot-and-fix-5-common-performance-bottlenecks-in-pandas-workflows/)