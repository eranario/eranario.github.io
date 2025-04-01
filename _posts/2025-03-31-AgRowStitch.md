---
title: "AgRowStitch: A High-fidelity Image Stitching Pipeline for Ground-based Agricultural Images"
layout: single
excerpt_separator: "<!--more-->"
categories:
  - Publications
---

Agricultural imaging often requires individual images to be stitched together into a final mosaic for analysis. However, agricultural images can be particularly challenging to stitch because feature matching across images is difficult due to repeated textures, plants are non-planar, and mosaics built from many images can accumulate errors that cause drift. Although these issues can be mitigated by using georeferenced images or taking images at high altitude, there is no general solution for images taken close to the crop. To address this, we created a user-friendly and open source pipeline for stitching ground-based images of a linear row of crops that does not rely on additional data. First, we use SuperPoint and LightGlue to extract and match features within small batches of images. Then we stitch the images in each batch in series while imposing constraints on the camera movement. After straightening and rescaling each batch mosaic, all batch mosaics are stitched together in series and then straightened into a final mosaic. We tested the pipeline on images collected along 72 m long rows of crops using two different agricultural robots and a camera manually carried over the row. In all three cases, the pipeline produced high-quality mosaics that could be used to georeference real world positions with a mean absolute error of 20 cm. This approach provides accessible leaf-scale stitching to users who need to coarsely georeference positions within a row, but do not have access to accurate positional data or sophisticated imaging systems.

<a href="https://arxiv.org/abs/2503.21990">
  <img src="https://img.shields.io/badge/arXiv-2503.21990-b31b1b.svg" height="22.5">
</a>

<!--more-->