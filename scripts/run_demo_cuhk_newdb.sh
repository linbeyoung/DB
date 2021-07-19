
export CUDA_VISIBLE_DEVICES=0

python demo.py \
experiments/seg_detector/fakepages_resnet50_deform_thre.yaml \
--image_path /disks/sdd/beyoung/data/ER007/20_19584 \
--visualize \
--sort_boxes \
--resume \
/home/euphoria/pkg/seg_detector/models/fakepage_res50_iter2.bin \
--box_thresh 0.5 \
--result_dir /disks/sdc/euphoria/ER007/20_19584/ \
