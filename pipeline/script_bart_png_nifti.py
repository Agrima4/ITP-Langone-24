# import sys
# sys.path.append("D:/Downloads/ITP/camrie/Lib/site-packages")
# import pynico_eros_montin.pynico as pn
# import cmtools.cm2D as cmh
# import cmtools.cm as cm
# import numpy as np
# import common as c
# import matplotlib.pyplot as plt
# import os
# import subprocess
# import pyable_eros_montin.imaginable as ima
# import SimpleITK as sitk

# # Timer and directory setup
# L = pn.Timer()
# L.start()
# B = pn.BashIt()

# direction = "axial"
# if len(sys.argv) > 3:
#     direction = sys.argv[3]

# OUTDIR = f"D:/Downloads/ITP/{direction}"
# if len(sys.argv) > 1:
#     OUTDIR = sys.argv[1]

# os.makedirs(OUTDIR, exist_ok=True)

# SEQ = "D:/Downloads/ITP/seq/sdl_pypulseq_TE10_TR600_os2_largeCrush_xSpoil.seq"
# coil = "cloudMR_birdcagecoil.zip"
# if len(sys.argv) > 4:
#     coil = sys.argv[4]

# print(f"OUTDIR={OUTDIR}", f"SEQ={SEQ}", f"coil={coil}", f"direction={direction}")

# # Reading coil data
# FIELD = c.readMarieOutput(coil)
# B0 = FIELD["B0"]
# GPU = False
# NT = 10
# desired_spin_resolution = (2e-3, 2e-3, 2e-3)
# SENS_DIR = pn.Pathable(FIELD["b1m"][0]).getPath()

# for SL in np.linspace(1, 120, 70, dtype=int):
#     print(f"Processing slice {SL}")
    
#     SL_OUTDIR = f"{OUTDIR}/{SL}/"
#     os.makedirs(SL_OUTDIR, exist_ok=True)

#     k = f"{SL_OUTDIR}/k.npz"
#     if os.path.exists(k):
#         data = np.load(k)["data"]
#     else:
#         try:
#             data = c.simulate_2D_slice(SL, B0, FIELD["T1"], FIELD["T2"], FIELD["T2star"], 
#                                        FIELD["dW"], FIELD["PD"], desired_spin_resolution, 
#                                        direction, SEQ, OUTDIR, SENS_DIR, GPU, NT, debug=True)
#             print(f"Slice {SL}: Simulated data type: {type(data)}, shape: {data.shape}")
#             np.savez(k, data=data)
#         except Exception as e:
#             print(f"Error during simulation for slice {SL}: {e}")
#             continue

#     BARTDIR = pn.createRandomTemporaryPathableFromFileName('a.cfl')
#     BARTDIR.appendPathRandom()
#     BARTDIR.ensureDirectoryExistence()
#     bartk = f"{BARTDIR.getPath()}/k"
#     bartr = f"{BARTDIR.getPath()}/"

#     c.write_cfl(data, bartk)

#     # Docker command for BART processing
#     command = [
#         'docker', 'run', 
#         '--platform', 'linux/amd64', 
#         '--mount', f'type=bind,source={BARTDIR.getPath()},target=/cfl',
#         '--mount', f'type=bind,source={SL_OUTDIR},target=/output',
#         '-it', '--entrypoint', '/bin/bash', 
#         'docker.io/biocontainers/bart:v0.4.04-2-deb_cv1',
#         '-c', 'bart fft -i 7 /cfl/k s && bart rss 8 s s2 && bart toimg s2 /output/g'
#     ]

#     try:
#         result = subprocess.run(command, capture_output=True, text=True, check=True)
#         print("STDOUT:", result.stdout)
#         print("STDERR:", result.stderr)
#     except subprocess.CalledProcessError as e:
#         print(f"Error in Docker processing for slice {SL}: {e}")
#         print("STDOUT:", e.stdout)
#         print("STDERR:", e.stderr)
#         continue

#     output_file = os.path.join(SL_OUTDIR, 'g.png')
#     if not os.path.exists(output_file):
#         print(f"Warning: Output file for slice {SL} not found: {output_file}")
#     else:
#         print(f"Output for slice {SL} is stored at: {output_file}")

# print("Processing complete.")

# import re
# from matplotlib.pyplot import imread  

# # Define the folder containing slices 
# slice_folder = "D:/Downloads/ITP/axial/"

# # Step 4: Automatically find all slice indices based on available subdirectories
# slice_indices = sorted([int(f) for f in os.listdir(slice_folder) if f.isdigit()])
# print(f"Found slice indices: {slice_indices}")

# # Generate list of slice file paths
# slice_files = [os.path.join(slice_folder, str(idx), "g.png") for idx in slice_indices if os.path.exists(os.path.join(slice_folder, str(idx), "g.png"))]

# # Load all slices into a 3D NumPy array and convert to grayscale
# def rgb_to_grayscale(rgb_image):
#     return 0.2989 * rgb_image[:, :, 0] + 0.5870 * rgb_image[:, :, 1] + 0.1140 * rgb_image[:, :, 2]

# slices = [rgb_to_grayscale(imread(slice_file)) for slice_file in slice_files] 
# array_3d = np.stack(slices, axis=0)  # Stack slices along the Z-axis

# # Normalize the array and scale to 16-bit integer
# array_3d /= np.max(array_3d)  
# array_3d *= 4096  
# array_3d = array_3d.astype(np.uint16)  

# # Convert the 3D NumPy array to a SimpleITK image
# sitk_image = sitk.GetImageFromArray(array_3d)

# # Set the calculated spacing
# sitk_image.SetSpacing((1.17, 1.17, 1.5))
# sitk_image.SetOrigin((0.0, 0.0, 0.0))   # Set origin at (0, 0, 0)

# # Save as NIfTI
# output_path = "D:/Downloads/ITP/outputs/axial_test_combined_03.nii.gz"
# sitk.WriteImage(sitk_image, output_path)

# print(f"3D volume has been saved as a NIfTI file at: {output_path}")

# # Verify the saved NIfTI file
# loaded_image = sitk.ReadImage(output_path)
# print(f"Saved Image Size: {loaded_image.GetSize()}")
# print(f"Saved Image Spacing: {loaded_image.GetSpacing()}")


import argparse
import sys
sys.path.append("D:/Downloads/ITP/camrie/Lib/site-packages")
import pynico_eros_montin.pynico as pn
import cmtools.cm2D as cmh
import cmtools.cm as cm
import numpy as np
import common as c
import os
import subprocess
import SimpleITK as sitk
from tqdm import tqdm
from matplotlib.pyplot import imread


def parse_arguments():
    """
    Parses command-line arguments for the script.
    """
    parser = argparse.ArgumentParser(description="MRI Simulation Script")
    parser.add_argument("--seq", required=True, help="Path to sequence file")
    parser.add_argument("--coil", required=True, help="Path to coil file")
    parser.add_argument("--slice-dir", required=True, help="Directory to save slices")
    parser.add_argument("--final-dir", required=True, help="Directory to save the NIfTI output")
    parser.add_argument("--direction", default="axial", help="Scan direction (default: axial)")
    return parser.parse_args()


def simulate_slices(seq, coil, slice_dir, direction="axial", resolution=(2e-3, 2e-3, 2e-3)):
    """
    Simulates MRI slices and processes them using Docker.
    """
    # Read coil data
    FIELD = c.readMarieOutput(coil)
    B0 = FIELD["B0"]
    SENS_DIR = pn.Pathable(FIELD["b1m"][0]).getPath()
    GPU = False
    NT = 10

    for SL in np.linspace(1, 120, 70, dtype=int):
        print(f"Processing slice {SL}")

        SL_OUTDIR = f"{slice_dir}/{SL}/"
        os.makedirs(SL_OUTDIR, exist_ok=True)

        k = f"{SL_OUTDIR}/k.npz"
        if os.path.exists(k):
            try:
                loaded_data = np.load(k)
                if "data" in loaded_data:
                    data = loaded_data["data"]
                else:
                    print(f"Key 'data' not found in {k}. Found keys: {list(loaded_data.keys())}")
                    print("Re-simulating slice...")
                    raise ValueError("Invalid .npz file structure")
            except Exception as e:
                print(f"Error loading {k}: {e}")
                print("Re-simulating slice...")
                try:
                    data = c.simulate_2D_slice(
                        SL, B0, FIELD["T1"], FIELD["T2"], FIELD["T2star"],
                        FIELD["dW"], FIELD["PD"], resolution,
                        direction, seq, slice_dir, SENS_DIR, GPU, NT, debug=True
                    )
                    np.savez(k, data=data)
                except Exception as sim_e:
                    print(f"Error during simulation for slice {SL}: {sim_e}")
                    continue
        else:
            try:
                data = c.simulate_2D_slice(
                    SL, B0, FIELD["T1"], FIELD["T2"], FIELD["T2star"],
                    FIELD["dW"], FIELD["PD"], resolution,
                    direction, seq, slice_dir, SENS_DIR, GPU, NT, debug=True
                )
                np.savez(k, data=data)
            except Exception as e:
                print(f"Error during simulation for slice {SL}: {e}")
                continue

        BARTDIR = pn.createRandomTemporaryPathableFromFileName('a.cfl')
        BARTDIR.appendPathRandom()
        BARTDIR.ensureDirectoryExistence()
        bartk = f"{BARTDIR.getPath()}/k"
        bartr = f"{BARTDIR.getPath()}/"

        c.write_cfl(data, bartk)

        # Docker command for BART processing
        command = [
            'docker', 'run',
            '--platform', 'linux/amd64',
            '--mount', f'type=bind,source={BARTDIR.getPath()},target=/cfl',
            '--mount', f'type=bind,source={SL_OUTDIR},target=/output',
            '-it', '--entrypoint', '/bin/bash',
            'docker.io/biocontainers/bart:v0.4.04-2-deb_cv1',
            '-c', 'bart fft -i 7 /cfl/k s && bart rss 8 s s2 && bart toimg s2 /output/g'
        ]

        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
        except subprocess.CalledProcessError as e:
            print(f"Error in Docker processing for slice {SL}: {e}")
            print("STDOUT:", e.stdout)
            print("STDERR:", e.stderr)
            continue

        output_file = os.path.join(SL_OUTDIR, 'g.png')
        if not os.path.exists(output_file):
            print(f"Warning: Output file for slice {SL} not found: {output_file}")
        else:
            print(f"Output for slice {SL} is stored at: {output_file}")

    print("Processing complete.")


def convert_to_nifti(slice_dir, output_path, spacing=(1.17, 1.17, 1.5)):
    """
    Stacks slices into a 3D volume and saves them as a NIfTI file.
    """
    slice_indices = sorted([int(f) for f in os.listdir(slice_dir) if f.isdigit()])
    print(f"Found slice indices: {slice_indices}")

    # Generate list of slice file paths
    slice_files = [os.path.join(slice_dir, str(idx), "g.png") for idx in slice_indices if os.path.exists(os.path.join(slice_dir, str(idx), "g.png"))]

    if not slice_files:
        raise ValueError("No valid slices found. Ensure Docker has generated 'g.png' files for each slice.")

    # Load all slices into a 3D NumPy array and convert to grayscale
    def rgb_to_grayscale(rgb_image):
        return 0.2989 * rgb_image[:, :, 0] + 0.5870 * rgb_image[:, :, 1] + 0.1140 * rgb_image[:, :, 2]

    slices = [rgb_to_grayscale(imread(slice_file)) for slice_file in slice_files]
    array_3d = np.stack(slices, axis=0)  # Stack slices along the Z-axis

    # Normalize the array and scale to 16-bit integer
    array_3d /= np.max(array_3d)
    array_3d *= 4096
    array_3d = array_3d.astype(np.uint16)

    # Convert the 3D NumPy array to a SimpleITK image
    sitk_image = sitk.GetImageFromArray(array_3d)

    # Set the calculated spacing
    sitk_image.SetSpacing(spacing)
    sitk_image.SetOrigin((0.0, 0.0, 0.0))  # Set origin at (0, 0, 0)

    # Save as NIfTI
    sitk.WriteImage(sitk_image, output_path)
    print(f"3D volume has been saved as a NIfTI file at: {output_path}")


if __name__ == "__main__":
    args = parse_arguments()

    # Simulate slices and generate NIfTI
    simulate_slices(args.seq, args.coil, args.slice_dir, args.direction)
    convert_to_nifti(args.slice_dir, os.path.join(args.final_dir, "simulated_mri.nii.gz"))



