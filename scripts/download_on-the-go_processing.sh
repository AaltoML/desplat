#!/bin/bash

mkdir ../data/
wget https://cvg-data.inf.ethz.ch/on-the-go.zip
unzip on-the-go.zip -d ../data/
rm on-the-go.zip

base_path="../data/on-the-go"

subfolders=(
    "patio"
    "mountain"
    "fountain"
    "patio_high"
    "spot"
    "corner"
    "arcdetriomphe" # for visualization
)

for folder in "${subfolders[@]}"; do
    mv "$base_path/$folder/images" "$base_path/$folder/input"
    python ./scripts/convert.py -s "$base_path/$folder" --resize
done