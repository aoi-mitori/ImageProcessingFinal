import cv2
import os
from skimage import color
from sklearn.preprocessing import StandardScaler
import numpy as np
from PIL import Image

img_dir_path = './image'
output_dir_path = './output'


def main():
    img_dir_full_path = os.path.join(os.path.dirname(os.path.realpath('__file__')), img_dir_path)
    img_dir = os.listdir(img_dir_full_path)

    h_mean = 0
    e_mean = 0
    d_mean = 0
    
    first=1
    for img_name in img_dir:
        img_path = os.path.join(img_dir_full_path, img_name)
    
        img = cv2.imread(img_path)
        img_h, img_w, _ = img.shape
        
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        img = np.array(img)

        s = np.reshape(color.rgb2hed(img), (-1, 3))
        scaler = StandardScaler()
        scaler.fit(s)
        
        if first==1:
            scaler.fit(s)
            mean = scaler.mean_
            h_mean = mean[0]
            e_mean = mean[1]
            d_mean = mean[2]

            print(f"h_mean: {h_mean}")
            print(f"e_mean: {e_mean}")
            print(f"d_mean: {d_mean}")

            first=0
        
        
            
        s = scaler.transform(s)
        s[: , 0] = s[: , 0] * 0.07
        s[: , 1] = s[: , 1] * 0.07
        s[: , 2] = s[: , 2] * 0.02

        
        nimg = color.hed2rgb(np.reshape(s, img.shape))

        imin = nimg.min()
        imax = nimg.max()
        rsimg = (255 * (nimg - imin) / (imax - imin)).astype('uint8')

        rsimg = Image.fromarray(rsimg)
        rsimg = rsimg = cv2.cvtColor(np.asarray(rsimg), cv2.COLOR_RGB2BGR)

        
        output_dir_full_path = os.path.join(os.path.dirname(os.path.realpath('__file__')), output_dir_path)
        output_img_dir_full_path = os.path.join(output_dir_full_path, img_name)
        
        cv2.imwrite(output_img_dir_full_path, rsimg)
        




if __name__=='__main__':
    main()