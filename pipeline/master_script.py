import sys
sys.path.append("D:/Downloads/ITP/camrie/Lib/site-packages")

import os
import shutil 
import subprocess
import SimpleITK as sitk
import common as c  
from glob import glob
import pandas as pd
import numpy as np

def extract_deformation_features(deformation_file):
    """
    Extracts numerical features from the deformation field file.
    """
    try:
        with open(deformation_file, 'r') as f:
            lines = f.readlines()

        parameters = []
        fixed_parameters = []

        for line in lines:
            if line.startswith("Parameters:"):
                parameters = list(map(float, line.split("Parameters:")[1].strip().split()))
            elif line.startswith("FixedParameters:"):
                fixed_parameters = list(map(float, line.split("FixedParameters:")[1].strip().split()))

        # Example features extracted from the deformation field
        return {
            "Deformation Param Sum": sum(parameters),
            "Deformation Fixed Param Sum": sum(fixed_parameters),
            "Deformation Param Count": len(parameters),
            "Deformation Fixed Param Count": len(fixed_parameters),
        }
    except Exception as e:
        print(f"Error extracting features from deformation field {deformation_file}: {e}")
        return {
            "Deformation Param Sum": 0,
            "Deformation Fixed Param Sum": 0,
            "Deformation Param Count": 0,
            "Deformation Fixed Param Count": 0,
        }

# def calculate_deformation_magnitude(deformation_file):
#     """
#     Calculate magnitude statistics from a deformation field.
#     """
#     try:
#         deformation = sitk.ReadImage(deformation_file)
#         deformation_array = sitk.GetArrayFromImage(deformation)
#         magnitude = np.linalg.norm(deformation_array, axis=-1)
#         return {
#             "Deformation Magnitude Mean": np.mean(magnitude),
#             "Deformation Magnitude Std": np.std(magnitude),
#             "Deformation Magnitude Max": np.max(magnitude),
#             "Deformation Magnitude Min": np.min(magnitude),
#         }
#     except Exception as e:
#         print(f"Error calculating deformation magnitude for {deformation_file}: {e}")
#         return {
#             "Deformation Magnitude Mean": 0,
#             "Deformation Magnitude Std": 0,
#             "Deformation Magnitude Max": 0,
#             "Deformation Magnitude Min": 0,
#         }

def calculate_registration_residuals(fixed_image, moving_image):
    """
    Calculate residuals after registration.
    """
    try:
        fixed = sitk.ReadImage(fixed_image)
        moving = sitk.ReadImage(moving_image)
        fixed_array = sitk.GetArrayFromImage(fixed)
        moving_array = sitk.GetArrayFromImage(moving)
        residuals = np.abs(fixed_array - moving_array)
        return {
            "Registration Residuals Mean": np.mean(residuals),
            "Registration Residuals Std": np.std(residuals),
            "Registration Residuals Max": np.max(residuals),
            "Registration Residuals Min": np.min(residuals),
        }
    except Exception as e:
        print(f"Error calculating registration residuals for {fixed_image} and {moving_image}: {e}")
        return {
            "Registration Residuals Mean": 0,
            "Registration Residuals Std": 0,
            "Registration Residuals Max": 0,
            "Registration Residuals Min": 0,
        }

def extract_simulated_image_features(image_path):
    """
    Extracts basic features (e.g., entropy) from a simulated image.
    """
    try:
        image = sitk.ReadImage(image_path)
        image_array = sitk.GetArrayFromImage(image)

        # Calculate entropy as an example feature
        histogram, _ = np.histogram(image_array, bins=256, range=(np.min(image_array), np.max(image_array)))
        histogram = histogram / histogram.sum()
        entropy = -np.sum(histogram * np.log2(histogram + 1e-10))

        return {
            "Simulated Image Entropy": entropy,
        }
    except Exception as e:
        print(f"Error extracting features from {image_path}: {e}")
        return {
            "Simulated Image Entropy": 0,
        }

def calculate_entropy(image_path):
    """
    Calculate the entropy of an image.
    """
    try:
        image = sitk.ReadImage(image_path)
        image_array = sitk.GetArrayFromImage(image)
        histogram, _ = np.histogram(image_array, bins=256, range=(np.min(image_array), np.max(image_array)))
        histogram = histogram / histogram.sum()
        entropy = -np.sum(histogram * np.log2(histogram + 1e-10))
        return entropy
    except Exception as e:
        print(f"Error calculating entropy for {image_path}: {e}")
        return None

def simulate_mri_once(seq_file, coil_file, temp_slices_dir, output_nifti):
    """
    Simulates the MRI once, generates slices, converts to NIfTI, and saves the output.
    """
    os.makedirs(temp_slices_dir, exist_ok=True)

    print(f"Simulating MRI and saving slices in {temp_slices_dir}...")
    command = [
        sys.executable,
        "script_bart_png_nifti.py",
        "--seq", seq_file,
        "--coil", coil_file,
        "--slice-dir", temp_slices_dir,
        "--final-dir", os.path.dirname(output_nifti)  # Output NIfTI will be saved in the same directory
    ]
    print("Command:", command)

    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        print("Simulation STDOUT:", result.stdout)
        print("Simulation STDERR:", result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error during MRI Simulation: {e}")
        print(f"STDERR: {e.stderr}")
        raise e

    print(f"MRI Simulation completed. Simulated NIfTI saved at {output_nifti}")

def run_registration(tool_dir, patient_image, simulated_image, registered_image, deformation_field):
    """
    Executes Stage 2: Registration.
    """
    print(f"Running Registration for {patient_image}")

    if not os.path.exists(patient_image):
        print(f"Fixed image not found: {patient_image}")
        return False
    if not os.path.exists(simulated_image):
        print(f"Moving image not found: {simulated_image}")
        return False

    registration_command = [
        os.path.join(tool_dir, "3DRegAffine.exe"),
        "-f", patient_image,
        "-m", simulated_image,
        "-o", registered_image,
        "-T", deformation_field,
        "-y", "0", "-Y", "0", "-N", "0", "-L", "0", "-n", "0", "-l", "0", "-p", "0.2"
    ]

    try:
        result = subprocess.run(
            registration_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        print("Registration STDOUT:", result.stdout)
        print("Registration STDERR:", result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error during registration: {e}")
        print(f"STDERR: {e.stderr}")
        return False

def apply_deformation(deformation_file, coil_file, registered_image, output_dir):
    """
    Executes Stage 3: Deformation field application.
    """
    print(f"Applying deformation field for {registered_image}")
    os.makedirs(output_dir, exist_ok=True)

    command = [
        "python", "scripit_reg.py",
        "--deformation", deformation_file,
        "--coil", coil_file,
        "--registered", registered_image,
        "--output", output_dir
    ]

    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            errors='replace',
            check=True
        )
        print("Deformation Application STDOUT:", result.stdout)
        print("Deformation Application STDERR:", result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error applying deformation field: {e}")
        print(f"STDERR: {e.stderr}")
        return False

def main():
    # Input configurations
    seq_file = "D:/Downloads/ITP/seq/sdl_pypulseq_TE10_TR600_os2_largeCrush_xSpoil.seq"
    coil_file = "cloudMR_birdcagecoil.zip"
    simulated_mri_file = "D:/Downloads/ITP/outputs/simulated_mri_test.nii.gz"  
    temp_slices_dir = "D:/Downloads/ITP/axial/"  
    patient_dir = "D:/Downloads/target"  
    dataset_dir = "D:/Downloads/dataset"  
    tool_dir = "D:/Downloads/registrationMplus/build/bin/Release"  

    # Ensure dataset directory exists
    os.makedirs(dataset_dir, exist_ok=True)

    # Generate simulated MRI once
    if not os.path.exists(simulated_mri_file):
        simulate_mri_once(seq_file, coil_file, temp_slices_dir, simulated_mri_file)

    patient_images = glob(os.path.join(patient_dir, "*.nii"))

    excel_data = []

    for idx, patient_image in enumerate(patient_images, start=1):
        print(f"Processing Patient {idx}: {patient_image}")

        # Directories for this patient
        patient_folder = os.path.join(dataset_dir, f"patient_{idx:02d}")
        final_out_dir = os.path.join(patient_folder, "final")
        deformation_field = os.path.join(patient_folder, "deformation_01.txt")
        registered_image = os.path.join(patient_folder, "Registeredimage_01.nii")
        tcia_output_dir = os.path.join(patient_folder, "TCIA_outputs")

        # Ensure directories exist
        os.makedirs(patient_folder, exist_ok=True)
        os.makedirs(final_out_dir, exist_ok=True)

        simulated_mri_dest = os.path.join(final_out_dir, "simulated_mri.nii.gz")

        try:
            shutil.copy(simulated_mri_file, simulated_mri_dest)
            print(f"Simulated MRI stored at {simulated_mri_dest}")
        except Exception as e:
            print(f"Error copying simulated MRI for Patient {idx}: {e}")
            continue  

        # Stage 2: Registration
        if not run_registration(tool_dir, patient_image, simulated_mri_file, registered_image, deformation_field):
            print(f"Skipping Patient {idx} due to registration failure.")
            continue

        # Stage 3: Deformation Application
        if not apply_deformation(deformation_field, coil_file, registered_image, tcia_output_dir):
            print(f"Skipping Patient {idx} due to deformation application failure.")
            continue

        tcia_t1_path = os.path.join(tcia_output_dir, "TCIA_T1.nii.gz")
        tcia_t2_path = os.path.join(tcia_output_dir, "TCIA_T2.nii.gz")
        tcia_pd_path = os.path.join(tcia_output_dir, "TCIA_PD.nii.gz")

        # Extract features from deformation field, simulated image, and TCIA outputs
        deformation_features = extract_deformation_features(deformation_field)
        # deformation_magnitude_features = calculate_deformation_magnitude(deformation_field)
        simulated_image_features = extract_simulated_image_features(simulated_mri_dest)
        registration_residuals = calculate_registration_residuals(patient_image, registered_image)
        t1_entropy = calculate_entropy(tcia_t1_path) if os.path.exists(tcia_t1_path) else None
        t2_entropy = calculate_entropy(tcia_t2_path) if os.path.exists(tcia_t2_path) else None
        pd_entropy = calculate_entropy(tcia_pd_path) if os.path.exists(tcia_pd_path) else None
        registered_entropy = calculate_entropy(registered_image) if os.path.exists(registered_image) else None

        # Append metadata for this patient
        excel_data.append({
            "Patient ID": f"patient_{idx:02d}",
            "Patient Image Path": patient_image,
            "Simulated MRI Path": simulated_mri_dest,
            **deformation_features,
            # **deformation_magnitude_features,
            **simulated_image_features,
            **registration_residuals,
            "TCIA T1 Path": tcia_t1_path,
            "TCIA T1 Entropy": t1_entropy,
            "TCIA T2 Path": tcia_t2_path,
            "TCIA T2 Entropy": t2_entropy,
            "TCIA PD Path": tcia_pd_path,
            "TCIA PD Entropy": pd_entropy,
            "Registered Image Path": registered_image,
            "Registered Image Entropy": registered_entropy,
        })

    # Save Excel file
    excel_output_path = os.path.join(dataset_dir, "dataset.xlsx")
    df = pd.DataFrame(excel_data)
    df.to_excel(excel_output_path, index=False)
    print(f"Excel dataset saved at {excel_output_path}")

    print(f"Dataset creation completed. Outputs saved in {dataset_dir}")

if __name__ == "__main__":
    main()




