# # 
# import sys
# sys.path.append("D:/Downloads/ITP/camrie/Lib/site-packages")  # Add this line

# import os
# import subprocess
# import SimpleITK as sitk
# import common as c  # Assuming `readMarieOutput` is available
# from glob import glob


# def simulate_mri_once(seq_file, coil_file, output_nifti):
#     """
#     Simulates the MRI once and saves it as a NIfTI file.
#     """
#     print(f"Simulating MRI once and saving to {output_nifti}...")
#     command = [
#         sys.executable,
#         "script_bart_png_nifti.py",
#         "--seq", seq_file,
#         "--coil", coil_file,
#         "--output", output_nifti,
#     ]
#     print("Command:", command)

#     try:
#         result = subprocess.run(
#             command,
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             text=True,  # Ensure output is decoded
#             encoding='utf-8',
#             errors='replace'  # Replace invalid characters
#         )
#         print("Simulation STDOUT:", result.stdout)
#         print("Simulation STDERR:", result.stderr)
#     except subprocess.CalledProcessError as e:
#         print(f"Error during MRI Simulation: {e}")
#         print(f"STDERR: {e.stderr}")
#         raise e
#     print(f"MRI Simulation completed. Simulated NIfTI saved at {output_nifti}")


# def run_registration(tool_dir, patient_image, simulated_image, registered_image, deformation_field):
#     """
#     Executes Stage 2: Registration.
#     """
#     print(f"Running Registration for {patient_image}")

#     if not os.path.exists(patient_image):
#         print(f"Fixed image not found: {patient_image}")
#         return
#     if not os.path.exists(simulated_image):
#         print(f"Moving image not found: {simulated_image}")
#         return

#     registration_command = [
#         os.path.join(tool_dir, "3DRegAffine.exe"),
#         "-f", patient_image,
#         "-m", simulated_image,
#         "-o", registered_image,
#         "-T", deformation_field,
#         "-y", "0", "-Y", "0", "-N", "0", "-L", "0", "-n", "0", "-l", "0", "-p", "0.2"
#     ]

#     try:
#         result = subprocess.run(
#             registration_command,
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             text=True,
#             encoding='utf-8',
#             errors='replace'
#         )
#         print("Registration STDOUT:", result.stdout)
#         print("Registration STDERR:", result.stderr)
#     except subprocess.CalledProcessError as e:
#         print(f"Error during registration: {e}")
#         print(f"STDERR: {e.stderr}")
#         raise e


# def apply_deformation(deformation_file, coil_file, registered_image, output_dir):
#     """
#     Executes Stage 3: Deformation field application.
#     """
#     print(f"Applying deformation field for {registered_image}")
#     os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists

#     command = [
#         "python", "scripit_reg.py",  # Call the deformation script
#         "--deformation", deformation_file,
#         "--coil", coil_file,
#         "--registered", registered_image,
#         "--output", output_dir  # Pass the correct output directory
#     ]

#     try:
#         result = subprocess.run(
#             command,
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             text=True,
#             encoding='utf-8',
#             errors='replace',
#             check=True  # Ensure errors are raised
#         )
#         print("Deformation Application STDOUT:", result.stdout)
#         print("Deformation Application STDERR:", result.stderr)
#     except subprocess.CalledProcessError as e:
#         print(f"Error applying deformation field: {e}")
#         print(f"STDERR: {e.stderr}")
#         raise e


# def main():
#     # Input configurations
#     seq_file = "D:/Downloads/ITP/seq/sdl_pypulseq_TE10_TR600_os2_largeCrush_xSpoil.seq"
#     coil_file = "cloudMR_birdcagecoil.zip"
#     simulated_mri_file = "D:/Downloads/ITP/simulated_mri.nii.gz"  # Path for pre-generated simulated MRI
#     patient_dir = "D:/Downloads/target"  # Folder containing patient images
#     dataset_dir = "D:/Downloads/dataset"  # Folder to store the final dataset
#     tool_dir = "D:/Downloads/registrationMplus/build/bin/Release"  # Directory containing 3DRegAffine.exe

#     # Ensure dataset directory exists
#     os.makedirs(dataset_dir, exist_ok=True)

#     # Step 1: Generate simulated MRI once
#     if not os.path.exists(simulated_mri_file):
#         simulate_mri_once(seq_file, coil_file, simulated_mri_file)

#     # List all patient images
#     patient_images = glob(os.path.join(patient_dir, "*.nii"))

#     for idx, patient_image in enumerate(patient_images, start=1):
#         print(f"Processing Patient {idx}: {patient_image}")

#         # Directories for this patient
#         patient_folder = os.path.join(dataset_dir, f"patient_{idx:02d}")
#         final_out_dir = os.path.join(patient_folder, "final")
#         deformation_field = os.path.join(patient_folder, "deformation_01.txt")
#         registered_image = os.path.join(patient_folder, "Registeredimage_01.nii")
#         tcia_output_dir = os.path.join(patient_folder, "TCIA_outputs")

#         # Ensure patient folder exists
#         os.makedirs(patient_folder, exist_ok=True)

#         # Stage 2: Registration
#         run_registration(tool_dir, patient_image, simulated_mri_file, registered_image, deformation_field)

#         # Stage 3: Deformation Application
#         apply_deformation(deformation_field, coil_file, registered_image, tcia_output_dir)

#     print(f"Dataset creation completed. Outputs saved in {dataset_dir}")


# if __name__ == "__main__":
#     main()


import sys
sys.path.append("D:/Downloads/ITP/camrie/Lib/site-packages")

import os
import shutil  # For cleaning up temporary directories
import subprocess
import SimpleITK as sitk
import common as c  # Assuming `readMarieOutput` is available
from glob import glob


def simulate_mri_once(seq_file, coil_file, temp_slices_dir, output_nifti):
    """
    Simulates the MRI once, generates slices, converts to NIfTI, and saves the output.
    """
    # Ensure temporary slice directory exists
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

    # # Cleanup temporary slice directory
    # print(f"Cleaning up temporary slice directory: {temp_slices_dir}")
    # shutil.rmtree(temp_slices_dir, ignore_errors=True)


def run_registration(tool_dir, patient_image, simulated_image, registered_image, deformation_field):
    """
    Executes Stage 2: Registration.
    """
    print(f"Running Registration for {patient_image}")

    if not os.path.exists(patient_image):
        print(f"Fixed image not found: {patient_image}")
        return
    if not os.path.exists(simulated_image):
        print(f"Moving image not found: {simulated_image}")
        return

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
    except subprocess.CalledProcessError as e:
        print(f"Error during registration: {e}")
        print(f"STDERR: {e.stderr}")
        raise e


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
    except subprocess.CalledProcessError as e:
        print(f"Error applying deformation field: {e}")
        print(f"STDERR: {e.stderr}")
        raise e


def main():
    # Input configurations
    seq_file = "D:/Downloads/ITP/seq/sdl_pypulseq_TE10_TR600_os2_largeCrush_xSpoil.seq"
    coil_file = "cloudMR_birdcagecoil.zip"
    simulated_mri_file = "D:/Downloads/ITP/outputs/simulated_mri.nii.gz"  # Path for pre-generated simulated MRI
    temp_slices_dir = "D:/Downloads/ITP/axial/"  # directory for slices
    patient_dir = "D:/Downloads/target"  # Folder containing patient images
    dataset_dir = "D:/Downloads/dataset"  # Folder to store the final dataset
    tool_dir = "D:/Downloads/registrationMplus/build/bin/Release"  # Directory containing 3DRegAffine.exe

    # Ensure dataset directory exists
    os.makedirs(dataset_dir, exist_ok=True)

    # Step 1: Generate simulated MRI once
    if not os.path.exists(simulated_mri_file):
        simulate_mri_once(seq_file, coil_file, temp_slices_dir, simulated_mri_file)

    # List all patient images
    patient_images = glob(os.path.join(patient_dir, "*.nii"))

    for idx, patient_image in enumerate(patient_images, start=1):
        print(f"Processing Patient {idx}: {patient_image}")

        # Directories for this patient
        patient_folder = os.path.join(dataset_dir, f"patient_{idx:02d}")
        final_out_dir = os.path.join(patient_folder, "final")
        deformation_field = os.path.join(patient_folder, "deformation_01.txt")
        registered_image = os.path.join(patient_folder, "Registeredimage_01.nii")
        tcia_output_dir = os.path.join(patient_folder, "TCIA_outputs")

        # Ensure patient folder exists
        os.makedirs(patient_folder, exist_ok=True)
        os.makedirs(final_out_dir, exist_ok=True)

        # Path to the global simulated image
        simulated_mri_source = "D:/Downloads/ITP/outputs/simulated_mri.nii.gz"
    
    # Path to store the simulated image for this patient
        simulated_mri_dest = os.path.join(final_out_dir, "simulated_mri.nii.gz")
    
    # Copy the simulated MRI to the patient's directory
        try:
            shutil.copy(simulated_mri_source, simulated_mri_dest)
            print(f"Simulated MRI stored at {simulated_mri_dest}")
        except Exception as e:
            print(f"Error copying simulated MRI for Patient {idx}: {e}")
            continue  # Skip to the next patient if there’s an error

        # Stage 2: Registration
        run_registration(tool_dir, patient_image, simulated_mri_file, registered_image, deformation_field)

        # Stage 3: Deformation Application
        apply_deformation(deformation_field, coil_file, registered_image, tcia_output_dir)

    print(f"Dataset creation completed. Outputs saved in {dataset_dir}")


if __name__ == "__main__":
    main()
