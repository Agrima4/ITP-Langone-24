import SimpleITK as sitk

# Load the NIfTI file
t2_image = sitk.ReadImage("/Users/agrimagupta/Downloads/ITP/def_output/TCIA_T2.nii.gz")

# Print the image size
print("Image Size:", t2_image.GetSize())

# Print the pixel spacing
print("Pixel Spacing:", t2_image.GetSpacing())

# Print the origin
print("Origin:", t2_image.GetOrigin())

# Print the direction cosines
print("Direction Cosines:", t2_image.GetDirection())

# Print the number of pixels and type
print("Number of Pixels:", t2_image.GetNumberOfPixels())
print("Pixel Type:", sitk.GetPixelIDValueAsString(t2_image.GetPixelID()))
