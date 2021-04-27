
export CUDA_VISIBLE_DEVICES=3

python demo.py \
experiments/seg_detector/fakepages_resnet50_deform_thre.yaml \
--image_path /home/euphoria/Chinese-ancient-book-recognition-HSK/data/book_pages_fz2_aug_jingbu_2w/test_images/ \
--visualize \
--sort_boxes \
--resume \
/disks/sdc/projs/AncientBooks/models/db/fakepage_res50_iter3.5.bin \
--box_thresh 0.5 \
--result_dir /disks/sdc/euphoria/db_test_results/aug_jingbu/res50_3.5 \
