# import os
# import numpy as np
# import SimpleITK as sitk
# from matplotlib.pyplot import imread  # Use Pillow or OpenCV as alternatives

# # Step 1: Define the folder containing slices
# slice_folder = "/Users/agrimagupta/Downloads/ITP/axial/"
# slice_indices = [1, 7, 13, 19, 26, 32, 38, 44, 51, 57, 63, 69, 76, 82, 88, 94, 101, 107, 113, 120]  # Add all slice numbers here
# slice_files = [os.path.join(slice_folder, str(idx), "t.png") for idx in slice_indices]

# # Step 2: Load all slices into a 3D NumPy array
# slices = [imread(slice_file) for slice_file in slice_files]  # Load each PNG slice
# array_3d = np.stack(slices, axis=0)  # Stack slices along the Z-axis

# # Step 3: Convert the 3D NumPy array to a SimpleITK image
# sitk_image = sitk.GetImageFromArray(array_3d)

# # Step 4: Set metadata (optional)
# sitk_image.SetSpacing((2.0, 2.0, 2.0))  # Example spacing: 1mm x 1mm x 2mm
# sitk_image.SetOrigin((0.0, 0.0, 0.0))   # Set origin at (0, 0, 0)

# # Step 5: Save as NIfTI
# output_path = "/Users/agrimagupta/Downloads/ITP/outputs/axial_test_02.nii.gz"
# sitk.WriteImage(sitk_image, output_path)

# print("3D volume has been saved as a NIfTI file.")


# loaded_image = sitk.ReadImage(output_path)
# print(f"Image Size: {loaded_image.GetSize()}")
# print(f"Image Spacing: {loaded_image.GetSpacing()}")



# import os
# import numpy as np
# import SimpleITK as sitk
# from matplotlib.pyplot import imread  # Use Pillow or OpenCV as alternatives

# # Step 1: Define the folder containing slices
# slice_folder = "/Users/agrimagupta/Downloads/ITP/axial/"

# # Automatically find all slice indices based on available subdirectories
# # Assumes subdirectories are named numerically (e.g., "1", "7", "13")
# slice_indices = sorted([int(f) for f in os.listdir(slice_folder) if f.isdigit()])
# print(f"Found slice indices: {slice_indices}")

# # Generate list of slice file paths
# slice_files = [os.path.join(slice_folder, str(idx), "t.png") for idx in slice_indices if os.path.exists(os.path.join(slice_folder, str(idx), "t.png"))]

# # Step 2: Load all slices into a 3D NumPy array
# slices = [imread(slice_file) for slice_file in slice_files]  # Load each PNG slice
# array_3d = np.stack(slices, axis=0)  # Stack slices along the Z-axis

# # Step 3: Convert the 3D NumPy array to a SimpleITK image
# sitk_image = sitk.GetImageFromArray(array_3d)

# image_shape = array_3d.shape  # (Z, Y, X)
# print(f"Image Shape (Z, Y, X): {image_shape}")

# # Step 4: Set metadata (optional)
# sitk_image.SetSpacing((2.0, 2.0, 2.0))  # Example spacing: 2mm x 2mm x 2mm
# sitk_image.SetOrigin((0.0, 0.0, 0.0))   # Set origin at (0, 0, 0)

# # Step 5: Save as NIfTI
# output_path = "/Users/agrimagupta/Downloads/ITP/outputs/axial_test70_02.nii.gz"
# sitk.WriteImage(sitk_image, output_path)

# print("3D volume has been saved as a NIfTI file.")

# # Verify the saved NIfTI file
# loaded_image = sitk.ReadImage(output_path)
# print(f"Image Size: {loaded_image.GetSize()}")
# print(f"Image Spacing: {loaded_image.GetSpacing()}")

# import os
# import re
# import numpy as np
# import SimpleITK as sitk
# from matplotlib.pyplot import imread  # Use Pillow or OpenCV as alternatives

# # Step 1: Extract FOV from the .seq file
# # def extract_fov_from_seq(seq_file_path):
# #     fov_x, fov_y, fov_z = None, None, None
# #     with open(seq_file_path, 'r') as file:
# #         for line in file:
# #             # Match FOV lines (e.g., "FOV 200 200 200" or similar format)
# #             if "FOV" in line.upper():
# #                 match = re.findall(r"[-+]?\d*\.\d+|\d+", line)  # Extract numbers (floats or integers)
# #                 if len(match) >= 3:
# #                     fov_x, fov_y, fov_z = map(float, match[:3])  # Convert to float
# #                     break
# #     return fov_x, fov_y, fov_z

# # Step 2: Define the folder containing slices and the .seq file
# slice_folder = "/Users/agrimagupta/Downloads/ITP/axial/"
# #seq_file_path = "/Users/agrimagupta/Downloads/ITP/seq/sdl_pypulseq_TE10_TR4000_os2_largeCrush_xSpoil.seq"

# # Step 3: Extract FOV values from the .seq file
# #fov_x, fov_y, fov_z = extract_fov_from_seq(seq_file_path)

# # #if fov_x and fov_y and fov_z:
# #     print(f"Extracted FOV values (m): X={fov_x}, Y={fov_y}, Z={fov_z}")
# # #else:
# #     print("FOV values not found in the .seq file. Please check the file.")
# #     exit()

# # Step 4: Automatically find all slice indices based on available subdirectories
# slice_indices = sorted([int(f) for f in os.listdir(slice_folder) if f.isdigit()])
# print(f"Found slice indices: {slice_indices}")

# # Generate list of slice file paths
# slice_files = [os.path.join(slice_folder, str(idx), "t.png") for idx in slice_indices if os.path.exists(os.path.join(slice_folder, str(idx), "t.png"))]

# # Step 5: Load all slices into a 3D NumPy array
# slices = [imread(slice_file) for slice_file in slice_files]  # Load each PNG slice
# array_3d = np.stack(slices, axis=0)  # Stack slices along the Z-axis

# # # Step 6: Calculate image spacing based on FOV and image shape
# # shape_z, shape_y, shape_x = array_3d.shape[:3]
# # spacing_x = (fov_x *1000)/ shape_x
# # spacing_y = (fov_y * 1000) / shape_y
# # spacing_z = (fov_z * 1000) / shape_z

# # print(f"Image Shape (Z, Y, X): {array_3d.shape}")
# # print(f"Calculated Spacing: X={spacing_x:.3f}, Y={spacing_y:.3f}, Z={spacing_z:.3f}")

# # Step 7: Convert the 3D NumPy array to a SimpleITK image
# array3d = array_3d/np.max(array_3d)
# array_3d *= 4096
# sitk_image = sitk.GetImageFromArray(array_3d.astype(np.uint16)) #casting array in int 16

# # Set the calculated spacing
# sitk_image.SetSpacing((1.17, 1.17, 5))
# sitk_image.SetOrigin((0.0, 0.0, 0.0))   # Set origin at (0, 0, 0)

# # Step 8: Save as NIfTI
# output_path = "/Users/agrimagupta/Downloads/ITP/outputs/axial_test_with_fov.nii.gz"
# sitk.WriteImage(sitk_image, output_path)

# print(f"3D volume has been saved as a NIfTI file at: {output_path}")

# # Step 9: Verify the saved NIfTI file
# loaded_image = sitk.ReadImage(output_path)
# print(f"Saved Image Size: {loaded_image.GetSize()}")
# print(f"Saved Image Spacing: {loaded_image.GetSpacing()}")


import os
import re
import numpy as np
import SimpleITK as sitk
from matplotlib.pyplot import imread  # Use Pillow or OpenCV as alternatives

# Step 2: Define the folder containing slices and the .seq file
slice_folder = "/Users/agrimagupta/Downloads/ITP/axial/"

# Step 4: Automatically find all slice indices based on available subdirectories
slice_indices = sorted([int(f) for f in os.listdir(slice_folder) if f.isdigit()])
print(f"Found slice indices: {slice_indices}")

# Generate list of slice file paths
slice_files = [os.path.join(slice_folder, str(idx), "t.png") for idx in slice_indices if os.path.exists(os.path.join(slice_folder, str(idx), "t.png"))]

# Step 5: Load all slices into a 3D NumPy array and convert to grayscale
def rgb_to_grayscale(rgb_image):
    """Convert an RGB image to grayscale using the standard luminosity method."""
    return 0.2989 * rgb_image[:, :, 0] + 0.5870 * rgb_image[:, :, 1] + 0.1140 * rgb_image[:, :, 2]

slices = [rgb_to_grayscale(imread(slice_file)) for slice_file in slice_files]  # Convert each RGB slice to grayscale
array_3d = np.stack(slices, axis=0)  # Stack slices along the Z-axis

# Normalize the array and scale to 16-bit integer
array_3d /= np.max(array_3d)  # Normalize to [0, 1]
array_3d *= 4096  # Scale to 12-bit range
array_3d = array_3d.astype(np.uint16)  # Convert to uint16

# Step 7: Convert the 3D NumPy array to a SimpleITK image
sitk_image = sitk.GetImageFromArray(array_3d)

# Set the calculated spacing
sitk_image.SetSpacing((1.17, 1.17, 1.5))
sitk_image.SetOrigin((0.0, 0.0, 0.0))   # Set origin at (0, 0, 0)

# Step 8: Save as NIfTI
output_path = "/Users/agrimagupta/Downloads/ITP/outputs/axial_test_with_fov_04.nii.gz"
sitk.WriteImage(sitk_image, output_path)

print(f"3D volume has been saved as a NIfTI file at: {output_path}")

# Step 9: Verify the saved NIfTI file
loaded_image = sitk.ReadImage(output_path)
print(f"Saved Image Size: {loaded_image.GetSize()}")
print(f"Saved Image Spacing: {loaded_image.GetSpacing()}")

