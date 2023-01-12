import os, glob
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import json
import cv2
from matplotlib.path import Path
from tqdm import tqdm


inputFolder = './input'
outputFolder = inputFolder+'-t'
img_ext = 'png'

# remove output folder if exists
if os.path.exists(outputFolder):
    os.system('rm -rf '+outputFolder)

# if folder not exist, create it
if not os.path.exists(outputFolder):
    os.makedirs(outputFolder)

imgfiles = glob.glob(inputFolder+'/*.'+img_ext)

for img_path in tqdm(imgfiles):
    img_obj = Image.open(img_path)
    img_array = np.array(img_obj)
    label_path = img_path.replace(img_ext, 'json').replace('images', 'labels')
    label_file = open(label_path)
    label_data = json.load(label_file)

    a = label_data['shapes']
    for b in a:
        c = b['points']

    width, height, _ = img_array.shape
    polygon = c
    width, height= img_obj.size
    poly_path=Path(polygon)
    x, y = np.mgrid[:height, :width]
    coors=np.hstack((x.reshape(-1, 1), y.reshape(-1,1)))
    mask = poly_path.contains_points(coors).reshape(height, width).T
    img_masked=np.zeros(img_array.shape,dtype=img_array.dtype)
    img_masked[mask]=img_array[mask]
    na = img_masked
    alpha = np.sum(na, axis=-1) > 0
    alpha = np.uint8(alpha * 255)
    res = np.dstack((na, alpha))

    img_name = img_path.split('\\')[-1][:-4]
    # Save result
    cv2.imwrite(outputFolder+'/'+img_name+'_t.png', res)

print("Done Thanks!")