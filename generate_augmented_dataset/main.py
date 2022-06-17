import argparse
import os
import sys
import cv2

from split_dataset import SplitDataset
from augmentation import Augment


def main():
    parser = argparse.ArgumentParser("Spilit datasets into three parts, train, validation, test. And Augment train datasets.")
    parser.add_argument("--img", help="Image datasets directory path.", default="Train_Images")
    parser.add_argument("--label", help="Label datasets (yolo format) directory path.", default="Train_Annotations_Yolo")
    parser.add_argument("--train_pro", help="Train datasets propogation", default=0.7)
    parser.add_argument("--val_pro", help="Validation datasets propogation", default=0.2)
    parser.add_argument("--test_pro", help="Test datasets propogation", default=0.1)
    parser.add_argument("--augment", action= "store_true", help="Image augmentation")
    parser.add_argument("--hedjitter", action="store_true", help="HEDJitter augmentation")
    parser.add_argument("--gaussblur", action="store_true", help="RandomGaussBlur augmentation")
    parser.add_argument("--geomtransform", action="store_true", help="GeometricTransform augmentation")
    args = parser.parse_args()

    img_dir_path = os.path.join(os.path.dirname(os.path.realpath('__file__')), args.img)
    if not os.path.exists(img_dir_path):
        print("Provide the correct folder for image datasets.")
        sys.exit()
    
    label_dir_path = os.path.join(os.path.dirname(os.path.realpath('__file__')), args.label)
    if not os.path.exists(label_dir_path):
        print("Provide the correct folder for label datasets.")

    
    # count number of datasets
    data_num = 0
    label_dir = os.listdir(label_dir_path)
    for f in label_dir:
        if f.lower().endswith('.txt'):
            data_num+=1
    

    # split datasets into train, validation, test parts
    splitDataset = SplitDataset(img_dir=img_dir_path, label_dir=label_dir_path)
    splitDataset.split(train_pro=args.train_pro, val_pro=args.val_pro, test_pro=args.test_pro, data_num=data_num)


    # image augmentation
    if args.augment:
        train_img_dir = os.path.join(os.path.dirname(os.path.realpath('__file__')), 'datasets/train/images')
        train_label_dir = os.path.join(os.path.dirname(os.path.realpath('__file__')), 'datasets/train/labels')

        train_img_dirs = os.listdir(train_img_dir)

        for img_f in train_img_dirs:
            img = cv2.imread(os.path.join(train_img_dir, img_f))
            label_f = img_f.split('.')[0] + '.txt'
            label_f = os.path.join(train_label_dir, label_f)

            bboxes_list = []
            classes_list = []

            with open(label_f) as f:
                lines = f.readlines()

                for line in lines:
                    items = line.split()
                    bbox_list = [float(items[1]), float(items[2]), float(items[3]), float(items[4])]
                    bboxes_list.append(bbox_list)
                    classes_list.append(int(items[0]))
            

            augment = Augment(args=args, img_name=img_f, img=img, bboxes=bboxes_list, classes=classes_list, img_dir_path=train_img_dir, bbox_dir_path=train_label_dir)
            augment()

            




if __name__ == "__main__":
    main()