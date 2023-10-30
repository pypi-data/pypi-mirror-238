#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
#
# Copyright 2020-* Emanuele Ballarin <emanuele@ballarin.cc>
# All Rights Reserved. Unless otherwise explicitly stated.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# ==============================================================================
#
# SPDX-License-Identifier: Apache-2.0
# Imports (wildcard)
from .data import *
from .distributed import *
from .logging import *
from .nn import *
from .optim import *

# Deletions (from .data)
del FastCollateMixup
del Mixup
del cifarhundred_dataloader_dispatcher
del cifarten_dataloader_dispatcher
del fashionmnist_dataloader_dispatcher
del imagenette_dataloader_dispatcher
del mnist_dataloader_dispatcher
del data_prep_dispatcher_1ch
del data_prep_dispatcher_3ch

# Deletions (from .distributed)
del slurm_nccl_env
del reduce_accumulate_keepalive

# Deletions (from .nn)
del ArgMaxLayer
del BatchNorm2dRP
del BinarizeLayer
del BrokenReLU
del CausalConv1d
del Conv2dRP
del ConvolutionalFlattenLayer
del CoordConv1d
del CoordConv2d
del CoordConv3d
del Dropout2dRP
del FCBlock
del FCBlockLegacy
del FieldTransform
del FlatChannelize2DLayer
del GaussianReparameterizerSampler
del InnerProduct
del KWTA1d
del KWTA2d
del Mish
del MultiSolvePoissonTensor
del NNEnsemble
del PoissonNetCifar
del ProbePrintLayer
del ReshapeLayer
del ScaledERF
del SERLU
del SGRUHCell
del SinLU
del SmeLU
del SolvePoisson
del SolvePoissonTensor
del WideResNet
del PreActResNet
del beta_reco_bce
del field_transform
del mishlayer_init
del patch_rp_train_network
del pixelwise_bce_mean
del pixelwise_bce_sum
del RBLinear
del DeepRBL
del build_resblock
del build_repeated_sequential
del build_homogeneous_resnet
del ResBlock

# Deletions (from .optim)
del AdaHessian
del Adan
del Lion
del Lookahead
del Lookaround
del RAdam
del SAM
del AdaBound
del ralah_optim
del wfneal
del tricyc1c
del epochwise_onecycle
del onecycle_lincos
del onecycle_linlin

# Deletions (from .logging)
del AverageMeter
del LogCSV
