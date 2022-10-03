from fileinput import close
import os, sys
import cv2
import numpy as np

label_dir_path = "D:\OBJ_Train_Datasets\compete_result_generate\labels"  #change
upload_file_path = "complete_result.json"  #change
image_file_path = "D:\\OBJ_Train_Datasets\\Public_Image\\Public_00000001.jpg"  #change


fp = open(upload_file_path, "a")
fp.write("{")

dirs = os.listdir(label_dir_path)
file_num=1
for file in dirs:
    
    if file_num!=1:
        fp.write(", ")
    file_num+=1

    image_name = file.split(".")[0] + ".jpg"
    fp.write(f"\"{image_name}\": [")
    print(image_name)

    img = cv2.imread(image_file_path)
    img_h, img_w, _ = img.shape # 942, 1716

    full_file_path = os.path.join(label_dir_path, file)
    print(full_file_path)
    with open(full_file_path) as f:
        
        line_num=1
        lines = f.readlines()
        
        for line in lines:
            if line_num!=1:
                fp.write(", ")
            line_num+=1
            
            items = line.split()

            x, y, w, h = float(items[1]), float(items[2]), float(items[3]), float(items[4])
            x_min, y_min = (x-w/2)*img_w, (y-h/2)*img_h
            x_max, y_max = (x+w/2)*img_w, (y+h/2)*img_h
            score = np.around(float(items[5]), decimals=5)

            x_min, y_min, x_max, y_max = int(np.around(x_min)), int(np.around(y_min)), int(np.around(x_max)), int(np.around(y_max))
            fp.write(f"[{x_min}, {y_min}, {x_max}, {y_max}, {score}]")
        
    fp.write("]")


fp.write("}")

fp.close()