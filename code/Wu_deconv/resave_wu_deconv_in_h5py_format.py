# Written by: Erick Cobos T
# Date: 19-July-2016
""" Opens the wu_deconv.h5 generated by Octave and resaves it with h5py

Called from generate_wu_deconv.m. Done for the convenience of having all data 
in a similar standard format.
"""
import h5py
import numpy as np

# Read Octave file
wu_deconv_file = h5py.File('wu_deconv.h5', 'r')
deconv_bold = np.array(wu_deconv_file['deconv_bold']['value']).transpose()
HRFs = np.array(wu_deconv_file['HRFs']['value']).transpose()
wu_deconv_file.close()

# Save deconv BOLD
deconv_file = h5py.File('wu_deconv.h5', 'w') # deletes old version
deconv_file.create_dataset('responses', data=deconv_bold)
deconv_file.close()

# Save HRFs
hrfs_file = h5py.File('wu_hrfs.h5', 'w')
hrfs_file.create_dataset('HRFs', data=HRFs)
hrfs_file.close()
