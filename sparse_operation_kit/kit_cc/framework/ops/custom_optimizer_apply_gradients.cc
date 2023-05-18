/*
 * Copyright (c) 2021, NVIDIA CORPORATION.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include "tensorflow/core/framework/common_shape_fns.h"
#include "tensorflow/core/framework/op.h"
#include "tensorflow/core/framework/shape_inference.h"
#include "sparse_operation_kit/kit_cc/utils.h"

using namespace tensorflow;
using namespace tensorflow::shape_inference;

REGISTER_OP("CustomOptimizerApplyGradients")
    .Input("emb_var_handle: resource")
    .Input("grad: float32")
    .Input("local_indices: indices_dtype")
    .Input("learning_rate: float32")
    .Input("current_step: int64")
    .Attr("indices_dtype: {int64}")
    .SetShapeFn([](InferenceContext* ctx) {
      ShapeHandle grad_shape;
      TF_RETURN_IF_ERROR(ctx->WithRank(ctx->input(1), 2, &grad_shape));
      return sok_tsl_status();
    });
