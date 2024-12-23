# # import SimpleITK as sitk
# # import numpy as np
# # import common as c  # Assuming you have readMarieOutput function here

# # def parse_deformation_file(deformation_file):
# #     """
# #     Parse the deformation field from a .txt file.
# #     """
# #     with open(deformation_file, 'r') as f:
# #         lines = f.readlines()
    
# #     for line in lines:
# #         if line.startswith("Parameters:"):
# #             params = list(map(float, line.split("Parameters:")[1].strip().split()))
# #         elif line.startswith("FixedParameters:"):
# #             fixed_params = list(map(float, line.split("FixedParameters:")[1].strip().split()))
    
# #     return params, fixed_params

# # def create_affine_transform(params, fixed_params):
# #     """
# #     Create an affine transform using SimpleITK.
# #     """
# #     transform = sitk.AffineTransform(3)
# #     transform.SetParameters(params[:12])  # First 12 values are matrix and translation
# #     transform.SetFixedParameters(fixed_params)  # Center of rotation
# #     return transform

# # def apply_deformation_and_save(deformation_file, coil_file, registered_image, output_dir):
# #     """
# #     Apply the deformation field to T1, T2, and PD maps.
# #     """
# #     # Parse deformation field
# #     params, fixed_params = parse_deformation_file(deformation_file)
# #     transform = create_affine_transform(params, fixed_params)
    
# #     # Load coil data (T1, T2, PD maps)
# #     FIELD = c.readMarieOutput(coil_file)
# #     t1_path = FIELD["T1"]
# #     t2_path = FIELD["T2"]
# #     pd_path = FIELD["PD"]
    
# #     # Load registered image for reference (optional)
# #     registered_img = sitk.ReadImage(registered_image)
    
# #     # Load T1, T2, PD images
# #     t1_img = sitk.ReadImage(t1_path, sitk.sitkFloat32)
# #     t2_img = sitk.ReadImage(t2_path, sitk.sitkFloat32)
# #     pd_img = sitk.ReadImage(pd_path, sitk.sitkFloat32)
    
# #     # Apply the affine transform to each map
# #     resampler = sitk.ResampleImageFilter()
# #     resampler.SetReferenceImage(registered_img)
# #     resampler.SetInterpolator(sitk.sitkLinear)
# #     resampler.SetTransform(transform)
    
# #     tcia_t1 = resampler.Execute(t1_img)
# #     tcia_t2 = resampler.Execute(t2_img)
# #     tcia_pd = resampler.Execute(pd_img)
    
# #     # Save the outputs
# #     sitk.WriteImage(tcia_t1, f"{output_dir}/TCIA_T1.nii.gz")
# #     sitk.WriteImage(tcia_t2, f"{output_dir}/TCIA_T2.nii.gz")
# #     sitk.WriteImage(tcia_pd, f"{output_dir}/TCIA_PD.nii.gz")
    
# #     print(f"Aligned T1, T2, and PD maps saved to {output_dir}")

# # # Example usage
# # if __name__ == "__main__":
# #     deformation_file = "/Users/agrimagupta/Downloads/deformation_01.txt"
# #     coil_file = "cloudMR_birdcagecoil.zip"
# #     registered_image = "/Users/agrimagupta/Downloads/Registeredimage_01.nii"
# #     output_dir = "/Users/agrimagupta/Downloads/ITP/def_output"
    
# #     apply_deformation_and_save(deformation_file, coil_file, registered_image, output_dir)
# import sys
# sys.path.append("D:/Downloads/ITP/camrie/Lib/site-packages")  # Add this line
# import SimpleITK as sitk
# import common as c  # Assuming `common.py` has `readMarieOutput`

# def parse_deformation_file(deformation_file):
#     """
#     Parse the deformation field from a .txt file.
#     """
#     with open(deformation_file, 'r') as f:
#         lines = f.readlines()
    
#     for line in lines:
#         if line.startswith("Parameters:"):
#             params = list(map(float, line.split("Parameters:")[1].strip().split()))
#         elif line.startswith("FixedParameters:"):
#             fixed_params = list(map(float, line.split("FixedParameters:")[1].strip().split()))
    
#     return params, fixed_params

# def create_affine_transform(params, fixed_params):
#     """
#     Create an affine transform using SimpleITK.
#     """
#     transform = sitk.AffineTransform(3)
#     transform.SetParameters(params[:12])  # First 12 values are matrix and translation
#     transform.SetFixedParameters(fixed_params)  # Center of rotation
#     return transform

# def apply_deformation_and_save(deformation_file, coil_file, registered_image, output_dir):
#     """
#     Apply the deformation field to T1, T2, and PD maps.
#     """
#     # Parse deformation field
#     params, fixed_params = parse_deformation_file(deformation_file)
#     transform = create_affine_transform(params, fixed_params)
    
#     # Load coil data (T1, T2, PD maps)
#     FIELD = c.readMarieOutput(coil_file)
#     t1_path = FIELD["T1"]
#     t2_path = FIELD["T2"]
#     pd_path = FIELD["PD"]
    
#     # Load registered image for reference
#     registered_img = sitk.ReadImage(registered_image)
    
#     # Load T1, T2, PD images
#     t1_img = sitk.ReadImage(t1_path, sitk.sitkFloat64)
#     t2_img = sitk.ReadImage(t2_path, sitk.sitkFloat64)
#     pd_img = sitk.ReadImage(pd_path, sitk.sitkFloat64)
    
#     # Resample each map to align with the registered image
#     resampler = sitk.ResampleImageFilter()
#     resampler.SetReferenceImage(registered_img)  # Match metadata (size, spacing, origin)
#     resampler.SetInterpolator(sitk.sitkLinear)
#     resampler.SetTransform(transform)
    
#     tcia_t1 = resampler.Execute(t1_img)
#     tcia_t2 = resampler.Execute(t2_img)
#     tcia_pd = resampler.Execute(pd_img)
    
#     # Save the outputs
#     sitk.WriteImage(tcia_t1, f"{output_dir}/TCIA_T1.nii.gz")
#     sitk.WriteImage(tcia_t2, f"{output_dir}/TCIA_T2.nii.gz")
#     sitk.WriteImage(tcia_pd, f"{output_dir}/TCIA_PD.nii.gz")
    
#     print(f"Aligned T1, T2, and PD maps saved to {output_dir}")

# # Example usage
# if __name__ == "__main__":
#     deformation_file = "D:/Downloads/output/deformation_01.txt"
#     coil_file = "cloudMR_birdcagecoil.zip"  # Coil file used in Stage 1
#     registered_image ="D:/Downloads/output/Registeredimage_01.nii"
#     output_dir = "D:/Downloads/dataset/TCIA_outputs"
    
#     apply_deformation_and_save(deformation_file, coil_file, registered_image, output_dir)

import sys
sys.path.append("D:/Downloads/ITP/camrie/Lib/site-packages")

import argparse
import SimpleITK as sitk
import common as c  # Assuming `common.py` has `readMarieOutput`
import os

def parse_deformation_file(deformation_file):
    with open(deformation_file, 'r') as f:
        lines = f.readlines()
    
    params, fixed_params = [], []
    for line in lines:
        if line.startswith("Parameters:"):
            params = list(map(float, line.split("Parameters:")[1].strip().split()))
        elif line.startswith("FixedParameters:"):
            fixed_params = list(map(float, line.split("FixedParameters:")[1].strip().split()))
    return params, fixed_params

def create_affine_transform(params, fixed_params):
    transform = sitk.AffineTransform(3)
    transform.SetParameters(params[:12])  # First 12 values are the affine transform
    transform.SetFixedParameters(fixed_params)  # Center of rotation
    return transform

def apply_deformation_and_save(deformation_file, coil_file, registered_image, output_dir):
    # Parse the deformation field
    params, fixed_params = parse_deformation_file(deformation_file)
    transform = create_affine_transform(params, fixed_params)

    # Load coil data
    FIELD = c.readMarieOutput(coil_file)
    t1_path = FIELD["T1"]
    t2_path = FIELD["T2"]
    pd_path = FIELD["PD"]

    # Load reference (registered) image
    registered_img = sitk.ReadImage(registered_image)

    # Load T1, T2, and PD images
    t1_img = sitk.ReadImage(t1_path, sitk.sitkFloat32)
    t2_img = sitk.ReadImage(t2_path, sitk.sitkFloat32)
    pd_img = sitk.ReadImage(pd_path, sitk.sitkFloat32)

    # Apply the affine transform
    resampler = sitk.ResampleImageFilter()
    resampler.SetReferenceImage(registered_img)
    resampler.SetInterpolator(sitk.sitkLinear)
    resampler.SetTransform(transform)

    tcia_t1 = resampler.Execute(t1_img)
    tcia_t2 = resampler.Execute(t2_img)
    tcia_pd = resampler.Execute(pd_img)

    # Save the aligned images
    os.makedirs(output_dir, exist_ok=True)
    sitk.WriteImage(tcia_t1, f"{output_dir}/TCIA_T1.nii.gz")
    sitk.WriteImage(tcia_t2, f"{output_dir}/TCIA_T2.nii.gz")
    sitk.WriteImage(tcia_pd, f"{output_dir}/TCIA_PD.nii.gz")
    print(f"Aligned T1, T2, and PD maps saved to {output_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Apply Deformation Script")
    parser.add_argument("--deformation", required=True, help="Path to deformation field file")
    parser.add_argument("--coil", required=True, help="Path to coil file")
    parser.add_argument("--registered", required=True, help="Path to registered image")
    parser.add_argument("--output", required=True, help="Output directory for TCIA maps")
    args = parser.parse_args()

    apply_deformation_and_save(args.deformation, args.coil, args.registered, args.output)
