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
import sys
import os


def embedding_training_cache_test(json_file, output_dir):
    dataset = [
        ("file_list." + str(i) + ".txt", "file_list." + str(i) + ".keyset") for i in range(5)
    ]
    solver = hugectr.CreateSolver(
        batchsize=16384,
        batchsize_eval=16384,
        vvgpu=[[0]],
        use_mixed_precision=False,
        i64_input_key=False,
        use_algorithm_search=True,
        use_cuda_graph=True,
        repeat_dataset=False,
    )
    reader = hugectr.DataReaderParams(
        data_reader_type=hugectr.DataReaderType_t.Parquet,
        source=["train" + str(i) + "/file_list." + str(i) + ".txt" for i in range(5)],
        keyset=["train" + str(i) + "/file.keyset" for i in range(5)],
        eval_source="train5/file_list.5.txt",
        check_type=hugectr.Check_t.Non,
        slot_size_array=[
            203750,
            18573,
            14082,
            7020,
            18966,
            4,
            6382,
            1246,
            49,
            185920,
            71354,
            67346,
            11,
            2166,
            7340,
            60,
            4,
            934,
            15,
            204208,
            141572,
            199066,
            60940,
            9115,
            72,
            34,
            278899,
            355877,
        ],
    )
    optimizer = hugectr.CreateOptimizer(optimizer_type=hugectr.Optimizer_t.Adam)
    hc_cnfg = hugectr.CreateHMemCache(2, 0.5, 0)
    etc = hugectr.CreateETC(
        ps_types=[hugectr.TrainPSType_t.Staged, hugectr.TrainPSType_t.Cached],
        sparse_models=[output_dir + "/wdl_0_sparse_model", output_dir + "/wdl_1_sparse_model"],
        local_paths=[output_dir],
        hmem_cache_configs=[hc_cnfg],
    )
    model = hugectr.Model(solver, reader, optimizer, etc)
    model.construct_from_json(graph_config_file=json_file, include_dense_network=True)
    model.compile()
    model.summary()
    model.fit(num_epochs=1, eval_interval=200, display=200)
    updated_model = model.get_incremental_model()
    model.save_params_to_files(os.path.join(output_dir, "wdl"))
    model.set_source(
        source=["train" + str(i) + "/file_list." + str(i) + ".txt" for i in range(6, 9)],
        keyset=["train" + str(i) + "/file.keyset" for i in range(6, 9)],
        eval_source="train5/file_list.5.txt",
    )
    model.fit(num_epochs=1, eval_interval=200, display=200)
    updated_model = model.get_incremental_model()
    model.save_params_to_files(os.path.join(output_dir, "wdl"))


if __name__ == "__main__":
    json_file = sys.argv[1]
    output_dir = sys.argv[2]
    embedding_training_cache_test(json_file, output_dir)
