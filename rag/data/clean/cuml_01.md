---
url: https://docs.rapids.ai/api/cuml/stable/
tecnologia: cuML
titulo: Welcome to cuML’s documentation! — cuml 26.06.00 documentation
---

Back to top`Ctrl` + `K`

cuml

[cucim](https://docs.rapids.ai/api/cucim/stable) [cudf-java](https://docs.rapids.ai/api/cudf-java/stable) [cudf](https://docs.rapids.ai/api/cudf/stable/) [cugraph](https://docs.rapids.ai/api/cugraph/stable) [cuml](https://docs.rapids.ai/api/cuml/stable) [cuproj](https://docs.rapids.ai/api/cuproj/stable) [cuspatial](https://docs.rapids.ai/api/cuspatial/stable) [cuvs](https://docs.rapids.ai/api/cuvs/stable) [cuxfilter](https://docs.rapids.ai/api/cuxfilter/stable) [dask-cuda](https://docs.rapids.ai/api/dask-cuda/stable) [dask-cudf](https://docs.rapids.ai/api/dask-cudf/stable) [kvikio](https://docs.rapids.ai/api/kvikio/stable) [libcudf](https://docs.rapids.ai/api/libcudf/stable/namespacecudf/) [libcuml](https://docs.rapids.ai/api/libcuml/stable) [libcuproj](https://docs.rapids.ai/api/libcuproj/stable) [libcuspatial](https://docs.rapids.ai/api/libcuspatial/stable) [libkvikio](https://docs.rapids.ai/api/libkvikio/stable) [librapidsmpf](https://docs.rapids.ai/api/librapidsmpf/stable) [librmm](https://docs.rapids.ai/api/librmm/stable) [libucxx](https://docs.rapids.ai/api/libucxx/stable) [nvforest](https://docs.rapids.ai/api/nvforest/stable) [raft](https://docs.rapids.ai/api/raft/stable) [rapids-cmake](https://docs.rapids.ai/api/rapids-cmake/stable) [rapidsmpf](https://docs.rapids.ai/api/rapidsmpf/stable) [rmm](https://docs.rapids.ai/api/rmm/stable) [ucxx](https://docs.rapids.ai/api/ucxx/stable)

stable (26.06)

[nightly (26.08)](https://docs.rapids.ai/api/cuml/nightly) [stable (26.06)](https://docs.rapids.ai/api/cuml/stable) [legacy (26.04)](https://docs.rapids.ai/api/cuml/legacy)

- System Settings
- Light
- Dark

- [GitHub](https://github.com/rapidsai/cuml)
- [Twitter](https://twitter.com/rapidsai)

# Welcome to cuML’s documentation! [\#](https://docs.rapids.ai/api/cuml/stable/\#welcome-to-cuml-s-documentation "Link to this heading")

cuML is a suite of fast, GPU-accelerated machine learning algorithms
designed for data science and analytical tasks. Our API mirrors scikit-learn,
providing practitioners with the familiar fit-predict-transform paradigm
without requiring GPU programming expertise. With [`cuml.accel`](https://docs.rapids.ai/api/cuml/stable/api/cuml.accel/#module-cuml.accel "cuml.accel"), cuML can also
automatically accelerate existing code with zero code changes.

cuML delivers on average **10-50x faster performance** than CPU-based
alternatives for realistic workloads and supports **50+ algorithms** across all
major machine learning categories, including clustering, regression,
classification, dimensionality reduction, and time series analysis. With
comprehensive **multi-GPU and multi-node support** via Dask, cuML scales from
single workstations to large clusters.

Especially if your scikit-learn, umap-learn, or hdbscan workflows take many
minutes to complete, you will likely benefit from using cuML. The equivalent
cuML estimators often run in seconds.

# Quick Start [\#](https://docs.rapids.ai/api/cuml/stable/\#quick-start "Link to this heading")

```
from cuml.datasets import make_blobs
from cuml.cluster import DBSCAN

# Create sample data
X, y = make_blobs(n_samples=100, centers=3, n_features=2, random_state=42)

# Fit clustering model
dbscan = DBSCAN(eps=1.0, min_samples=5)
dbscan.fit(X)
print(dbscan.labels_)
```

Copy to clipboard

# Key Features [\#](https://docs.rapids.ai/api/cuml/stable/\#key-features "Link to this heading")

- **GPU Acceleration**: 10-50x faster than CPU-based alternatives

- **Scikit-learn Compatible**: Drop-in replacement for most sklearn algorithms

- **Multi-GPU Support**: Scale across multiple GPUs and nodes with Dask

- **Comprehensive Coverage**: 50+ algorithms across all major ML categories

- **Flexible Input**: Works with NumPy, cuDF, cuPy, and PyTorch tensors

- **Production Ready**: Battle-tested in enterprise environments

# Installation [\#](https://docs.rapids.ai/api/cuml/stable/\#installation "Link to this heading")

cuML is available through conda and pip. For detailed installation instructions,
visit the [RAPIDS Release Selector](https://docs.rapids.ai/install#selector).

Note

cuML is only supported on Linux operating systems and WSL 2. See
for details on system and hardware requirements.

# Part of RAPIDS [\#](https://docs.rapids.ai/api/cuml/stable/\#part-of-rapids "Link to this heading")

cuML is part of the RAPIDS suite of open source libraries that enable
end-to-end data science and analytics pipelines entirely on GPUs. It works
seamlessly with other RAPIDS libraries like cuDF for data manipulation and
cuGraph for graph analytics.

# Community & Support [\#](https://docs.rapids.ai/api/cuml/stable/\#community-support "Link to this heading")

- [User Guide](https://docs.rapids.ai/api/cuml/stable/user_guide/) \- Comprehensive usage documentation

- [API Reference](https://docs.rapids.ai/api/cuml/stable/api/) \- Complete API documentation

- [GitHub Issues](https://github.com/rapidsai/cuml/issues) \- Report bugs and request features

- [RAPIDS Community](https://rapids.ai/community.html) \- Join our community

On this page