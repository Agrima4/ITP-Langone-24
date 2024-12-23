# ITP-Langone-24

**MRI Dataset Generation and Processing Pipeline**

This project focuses on creating a dataset and a robust pipeline for simulating and processing MRI data, enabling accurate alignment and deformation applications with target images.

**Overview**

This project involves three main stages:

    1. MRI Simulation and NIfTI Generation: Simulate MRI slices from input parameters (T1, T2, PD, and a sequence file) and convert them into a 3D NIfTI image.
    2. Registration: Align the simulated MRI with target MRI images using affine registration.
    3. Deformation Field Application: Apply the deformation field generated during registration to align T1, T2, and PD maps with the target images.

The output dataset includes the aligned TCIA_T1, TCIA_T2, and TCIA_PD maps for each patient, along with the deformation field.

**Usage**
Run the master_script.py to run the whole pipeline:

      python master_script.py


