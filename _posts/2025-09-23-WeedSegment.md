---
title: "Enabling Plant Phenotyping in Weedy Environments using Multi-Modal Imagery via Synthetic and Generated Training Data"
layout: single
excerpt_separator: "<!--more-->"
categories:
  - Publications
---

Authors: Earl Ranario, Ismael Mayanja, Heesup Yun, Brian N Bailey, J Mason Earles

Accurate plant segmentation in thermal imagery remains a significant challenge for high throughput field phenotyping, particularly in outdoor environments where low contrast between plants and weeds and frequent occlusions hinder performance. To address this, we present a framework that leverages synthetic RGB imagery, a limited set of real annotations, and GAN-based cross-modality alignment to enhance semantic segmentation in thermal images. We trained models on 1,128 synthetic images containing complex mixtures of crop and weed plants in order to generate image segmentation masks for crop and weed plants. We additionally evaluated the benefit of integrating as few as five real, manually segmented field images within the training process using various sampling strategies. When combining all the synthetic images with a few labeled real images, we observed a maximum relative improvement of 22% for the weed class and 17% for the plant class compared to the full real-data baseline. Cross-modal alignment was enabled by translating RGB to thermal using CycleGAN-turbo, allowing robust template matching without calibration. Results demonstrated that combining synthetic data with limited manual annotations and cross-domain translation via generative models can significantly boost segmentation performance in complex field environments for multi-model imagery.

<a href="https://arxiv.org/pdf/2509.19208?">
  <img src="https://img.shields.io/badge/arXiv-2503.21990-b31b1b.svg" height="22.5">
</a>

<!--more-->