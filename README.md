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

1. Installation
    Step 1: Install Julia

On Windows:

    Download Julia from the official website.
    Run the installer and follow the instructions.
    After installation, add Julia to your system path:
        Open the Start menu, search for 'Environment Variables,' and select 'Edit the system environment variables.'
        Click on 'Environment Variables.'
        Under 'System variables,' find 'Path,' select it, and click 'Edit.'
        Click 'New' and add the path where Julia was installed (usually C:\Users\YourUsername\AppData\Local\Programs\Julia-1.x.x\bin).
        Click 'OK' to close the windows.

On Mac:

    Open the terminal.
    Install Julia using Homebrew:

    brew install --cask julia

Verify the installation:

    julia --version

On Linux:

    Open the terminal.
    Download the latest version of Julia:

    wget https://julialang-s3.julialang.org/bin/linux/x64/1.9/julia-1.9.0-linux-x86_64.tar.gz

Extract the downloaded file and move it to /opt:

    tar xzf julia-1.9.0-linux-x86_64.tar.gz
    sudo mv julia-1.9.0 /opt/

Add Julia to your path:

    sudo ln -s /opt/julia-1.9.0/bin/julia /usr/local/bin/julia

Verify the installation:

    julia --version

Step 2: Install Julia Packages
Open Julia in the terminal:

    julia

Add the necessary packages:

    using Pkg
    Pkg.add(["KomaMRI", "FileIO", "JLD2","JSON","NPZ","NIfTI"])

Exit Julia:

    exit()

Step 3: Install Python

On Windows:

    Download and install Python from the official site.
    During installation, make sure to check the box 'Add Python to PATH.'

On Mac:

    Open the terminal and install Python via Homebrew:

    brew install python

On Linux:

    Open the terminal and run:

    sudo apt update
    sudo apt install python3 python3-pip

Step 4: Install virtualenv and Create a Python Environment Named camrie
Open the terminal (or Command Prompt on Windows).
Install virtualenv if it’s not installed:

    pip install virtualenv

Create a new virtual environment named camrie:

    virtualenv camrie

Step 5: Activate the camrie Environment

On Windows:

    camrie\Scripts\activate

On Mac/Linux:

    source camrie/bin/activate

Step 6: Install Python Packages from requirements.txt

Once the camrie environment is active, install the required Python packages:

    pip install -r requirements.txt

Step 7: Verify Installation
Ensure that all Julia packages are installed correctly:

    julia
    using KomaMRI, FileIO, JLD2, JSON,NPZ,NIfTI

Ensure that all Python packages are installed correctly:

    pip list

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


You can download the paitent dataset from here: https://www.cancerimagingarchive.net/collection/brats-africa/



