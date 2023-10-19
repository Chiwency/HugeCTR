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
    batchsize=16384,
    lr=0.001,
    vvgpu=[[0]],
    repeat_dataset=True,
    i64_input_key=True,
)
reader = hugectr.DataReaderParams(
    data_reader_type=hugectr.DataReaderType_t.Parquet,
    source=["./deepfm_data_nvt/train/_file_list.txt"],
    eval_source="./deepfm_data_nvt/val/_file_list.txt",
    check_type=hugectr.Check_t.Sum,
    slot_size_array=[
        203931,
        18598,
        14092,
        7012,
        18977,
        4,
        6385,
        1245,
        49,
        186213,
        71328,
        67288,
        11,
        2168,
        7338,
        61,
        4,
        932,
        15,
        204515,
        141526,
        199433,
        60919,
        9137,
        71,
        34,
    ],
)
optimizer = hugectr.CreateOptimizer(
    optimizer_type=hugectr.Optimizer_t.Adam,
    update_type=hugectr.Update_t.Global,
    beta1=0.9,
    beta2=0.999,
    epsilon=0.0000001,
)
model = hugectr.Model(solver, reader, optimizer)
model.add(
    hugectr.Input(
        label_dim=1,
        label_name="label",
        dense_dim=13,
        dense_name="dense",
        data_reader_sparse_param_array=[hugectr.DataReaderSparseParam("data1", 1, True, 26)],
    )
)
model.add(
    hugectr.SparseEmbedding(
        embedding_type=hugectr.Embedding_t.DistributedSlotSparseEmbeddingHash,
        workspace_size_per_gpu_in_mb=2400,
        embedding_vec_size=128,
        combiner="sum",
        sparse_embedding_name="sparse_embedding1",
        bottom_name="data1",
        optimizer=optimizer,
    )
)
model.add(
    hugectr.DenseLayer(
        layer_type=hugectr.Layer_t.InnerProduct,
        bottom_names=["dense"],
        top_names=["fc1"],
        num_output=512,
    )
)
model.add(
    hugectr.DenseLayer(layer_type=hugectr.Layer_t.ReLU, bottom_names=["fc1"], top_names=["relu1"])
)
model.add(
    hugectr.DenseLayer(
        layer_type=hugectr.Layer_t.InnerProduct,
        bottom_names=["relu1"],
        top_names=["fc2"],
        num_output=256,
    )
)
model.add(
    hugectr.DenseLayer(layer_type=hugectr.Layer_t.ReLU, bottom_names=["fc2"], top_names=["relu2"])
)
model.add(
    hugectr.DenseLayer(
        layer_type=hugectr.Layer_t.InnerProduct,
        bottom_names=["relu2"],
        top_names=["fc3"],
        num_output=128,
    )
)
model.add(
    hugectr.DenseLayer(layer_type=hugectr.Layer_t.ReLU, bottom_names=["fc3"], top_names=["relu3"])
)
model.add(
    hugectr.DenseLayer(
        layer_type=hugectr.Layer_t.Interaction,
        bottom_names=["relu3", "sparse_embedding1"],
        top_names=["interaction1"],
    )
)
model.add(
    hugectr.DenseLayer(
        layer_type=hugectr.Layer_t.InnerProduct,
        bottom_names=["interaction1"],
        top_names=["fc4"],
        num_output=1024,
    )
)
model.add(
    hugectr.DenseLayer(layer_type=hugectr.Layer_t.ReLU, bottom_names=["fc4"], top_names=["relu4"])
)
model.add(
    hugectr.DenseLayer(
        layer_type=hugectr.Layer_t.InnerProduct,
        bottom_names=["relu4"],
        top_names=["fc5"],
        num_output=1024,
    )
)
model.add(
    hugectr.DenseLayer(
        layer_type=hugectr.Layer_t.BatchNorm,
        bottom_names=["fc5"],
        top_names=["bn5"],
        factor=1.0,
        eps=0.00001,
        gamma_init_type=hugectr.Initializer_t.XavierUniform,
        beta_init_type=hugectr.Initializer_t.XavierUniform,
    )
)
model.add(
    hugectr.DenseLayer(layer_type=hugectr.Layer_t.ReLU, bottom_names=["bn5"], top_names=["relu5"])
)
model.add(
    hugectr.DenseLayer(
        layer_type=hugectr.Layer_t.InnerProduct,
        bottom_names=["relu5"],
        top_names=["fc6"],
        num_output=512,
    )
)
model.add(
    hugectr.DenseLayer(
        layer_type=hugectr.Layer_t.BatchNorm,
        bottom_names=["fc6"],
        top_names=["bn6"],
        factor=1.0,
        eps=0.00001,
        gamma_init_type=hugectr.Initializer_t.XavierUniform,
        beta_init_type=hugectr.Initializer_t.XavierUniform,
    )
)
model.add(
    hugectr.DenseLayer(layer_type=hugectr.Layer_t.ReLU, bottom_names=["bn6"], top_names=["relu6"])
)
model.add(
    hugectr.DenseLayer(
        layer_type=hugectr.Layer_t.InnerProduct,
        bottom_names=["relu6"],
        top_names=["fc7"],
        num_output=256,
    )
)
model.add(
    hugectr.DenseLayer(
        layer_type=hugectr.Layer_t.BatchNorm,
        bottom_names=["fc7"],
        top_names=["bn7"],
        factor=1.0,
        eps=0.00001,
        gamma_init_type=hugectr.Initializer_t.XavierUniform,
        beta_init_type=hugectr.Initializer_t.XavierUniform,
    )
)
model.add(
    hugectr.DenseLayer(layer_type=hugectr.Layer_t.ReLU, bottom_names=["bn7"], top_names=["relu7"])
)
model.add(
    hugectr.DenseLayer(
        layer_type=hugectr.Layer_t.InnerProduct,
        bottom_names=["relu7"],
        top_names=["fc8"],
        num_output=1,
    )
)
model.add(
    hugectr.DenseLayer(
        layer_type=hugectr.Layer_t.BinaryCrossEntropyLoss,
        bottom_names=["fc8", "label"],
        top_names=["loss"],
    )
)
model.graph_to_json("/onnx_converter/graph_files/dlrm.json")
model.compile()
model.summary()
model.fit(
    max_iter=2300,
    display=200,
    eval_interval=2000,
    snapshot=2000,
    snapshot_prefix="/onnx_converter/hugectr_models/dlrm",
)

import numpy as np

preds = model.check_out_tensor("fc8", hugectr.Tensor_t.Evaluate)
np.save("/onnx_converter/hugectr_models/dlrm_preds.npy", preds)
