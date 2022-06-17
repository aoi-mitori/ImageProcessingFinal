import random
import os
import shutil

class SplitDataset(object):
    def __init__(self, img_dir, label_dir):
        self.img_extention = '.jpg'
        self.img_dir = img_dir
        self.label_dir = label_dir
        self.datasets_dir = os.path.join(os.path.dirname(os.path.realpath('__file__')), 'datasets')
        self.train_dir = os.path.join(self.datasets_dir, 'train')
        self.val_dir = os.path.join(self.datasets_dir, 'valid')
        self.test_dir = os.path.join(self.datasets_dir, 'test')
        self.train_img_dir = os.path.join(self.train_dir, 'images')
        self.train_label_dir = os.path.join(self.train_dir, 'labels')
        self.val_img_dir = os.path.join(self.val_dir, 'images')
        self.val_label_dir = os.path.join(self.val_dir, 'labels')
        self.test_img_dir = os.path.join(self.test_dir, 'images')
        self.test_label_dir = os.path.join(self.test_dir, 'labels')
    

    def split(self, train_pro, val_pro, test_pro, data_num):
        if not os.path.exists(self.datasets_dir):
            os.makedirs(self.datasets_dir)
            os.makedirs(self.train_dir)
            os.makedirs(self.val_dir)
            os.makedirs(self.test_dir)
            os.makedirs(self.train_img_dir)
            os.makedirs(self.train_label_dir)
            os.makedirs(self.val_img_dir)
            os.makedirs(self.val_label_dir)
            os.makedirs(self.test_img_dir)
            os.makedirs(self.test_label_dir)
        
        
        random_list = random.sample(range(data_num), data_num)

        train_start_item = 0
        val_start_item = round(data_num * train_pro)
        test_start_item = val_start_item + round(data_num * val_pro)



        label_dirs = os.listdir(self.label_dir)
        
        for i in range(train_start_item, val_start_item):
            img_file = label_dirs[random_list[i]].split('.')[0] + self.img_extention
            label_file = label_dirs[random_list[i]]
            shutil.move(os.path.join(self.img_dir, img_file), os.path.join(self.train_img_dir, img_file))
            shutil.move(os.path.join(self.label_dir, label_file), os.path.join(self.train_label_dir, label_file))

        for i in range(val_start_item, test_start_item):
            img_file = label_dirs[random_list[i]].split('.')[0] + self.img_extention
            label_file = label_dirs[random_list[i]]
            shutil.move(os.path.join(self.img_dir, img_file), os.path.join(self.val_img_dir, img_file))
            shutil.move(os.path.join(self.label_dir, label_file), os.path.join(self.val_label_dir, label_file))
        
        for i in range(test_start_item, data_num):
            img_file = label_dirs[random_list[i]].split('.')[0] + self.img_extention
            label_file = label_dirs[random_list[i]]
            shutil.move(os.path.join(self.img_dir, img_file), os.path.join(self.test_img_dir, img_file))
            shutil.move(os.path.join(self.label_dir, label_file), os.path.join(self.test_label_dir, label_file))

    

    