# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""AzureML ACFT Image Components package - finetuning component."""
__path__ = __import__('pkgutil').extend_path(__path__, __name__)


# List of Huggingface models that are not supported by the fine-tuning component. The name of model should be
# exactly same as model name specified in huggingface model repository.
UNSUPPORTED_HF_MODEL = [

]


# List of MMDetection models that are not supported by the fine-tuning component. The name of model should be
# exactly same as model name specified in mmdetection metafile.yaml
# (https://github.com/open-mmlab/mmdetection/tree/v2.28.2/configs).
UNSUPPORTED_MMDETECTION_MODEL = [
    # *rcnn_convnext* models are failing due to ModuleNotFoundError: No module named 'mmcls' WI: 2503815
    "mask-rcnn_convnext-t-p4-w7_fpn_amp-ms-crop-3x_coco",
    "cascade-mask-rcnn_convnext-t-p4-w7_fpn_4conv1fc-giou_amp-ms-crop-3x_coco",
    "cascade-mask-rcnn_convnext-s-p4-w7_fpn_4conv1fc-giou_amp-ms-crop-3x_coco",
    # centernet* models are failing with key error ['border']. WI: 2500745
    "centernet_r18-dcnv2_8xb16-crop512-140e_coco",
    "centernet_r18_8xb16-crop512-140e_coco",
    "centernet-update_r50-caffe_fpn_ms-1x_coco",
    # ga* models are failing with assert exception in evaluation loop. WI: 2500727
    "ga-rpn_r50-caffe_fpn_1x_coco",
    "ga-rpn_r101-caffe_fpn_1x_coco",
    "ga-rpn_x101-32x4d_fpn_1x_coco",
    "ga-rpn_x101-64x4d_fpn_1x_coco",
    "ga-faster-rcnn_r50-caffe_fpn_1x_coco",
    "ga-faster-rcnn_r101-caffe_fpn_1x_coco",
    "ga-faster-rcnn_x101-32x4d_fpn_1x_coco",
    "ga-faster-rcnn_x101-64x4d_fpn_1x_coco",
    "ga-retinanet_r50-caffe_fpn_1x_coco",
    "ga-retinanet_r101-caffe_fpn_1x_coco",
    "ga-retinanet_x101-32x4d_fpn_1x_coco",
    "ga-retinanet_x101-64x4d_fpn_1x_coco",

    # MessageHub needs to be updated
    "tood_r101_fpn_ms-2x_coco",
    "tood_x101-64x4d_fpn_ms-2x_coco",
    "tood_r101-dconv-c3-c5_fpn_ms-2x_coco",
    "tood_r50_fpn_anchor-based_1x_coco",
    "tood_r50_fpn_1x_coco",
    "tood_r50_fpn_ms-2x_coco",
    # requires batch_gt_instances_ignore
    "crowddet-rcnn_refine_r50_fpn_8xb2-30e_crowdhuman",
    "crowddet-rcnn_r50_fpn_8xb2-30e_crowdhuman",
    # System error: The size of tensor a (19) must match the
    # size of tensor b (20) at non-singleton dimension 3
    "faster-rcnn_r50_fpg_crop640-50e_coco",
    "faster-rcnn_r50_fpg-chn128_crop640-50e_coco",
    "mask-rcnn_r50_fpg_crop640-50e_coco",
    "mask-rcnn_r50_fpg-chn128_crop640-50e_coco",
    "retinanet_r50_fpg_crop640_50e_coco",
    "retinanet_r50_fpg-chn128_crop640_50e_coco",
    #  KeyError: 'border'
    "centernet_r18-dcnv2_8xb16-crop512-140e_coco",
    "centernet-update_r50-caffe_fpn_ms-1x_coco",
    # 'InstanceData' object has no attribute 'masks'
    "faster-rcnn_r50_fpn_carafe_1x_coco",
    "mask-rcnn_r50_fpn_carafe_1x_coco",
    # semantic - requires pairwisemasks
    "htc_r50_fpn_1x_coco",
    "htc_r101_fpn_20e_coco",
    "htc_x101-32x4d_fpn_16xb1-20e_coco",
    "htc_x101-64x4d_fpn_16xb1-20e_coco",
    "htc_x101-64x4d-dconv-c3-c5_fpn_ms-400-1400-16xb1-20e_coco"
]


UNSUPPORTED_MMTRACKING_MODEL = [
    # currently do not support joint detection and tracking methods
    "sort_faster-rcnn_fpn_4e_mot17-public-half",
    "sort_faster-rcnn_fpn_4e_mot17-private-half",
    "deepsort_faster-rcnn_fpn_4e_mot17-public-half",
    "deepsort_faster-rcnn_fpn_4e_mot17-private-half",
    "qdtrack_faster-rcnn_r50_fpn_4e_mot17-private-half",
    "qdtrack_faster-rcnn_r50_fpn_4e_crowdhuman_mot17-private-half",
    "qdtrack_faster-rcnn_r101_fpn_24e_lvis",
    "qdtrack_faster-rcnn_r101_fpn_12e_tao",
    "tracktor_faster-rcnn_r50_fpn_4e_mot15-public-half",
    "tracktor_faster-rcnn_r50_fpn_4e_mot15-private-half",
    "tracktor_faster-rcnn_r50_fpn_4e_mot16-public-half",
    "tracktor_faster-rcnn_r50_fpn_4e_mot16-private-half",
    "tracktor_faster-rcnn_r50_fpn_4e_mot17-public-half",
    "tracktor_faster-rcnn_r50_fpn_4e_mot17-private-half",
    "tracktor_faster-rcnn_r50_fpn_4e_mot17-public",
    "tracktor_faster-rcnn_r50_fpn_8e_mot20-public-half",
    "tracktor_faster-rcnn_r50_fpn_8e_mot20-public",
    "tracktor_faster-rcnn_r50_fpn_fp16_4e_mot17-private-half"
]
