<div align="center">

  # <strong>DeSplat</strong>: Decomposed Gaussian Splatting for Distractor-Free Rendering

  <p align="center">
    <a href="https://johanna0626.github.io/">Yihao Wang</a> ·
    <a href="https://marcusklasson.github.io/">Marcus Klasson</a> ·
    <a href="https://maturk.github.io/">Matias Turkulainen</a> ·
    <a href="https://ffrivera0.github.io/">Shuzhe Wang</a> ·
    <a href="https://users.aalto.fi/~kannalj1/">Juho Kannala</a> ·
    <a href="https://users.aalto.fi/~asolin/">Arno Solin</a>
  </p>

  <h2 align="center">CVPR 2025</h2>

  <h3>
    <a href="https://arxiv.org/abs/2411.19756">Paper</a> |
    <a href="https://aaltoml.github.io/desplat/">Project Page</a>
  </h3>

</div>

---

This is a reimplementation of **DeSplat** based on the [gsplat](https://docs.gsplat.studio/) codebase, including the core functions.  
It is currently still under construction. Due to differences in scene scales, the thresholds and learning rates are not yet optimal.

## Installation
Please follow the installation instructions of **gsplat v1.0.0**.  
Additionally, install the required libraries listed in `/examples/requirements.txt`.


## Training

Please run:
```
cd examples

# Train from scratch
python simple_trainer_desplat.py --data_dir [data_dir] --data_factor 8 --result_dir [result_dir] [--eval_train]

# Load from checkpoint
python simple_trainer_desplat.py --data_dir [data_dir] --data_factor 8 --result_dir [result_dir] [--eval_train] --ckpt [checkpoint dir end with ckpt_29999.pt]
```

## Citation

```
@InProceedings{wang2024desplat,
    title={{DeSplat}: Decomposed {G}aussian Splatting for Distractor-Free Rendering},
    author={Wang, Yihao and Klasson, Marcus and Turkulainen, Matias and Wang, Shuzhe and Kannala, Juho and Solin, Arno},
    booktitle={IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
    year={2025}
}
```

## License
This software is provided under the MIT License. See the accompanying [LICENSE](LICENSE) file for details.
