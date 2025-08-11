# This code is copied from the 3D Gaussian Splatter repository, available at https://github.com/graphdeco-inria/gaussian-splatting.
#
# Copyright (C) 2023, Inria
# GRAPHDECO research group, https://team.inria.fr/graphdeco
# All rights reserved.
#
# This software is free for non-commercial, research and evaluation use
# under the terms of the LICENSE.md file.
#
# For inquiries contact  george.drettakis@inria.fr
#

import os
import logging
from argparse import ArgumentParser
import shutil
import math
from PIL import Image

# This Python script is based on the shell converter script provided in the MipNerF 360 repository.
parser = ArgumentParser("Colmap converter")
parser.add_argument("--no_gpu", action="store_true")
parser.add_argument("--skip_matching", action="store_true")
parser.add_argument("--source_path", "-s", required=True, type=str)
parser.add_argument("--camera", default="OPENCV", type=str)
parser.add_argument("--colmap_executable", default="", type=str)
parser.add_argument("--resize", action="store_true")
parser.add_argument("--magick_executable", default="", type=str)
args = parser.parse_args()
colmap_command = (
    '"{}"'.format(args.colmap_executable)
    if len(args.colmap_executable) > 0
    else "colmap"
)
magick_command = (
    '"{}"'.format(args.magick_executable)
    if len(args.magick_executable) > 0
    else "magick"
)
use_gpu = 1 if not args.no_gpu else 0

# rename images folder to input
images_path = os.path.join(args.source_path, "images")
input_path = os.path.join(args.source_path, "input")

if os.path.exists(images_path):
    os.rename(images_path, input_path)
    print(f"'{images_path}' has been renamed to '{input_path}'")
else:
    print(f"The folder '{images_path}' does not exist.")

if not args.skip_matching:
    os.makedirs(args.source_path + "/distorted/sparse", exist_ok=True)
    ## Feature extraction
    feat_extracton_cmd = (
        colmap_command + " feature_extractor "
        "--database_path "
        + args.source_path
        + "/distorted/database.db \
        --image_path "
        + args.source_path
        + "/input \
        --ImageReader.single_camera 1 \
        --ImageReader.camera_model "
        + args.camera
        + " \
        --FeatureExtraction.use_gpu "
        + str(use_gpu)
    )
    exit_code = os.system(feat_extracton_cmd)
    if exit_code != 0:
        logging.error(f"Feature extraction failed with code {exit_code}. Exiting.")
        exit(exit_code)

    ## Feature matching
    feat_matching_cmd = (
        colmap_command
        + " exhaustive_matcher \
        --database_path "
        + args.source_path
        + "/distorted/database.db \
        --FeatureMatching.use_gpu "
        + str(use_gpu)
    )
    exit_code = os.system(feat_matching_cmd)
    if exit_code != 0:
        logging.error(f"Feature matching failed with code {exit_code}. Exiting.")
        exit(exit_code)

    ### Bundle adjustment
    # The default Mapper tolerance is unnecessarily large,
    # decreasing it speeds up bundle adjustment steps.
    mapper_cmd = (
        colmap_command
        + " mapper \
        --database_path "
        + args.source_path
        + "/distorted/database.db \
        --image_path "
        + args.source_path
        + "/input \
        --output_path "
        + args.source_path
        + "/distorted/sparse \
        --Mapper.ba_global_function_tolerance=0.000001"
    )
    exit_code = os.system(mapper_cmd)
    if exit_code != 0:
        logging.error(f"Mapper failed with code {exit_code}. Exiting.")
        exit(exit_code)

### Image undistortion
## We need to undistort our images into ideal pinhole intrinsics.
img_undist_cmd = (
    colmap_command
    + " image_undistorter \
    --image_path "
    + args.source_path
    + "/input \
    --input_path "
    + args.source_path
    + "/distorted/sparse/0 \
    --output_path "
    + args.source_path
    + "\
    --output_type COLMAP"
)
exit_code = os.system(img_undist_cmd)
if exit_code != 0:
    logging.error(f"Mapper failed with code {exit_code}. Exiting.")
    exit(exit_code)

files = os.listdir(args.source_path + "/sparse")
os.makedirs(args.source_path + "/sparse/0", exist_ok=True)
# Copy each file from the source directory to the destination directory
for file in files:
    if file == "0":
        continue
    source_file = os.path.join(args.source_path, "sparse", file)
    destination_file = os.path.join(args.source_path, "sparse", "0", file)
    shutil.move(source_file, destination_file)

if args.resize:
    print("Copying and resizing...")

    # Resize images.
    # for patio scene, we resize by 25%
    if args.source_path.endswith("patio") or args.source_path.endswith("arcdetriomphe"):
        resize_factor = 4
    else:
        resize_factor = 8
    os.makedirs(args.source_path + "/images_" + str(resize_factor), exist_ok=True)
    # Get the list of files in the source directory
    files = os.listdir(args.source_path + "/images")
    # Copy each file from the source directory to the destination directory
    for file in files:
        source_file = os.path.join(args.source_path, "images", file)

        with Image.open(source_file) as img:
            width, height = img.size
        target_width = math.floor(width / resize_factor)
        target_height = math.floor(height / resize_factor)

        destination_file = os.path.join(
            args.source_path, f"images_{resize_factor}", file
        )
        shutil.copy2(source_file, destination_file)
        exit_code = os.system(
            f"{magick_command} mogrify -resize {target_width}x{target_height}! {destination_file}"
        )
        if exit_code != 0:
            logging.error(f"resize failed with code {exit_code}. Exiting.")
            exit(exit_code)

print("Done.")
