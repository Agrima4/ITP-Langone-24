# ITP-Langone-24

**MRI Dataset Generation and Processing Pipeline**

This project focuses on creating a dataset and a robust pipeline for simulating and processing MRI data, enabling accurate alignment and deformation applications with target images.

# Overview

This project involves three main stages:

    1. MRI Simulation and NIfTI Generation: Simulate MRI slices from input parameters (T1, T2, PD, and a sequence file) and convert them into a 3D NIfTI image.
    2. Registration: Align the simulated MRI with target MRI images using affine registration.
    3. Deformation Field Application: Apply the deformation field generated during registration to align T1, T2, and PD maps with the target images.

The output dataset includes the aligned TCIA_T1, TCIA_T2, and TCIA_PD maps for each patient, along with the deformation field.

# Project Architecture

The project consists of three main stages:

1. Stage 1: MRI Simulation

   Description: This stage generates simulated MRI slices and 3D MRI images in NIfTI format.

   Key Components:

   Simulated MRI slices (PNG format).

   Simulated 3D MRI (NIfTI format).

   SEQ and Coil files are used for simulation.
**
Setup Instructions:**

Clone and set up the following repositories:

1. LambdaKoma Repository : https://github.com/erosmontin/lambdakoma

2. KomaNYU Repository : https://github.com/cloudmrhub/KomaNYU.jl/blob/master/README.md

2. Stage 2: Registration

   Description: Registers the simulated NIfTI MRI image with the TCIA (The Cancer Imaging Archive) MRI image.

   Key Components:

   MRI Image (moving image).

   TCIA MRI (target image).

   Outputs deformation field and transformed MRI.

**Setup Instructions:**

Clone and set up the following repository:

1. RegistrationMplus Repository : https://github.com/erosmontin/registrationMplus/tree/master

2. Install the following dependencies:

   CMake.

   ITK version 4.13.0.

3. Stage 3: Deformation Field Application

   Description: Applies the deformation field or transformed MRI image to T1, T2, and PD images.

   Key Components:

   Deformation field/Transformed MRI.

   TCIA outputs (T1, T2, PD).

# Setup Instructions

Clone and Set Up Repositories:

For Stage 1:

git clone https://github.com/erosmontin/lambdakoma.git and 

git clone https://github.com/cloudmrhub/KomaNYU.jl.git

For Stage 2:

git clone https://github.com/erosmontin/registrationMplus.git

Install Dependencies:

Install CMake:
Download and install from CMake Official Website.

Install ITK:
Download ITK 4.13.0 from ITK Downloads.

Run the Master Script:
Once all dependencies are installed and the repositories are set up, execute the master script to run the entire project pipeline.
        
        python master_scripit.py

# Execution

The entire project workflow is executed by running the master_scripit.py file, which:

Simulates MRI images.

Registers the simulated image with the TCIA MRI image.

Applies the deformation field to generate TCIA T1, T2, and PD outputs.

Ensure all paths, files, and dependencies are correctly configured before running the script.

Output

Stage 1 Output:

Simulated MRI slices (PNG format).

Simulated 3D MRI (NIfTI format).

Stage 2 Output:

Deformation field/Transformed MRI image.

Stage 3 Output:

TCIA T1, T2, and PD images with applied deformation field.



