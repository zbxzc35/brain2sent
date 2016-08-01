# Written by: Erick Cobos T (a01184587@itesm.mx)
# Date: 01-Aug-2016
""" Extract BOLD and ROI info and save as h5 files.

Reads matrices from Gallant's data, creates the brain mask, drops invalid
columns and generates a matrix (timesteps x voxels) for (1) original BOLD
activations and (2) temporally smoothed BOLD activations (1-d gaussian filter 
with sigma = 5 seconds). It also saves the ROI mask.

Works for train or test responses.
"""
import h5py
import numpy as np
from scipy import ndimage

# Read BOLD data file
voxel_file = h5py.File('VoxelResponses_subject1.mat', 'r')
rois = voxel_file['roi']
bold = voxel_file['rt'] # 'rv' for test responses

# Extract ROIs
brain = np.zeros([18, 64, 64])
roi_id = 1
for roi in rois:
	brain = brain + roi_id*np.array(rois[roi])
	print(roi, roi_id)
	roi_id += 1
	
# Extract BOLD
bold = np.array(bold).transpose()

# Select voxels from all regions
roi_mask = (brain > 0).flatten()
bold = bold[:, roi_mask]

# Clean data (delete columns with any nans)
nan_cols = np.isnan(bold).any(axis=0)
nan_mask = np.logical_not(nan_cols) 
bold = bold[:, nan_mask] # 8982 remaining voxels for S1
# Tested: Same voxels are dropped for train and test responses

# Save as BOLD
bold_file = h5py.File('bold.h5', 'w')
bold_file.create_dataset('responses', data=bold)
bold_file.close()

# Create smooth BOLD
smooth_bold = ndimage.gaussian_filter1d(bold, sigma=5, axis=0)

# Save as smooth BOLD
smooth_bold_file = h5py.File('smooth_bold.h5', 'w')
smooth_bold_file.create_dataset('responses', data=smooth_bold)
smooth_bold_file.close()

# Create ROI per voxel (later used for voxel selection)
roi_info = (brain[brain > 0])[nan_mask]

# Save ROI info
roi_file = h5py.File('roi_info.h5', 'w')
roi_file.create_dataset('rois', data=roi_info)
roi_file.close()

# Close voxel file
voxel_file.close()

print('Done!')



### Optionally,
import matplotlib.pyplot as plt

# Save ROIs as images (for visualization)
for i in range(18):
	plt.imsave('coronal_' + str(i+1) + '.png', brain[i,...])
