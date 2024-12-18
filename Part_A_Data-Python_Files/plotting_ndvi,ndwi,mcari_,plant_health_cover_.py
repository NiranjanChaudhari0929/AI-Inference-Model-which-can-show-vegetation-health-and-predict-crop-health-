# -*- coding: utf-8 -*-
"""Plotting NDVI,NDWI,MCARI ,Plant health cover  .ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1AgfrA2m3gEXVD2evhf5a0XgzUHosdUg5

import required libraries
"""

# Commented out IPython magic to ensure Python compatibility.
#import required libraries
import rasterio
from rasterio import plot
import matplotlib.pyplot as plt
import numpy as np
# %matplotlib inline

"""Uploading the multispectral images of the same image

Uplaod the images in the google collaboratory interface
This will work for any image
file ending with 1 is for :blue
file ending with 2 is for :green
file ending with 3 is for :red
file ending with 5 is for :NIR
"""

band1=rasterio.open('/content/DJI_0051.TIF') #blue
band2=rasterio.open('/content/DJI_0052.TIF') #green
band3 = rasterio.open('/content/DJI_0053.TIF') #red
band5 = rasterio.open('/content/DJI_0055.TIF') #nir

"""Calculation NIR(Near Infra Red) and Red spectrum"""

#type of raster byte
band3.dtypes[0]
#raster sytem of reference
band3.crs
#raster transform parameters
band3.transform
#raster values as matrix array
band3.read(1)
#multiple band representation
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))


plot.show(band3, ax=ax1, cmap='Blues') #red
plot.show(band5, ax=ax2, cmap='Blues') #nir
fig.tight_layout()
#generate nir and red objects as arrays in float64 format
red = band3.read(1).astype('float64')
nir = band5.read(1).astype('float64')

nir

"""Calcuation of Blue and Green spectrum"""

#type of raster byte
band1.dtypes[0]
#raster sytem of reference
band1.crs
#raster transform parameters
band3.transform
#raster values as matrix array
band1.read(1)
#multiple band representation
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))


plot.show(band1, ax=ax1, cmap='Blues') #blue
plot.show(band2, ax=ax2, cmap='Blues') #green
fig.tight_layout()
#generate nir and red objects as arrays in float64 format
blue = band1.read(1).astype('float64')
green = band2.read(1).astype('float64')

green

"""Calculating NDVI value

Normalized Difference Vegetation Index (NDVI)
"""

#ndvi calculation, empty cells or nodata cells are reported as 0
ndvi=np.where(
    (nir+red)==0.,
    0,
    (nir-red)/(nir+red))
ndvi[:5,:5]  #this only prints first 5 rows and first 5 columns

"""Normalized Difference Water Index (NDWI)

"""

#ndvi calculation, empty cells or no data cells are reported as 0
ndwi=np.where(
    (green+nir)==0.,
    0,
    (nir-green)/(nir+green))
ndwi[:5,:5]

"""Expiratory variability index (EVI)"""

#ndvi calculation, empty cells or no data cells are reported as 0
evi=np.where(
    (nir + (6 * red) - (7.5 * blue) + 1)==0.,
    0,
    2.5 * ((nir - red) / (nir + (6 * red) - (7.5 * blue) + 1)))
evi[:5,:5]

"""Changing sign of elements as the formula applied above was inverse"""

#ndvi calculation, empty cells or no data cells are reported as 0
evi=np.where(
    (nir + (6 * red) - (7.5 * blue) + 1)==0.,
    0,
    2.5 * ((nir - red) / (nir + (6 * red) - (7.5 * blue) + 1)))
evi[:5,:5]

"""MCARI index"""

# Assuming you have the values for the Near-Infrared (nir) and Red (red) bands

# Calculate MCARI, handling empty cells or nodata cells
mcari_condition = (nir - red) - 0.2 * (nir - red) * (nir / red)
mcari = np.where(mcari_condition, mcari_condition, np.nan)

# Printing the first 5x5 values of the calculated MCARI
print(mcari[:5, :5])

"""Printing the indices on a color gradient plot"""

import os

output_directory = '../Output/'
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

"""NDVI plotting"""

import rasterio
import matplotlib.pyplot as plt
import os

# Assuming you have already calculated the NDVI and have the variables 'ndvi' and 'band4' available

# Create the output directory if it doesn't exist
output_directory = '../Output/'
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Export NDVI image
ndviImage = rasterio.open(output_directory + 'ndviImage.tiff', 'w', driver='Gtiff',
                          width=band3.width,
                          height=band3.height,
                          count=1, crs=band3.crs,
                          transform=band3.transform,
                          dtype='float64')
ndviImage.write(ndvi, 1)
ndviImage.close()

# Plot NDVI
ndvi_data = rasterio.open(output_directory + 'ndviImage.tiff')
fig = plt.figure(figsize=(18, 12))
plt.imshow(ndvi_data.read(1), cmap='viridis')  # Assuming NDVI is in band 1
plt.title('NDVI Image')
plt.colorbar(label='NDVI Value')
plt.show()
plt.savefig('/ndvi_plot.png')
plt.savefig('/content/ndvi.png')

"""Plotting NDWI on color graded plot"""

import os

output_directory = '../Output/'
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

import rasterio
import matplotlib.pyplot as plt
import os

# Assuming you have already calculated the NDVI and have the variables 'ndvi' and 'band4' available

# Create the output directory if it doesn't exist
output_directory = '../Output/'
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Export NDVI image
ndwiImage = rasterio.open(output_directory + 'ndwiImage.tiff', 'w', driver='Gtiff',
                          width=band1.width,
                          height=band1.height,
                          count=1, crs=band1.crs,
                          transform=band1.transform,
                          dtype='float64')
ndwiImage.write(ndwi, 1)
ndwiImage.close()

# Plot NDVI
ndwi_data = rasterio.open(output_directory + 'ndwiImage.tiff')
fig = plt.figure(figsize=(18, 12))
plt.imshow(ndwi_data.read(1), cmap='viridis')  # Assuming NDVI is in band 1
plt.title('NDWI Image')
plt.colorbar(label='NDWI Value')
plt.show()
plt.savefig('/content/ndwi.png')

"""MCARI Plot"""

import os

output_directory = '../Output/'
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

import rasterio
import matplotlib.pyplot as plt
import os

# Assuming you have already calculated the NDVI and have the variables 'ndvi' and 'band4' available

# Create the output directory if it doesn't exist
output_directory = '../Output/'
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Export NDVI image
mcariImage = rasterio.open(output_directory + 'mcariImage.tiff', 'w', driver='Gtiff',
                          width=band3.width,
                          height=band3.height,
                          count=1, crs=band3.crs,
                          transform=band3.transform,
                          dtype='float64')
mcariImage.write(mcari, 1)
mcariImage.close()

# Plot NDVI
mcari_data = rasterio.open(output_directory + 'mcariImage.tiff')
fig = plt.figure(figsize=(18, 12))
plt.imshow(mcari_data.read(1), cmap='viridis')  # Assuming NDVI is in band 1
plt.title('MCARI Image')
plt.colorbar(label='MCARI Value')
plt.show()

"""(MCARI) have been used to measure canopy cover and chlorophyll content of plants

"""

import os

output_directory = '../Output/'
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

import rasterio
import matplotlib.pyplot as plt
import os

# Assuming you have already calculated the EVI and have the variables 'evi' and 'band3' available

# Create the output directory if it doesn't exist
output_directory = '../Output/'
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Export EVI image
eviImage = rasterio.open(output_directory + 'eviImage.tiff', 'w', driver='Gtiff',
                          width=band3.width,
                          height=band3.height,
                          count=1, crs=band3.crs,
                          transform=band3.transform,
                          dtype='float64')
eviImage.write(evi, 1)
eviImage.close()

# Plot EVI
evi_data = rasterio.open(output_directory + 'eviImage.tiff')
fig = plt.figure(figsize=(18, 12))

# Specify the desired range for the color bar
vmin = +1  # Replace with your desired minimum value
vmax = -1   # Replace with your desired maximum value

plt.imshow(evi_data.read(1), cmap='viridis', vmin=vmin, vmax=vmax)  # Assuming EVI is in band 1
plt.title('EVI Image')
plt.colorbar(label='EVI Value')
plt.show()

"""FInding healthy and Unhealthy plant cover

Concept obtained from research popers:

EVI value
Between 0.2 to 0.8 is healthy
As we go close to 0 it is unhealthy
"""

#finding the size of our arrays
print(evi.size)
print(ndvi.size)
print(ndwi.size)
#proceed if evryone has same size

#define various parameters
unhealthy=0
sparse=0
moderate=0
healthy=0


for i in range(len(ndvi)):
  for j in range(len(ndvi[0])):
    if(0<ndvi[i][j]<0.2):
      sparse+=1
    elif(0.2<ndvi[i][j]<0.5):
      moderate+=1
    elif(ndvi[i][j]>0.5):
      healthy+=1
    else:
      unhealthy+=1


print((unhealthy/ndvi.size)*100)
print((sparse/ndvi.size)*100)
print((moderate/ndvi.size)*100)
print((healthy/ndvi.size)*100)

"""This Plot shows the index on the gradient scale"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# Define the NDVI values and their corresponding colors
ndvi_ranges = [-1, 0.2, 0.5, 1]
colors = ['blue', 'red', 'green', 'yellow']

# Create a colormap with specified colors for each NDVI range
cmap = ListedColormap(colors)

# Assuming you have already calculated the NDVI and have the variable 'ndvi' available
# Replace this with your actual NDVI values

# Plot NDVI with custom colormap
fig = plt.figure(figsize=(18, 12))
plt.imshow(ndvi, cmap=cmap, vmin=-1, vmax=1)  # Set the min and max values for the color map
plt.title('NDVI Image with Custom Colormap')
plt.colorbar(label='NDVI Value')
plt.show()
plt.savefig('/content/final.png')

"""This Plot shows the type of vegetation  on the gradient scale"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# Define the NDVI values and their corresponding colors
ndvi_ranges = [-1, 0.2, 0.5, 1]
colors = ['blue', 'red', 'green', 'yellow']

# Create a colormap with specified colors for each NDVI range
cmap = ListedColormap(colors)

# Assuming you have already calculated the NDVI and have the variable 'ndvi' available
# Replace this with your actual NDVI values

# Plot NDVI with custom colormap
fig = plt.figure(figsize=(18, 12))
plt.imshow(ndvi, cmap=cmap, vmin=-1, vmax=1)  # Set the min and max values for the color map
plt.title('NDVI Image with Custom Colormap')

# Create a colorbar with legend labels corresponding to the NDVI ranges
cbar = plt.colorbar(cmap=cmap, ticks=np.linspace(-1, 1, len(ndvi_ranges)))
cbar.ax.set_yticklabels(['Unhealthy', 'Sparse', 'Moderate', 'Healthy'])

plt.show()
plt.savefig('/content/final.png')