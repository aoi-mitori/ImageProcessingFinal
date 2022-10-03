import cv2
import os
# img_dir = './OBJ_Train_Datasets/Train_Images/'
# img_save_dir = './Cut_Train_Datasets/Train_Images/'

img_dir = './datasets_origin/valid/images/'
img_save_dir = './datasets_cut/valid/images/'


# img_dir = './Public_Image/'
# img_save_dir = './Public_Cut_Img/'
dirs = os.listdir(img_dir)
for file in dirs:
    #print(file)
    img = cv2.imread(img_dir + file)
    cut_img_1 = img[0:471, 0:572]
    cut_img_2 = img[0:471, 572:1144]
    cut_img_3 = img[0:471, 1144:1716]
    cut_img_4 = img[471:942, 0:572]
    cut_img_5 = img[471:942, 572:1144]
    cut_img_6 = img[471:942, 1144:1716]
    ii = 0
    cv2.imwrite(img_save_dir+file.split(".")[0]+'_'+str(ii)+'.jpg', cut_img_1)
    ii = ii+1
    cv2.imwrite(img_save_dir+file.split(".")[0]+'_'+str(ii)+'.jpg', cut_img_2)
    ii = ii+1
    cv2.imwrite(img_save_dir+file.split(".")[0]+'_'+str(ii)+'.jpg', cut_img_3)
    ii = ii+1
    cv2.imwrite(img_save_dir+file.split(".")[0]+'_'+str(ii)+'.jpg', cut_img_4)
    ii = ii+1
    cv2.imwrite(img_save_dir+file.split(".")[0]+'_'+str(ii)+'.jpg', cut_img_5)
    ii = ii+1
    cv2.imwrite(img_save_dir+file.split(".")[0]+'_'+str(ii)+'.jpg', cut_img_6)
    ii = ii+1


 

# ii = 0
# for i in range(1053):
# #for i in range(131):
#     #image_file_path = img_dir + str(i).zfill(8) + '.jpg'
#     image_file_path = img_dir +str(i).zfill(8) + '.jpg'
#     #print(image_file_path)
#     img = cv2.imread(image_file_path)
#     cut_img_1 = img[0:471, 0:572]
#     cut_img_2 = img[0:471, 572:1144]
#     cut_img_3 = img[0:471, 1144:1716]
#     cut_img_4 = img[471:942, 0:572]
#     cut_img_5 = img[471:942, 572:1144]
#     cut_img_6 = img[471:942, 1144:1716]

    
#     cv2.imwrite(img_save_dir+str(ii).zfill(8)+'.jpg', cut_img_1)
#     ii = ii+1
#     cv2.imwrite(img_save_dir+str(ii).zfill(8)+'.jpg', cut_img_2)
#     ii = ii+1
#     cv2.imwrite(img_save_dir+str(ii).zfill(8)+'.jpg', cut_img_3)
#     ii = ii+1
#     cv2.imwrite(img_save_dir+str(ii).zfill(8)+'.jpg', cut_img_4)
#     ii = ii+1
#     cv2.imwrite(img_save_dir+str(ii).zfill(8)+'.jpg', cut_img_5)
#     ii = ii+1
#     cv2.imwrite(img_save_dir+str(ii).zfill(8)+'.jpg', cut_img_6)
#     ii = ii+1


