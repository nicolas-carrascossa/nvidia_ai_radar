---
url: https://docs.rapids.ai/api/cudf/stable/
tecnologia: cuDF
titulo: Welcome to the cuDF documentation! — cudf 26.06.01 documentation
---

[Skip to main content](https://docs.rapids.ai/api/cudf/stable/#main-content)

Back to top`Ctrl` + `K`

[Home](https://docs.rapids.ai/api)

cudf

[cucim](https://docs.rapids.ai/api/cucim/stable) [cudf-java](https://docs.rapids.ai/api/cudf-java/stable) [cudf](https://docs.rapids.ai/api/cudf/stable/) [cugraph](https://docs.rapids.ai/api/cugraph/stable) [cuml](https://docs.rapids.ai/api/cuml/stable) [cuproj](https://docs.rapids.ai/api/cuproj/stable) [cuspatial](https://docs.rapids.ai/api/cuspatial/stable) [cuvs](https://docs.rapids.ai/api/cuvs/stable) [cuxfilter](https://docs.rapids.ai/api/cuxfilter/stable) [dask-cuda](https://docs.rapids.ai/api/dask-cuda/stable) [dask-cudf](https://docs.rapids.ai/api/dask-cudf/stable) [kvikio](https://docs.rapids.ai/api/kvikio/stable) [libcudf](https://docs.rapids.ai/api/libcudf/stable/namespacecudf/) [libcuml](https://docs.rapids.ai/api/libcuml/stable) [libcuproj](https://docs.rapids.ai/api/libcuproj/stable) [libcuspatial](https://docs.rapids.ai/api/libcuspatial/stable) [libkvikio](https://docs.rapids.ai/api/libkvikio/stable) [librapidsmpf](https://docs.rapids.ai/api/librapidsmpf/stable) [librmm](https://docs.rapids.ai/api/librmm/stable) [libucxx](https://docs.rapids.ai/api/libucxx/stable) [nvforest](https://docs.rapids.ai/api/nvforest/stable) [raft](https://docs.rapids.ai/api/raft/stable) [rapids-cmake](https://docs.rapids.ai/api/rapids-cmake/stable) [rapidsmpf](https://docs.rapids.ai/api/rapidsmpf/stable) [rmm](https://docs.rapids.ai/api/rmm/stable) [ucxx](https://docs.rapids.ai/api/ucxx/stable)

stable (26.06)

[nightly (26.08)](https://docs.rapids.ai/api/cudf/nightly/) [stable (26.06)](https://docs.rapids.ai/api/cudf/stable/) [legacy (26.04)](https://docs.rapids.ai/api/cudf/legacy/)

- System Settings
- Light
- Dark

- [GitHub](https://github.com/rapidsai/cudf)
- [Twitter](https://twitter.com/rapidsai)

# Welcome to the cuDF documentation! [\#](https://docs.rapids.ai/api/cudf/stable/\#welcome-to-the-cudf-documentation "Link to this heading")

![_images/RAPIDS-logo-purple.png](https://docs.rapids.ai/api/cudf/stable/_images/RAPIDS-logo-purple.png)

**cuDF** (pronounced “KOO-dee-eff”) is a Python GPU DataFrame library (built
on the [Apache Arrow](https://arrow.apache.org/) columnar memory format)
for loading, joining, aggregating, filtering, and otherwise manipulating data.
cuDF also provides a pandas-like API that will be familiar to data engineers
& data scientists, so they can use it to easily accelerate their workflows
without going into the details of CUDA programming.

`cudf.pandas` is built on cuDF and accelerates pandas code on the
GPU. It supports 100% of the pandas API, using the GPU for
supported operations, and automatically falling back to pandas for
other operations.

![_images/duckdb-benchmark-groupby-join.png](https://docs.rapids.ai/api/cudf/stable/_images/duckdb-benchmark-groupby-join.png)

Results of the [Database-like ops benchmark](https://duckdblabs.github.io/db-benchmark/) including cudf.pandas. See details [here](https://docs.rapids.ai/api/cudf/stable/cudf_pandas/benchmarks.html). [#](https://docs.rapids.ai/api/cudf/stable/#id1 "Link to this image")

Contents:

- [cuDF User Guide](https://docs.rapids.ai/api/cudf/stable/user_guide/)
- [cudf.pandas](https://docs.rapids.ai/api/cudf/stable/cudf_pandas/)
- [Polars GPU engine](https://docs.rapids.ai/api/cudf/stable/cudf_polars/)
- [pylibcudf documentation](https://docs.rapids.ai/api/cudf/stable/pylibcudf/)
- [libcudf documentation](https://docs.rapids.ai/api/cudf/stable/libcudf_docs/)
- [Indices and tables](https://docs.rapids.ai/api/cudf/stable/libcudf_docs/#indices-and-tables)
- [Developer Guide](https://docs.rapids.ai/api/cudf/stable/developer_guide/)

[Show Source](https://docs.rapids.ai/api/cudf/stable/_sources/index.rst.txt)