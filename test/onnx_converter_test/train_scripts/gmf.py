"""
 Copyright (c) 2023, NVIDIA CORPORATION.
 
 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""

import hugectr
from mpi4py import MPI

solver = hugectr.CreateSolver(
    max_eval_batches=1,
    batchsize_eval=6400,
    batchsize=17548,
    lr=0.0045,
    vvgpu=[[0]],
    metrics_spec={
        hugectr.MetricsType.HitRate: 0.8,
        hugectr.MetricsType.AverageLoss: 0.0,
        hugectr.MetricsType.AUC: 1.0,
    },
    i64_input_key=True,
    repeat_dataset=True,
)
reader = hugectr.DataReaderParams(
    data_reader_type=hugectr.DataReaderType_t.Parquet,
    source=["./movie_len_parquet/train/_file_list.txt"],
    eval_source="./movie_len_parquet/val/_file_list.txt",
    check_type=hugectr.Check_t.Non,
    slot_size_array=[162543, 56573],
)
optimizer = hugectr.CreateOptimizer(
    optimizer_type=hugectr.Optimizer_t.Adam,
    update_type=hugectr.Update_t.Global,
    beta1=0.25,
    beta2=0.5,
    epsilon=0.0000001,
)
model = hugectr.Model(solver, reader, optimizer)
model.add(
    hugectr.Input(
        label_dim=1,
        label_name="label",
        dense_dim=0,
        dense_name="dense",
        data_reader_sparse_param_array=[hugectr.DataReaderSparseParam("data", 1, True, 2)],
    )
)
model.add(
    hugectr.SparseEmbedding(
        embedding_type=hugectr.Embedding_t.DistributedSlotSparseEmbeddingHash,
        workspace_size_per_gpu_in_mb=60,
        embedding_vec_size=16,
        combiner="sum",
        sparse_embedding_name="gmf_embedding",
        bottom_name="data",
        optimizer=optimizer,
    )
)
model.add(
    hugectr.DenseLayer(
        layer_type=hugectr.Layer_t.Reshape,
        bottom_names=["gmf_embedding"],
        top_names=["reshape1"],
        leading_dim=32,
    )
)
model.add(
    hugectr.DenseLayer(
        layer_type=hugectr.Layer_t.Slice,
        bottom_names=["reshape1"],
        top_names=["user", "item"],
        ranges=[(0, 15), (16, 31)],
    )
)
model.add(
    hugectr.DenseLayer(
        layer_type=hugectr.Layer_t.ElementwiseMultiply,
        bottom_names=["user", "item"],
        top_names=["multiply1"],
    )
)
model.add(
    hugectr.DenseLayer(
        layer_type=hugectr.Layer_t.InnerProduct,
        bottom_names=["multiply1"],
        top_names=["gmf_out"],
        num_output=1,
    )
)
model.add(
    hugectr.DenseLayer(
        layer_type=hugectr.Layer_t.BinaryCrossEntropyLoss,
        bottom_names=["gmf_out", "label"],
        top_names=["loss"],
    )
)
model.graph_to_json("/onnx_converter/graph_files/gmf.json")
model.compile()
model.summary()
model.fit(
    max_iter=2100,
    display=200,
    eval_interval=2000,
    snapshot=2000,
    snapshot_prefix="/onnx_converter/hugectr_models//gmf",
)

import numpy as np

preds = model.check_out_tensor("gmf_out", hugectr.Tensor_t.Evaluate)
np.save("/onnx_converter/hugectr_models/gmf_preds.npy", preds)
