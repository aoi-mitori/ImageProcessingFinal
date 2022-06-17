from email.mime import image
import albumentations as A
import cv2
import numbers
import numpy as np
import os
import random

from skimage import color
from PIL import Image, ImageFilter


__all__ = ["Augment"]

class Augment(object):
    def __init__(self, args, img_name, img, bboxes, classes, img_dir_path, bbox_dir_path):
        self.args = args
        self.img_name = img_name
        self.img = img
        self.bboxes = bboxes
        self.classes = classes
        self.img_dir_path = img_dir_path
        self.bbox_dir_path = bbox_dir_path


    
    def save(self, nimg, nlabels, nclasses, file_postfix):
        nimg_name = self.img_name.split('.')[0] + file_postfix + '.' + self.img_name.split('.')[1]
        nlabel_name = self.img_name.split('.')[0] + file_postfix + '.txt'

        nimg_full_path = os.path.join(self.img_dir_path, nimg_name)
        nlabel_full_path = os.path.join(self.bbox_dir_path, nlabel_name)

        with open(nlabel_full_path, "a") as f:
            for index, item in enumerate(nlabels):
                print(nclasses[index])
                f.write(f"{nclasses[index]} {item[0]} {item[1]} {item[2]} {item[3]}\n")
        
        
        cv2.imwrite(nimg_full_path, nimg)
    


    def save_in_output_dir(self, nimg, nlabels, nclasses, file_postfix):
        nimg_name = self.img_name.split('.')[0] + file_postfix + '.' + self.img_name.split('.')[1]
        nlabel_name = self.img_name.split('.')[0] + file_postfix + '.txt'


        nimg_full_path = os.path.join(os.path.dirname(os.path.realpath('__file__')), "augment_output/images/"+nimg_name)
        nlabel_full_path = os.path.join(os.path.dirname(os.path.realpath('__file__')), "augment_output/labels/"+nlabel_name)

        with open(nlabel_full_path, "a") as f:
            for index, item in enumerate(nlabels):
                print(nclasses[index])
                f.write(f"{nclasses[index]} {item[0]} {item[1]} {item[2]} {item[3]}\n")

        cv2.imwrite(nimg_full_path, nimg)



    def __call__(self):

        if self.args.hedjitter:
            # HEDJitter
            hed_jitter = HEDJitter(theta=0.05)
            hed_jitter_img, hed_jitter_bboxes, hed_jitter_classes = hed_jitter(self.img, self.bboxes, self.classes)
        
        
            self.save_in_output_dir(nimg=hed_jitter_img, nlabels=hed_jitter_bboxes, nclasses=hed_jitter_classes, file_postfix='_HEDJitter')


        if self.args.gaussblur:
            gauss_blur = RandomGaussBlur(radius=[0.5, 1.5])
            blur_img, blur_bboxes, blur_classes = gauss_blur(self.img, self.bboxes, self.classes)

            self.save_in_output_dir(nimg=blur_img, nlabels=blur_bboxes, nclasses=blur_classes, file_postfix='_GaussBlur')



        if self.args.geomtransform:
            geom_transform = GeomTransform()
            geom_img, geom_bboxs, geom_classes = geom_transform(self.img, self.bboxes, self.classes)

            self.save_in_output_dir(nimg=geom_img, nlabels=geom_bboxs, nclasses=geom_classes, file_postfix='_GeomTransform')

    




class HEDJitter(object):
    def __init__(self, theta=0.):
        assert isinstance(theta, numbers.Number), "theta should be a single number."
        self.theta = theta
        self.alpha = np.random.uniform(1-theta, 1+theta, (1, 3))
        self.betti = np.random.uniform(-theta, theta, (1, 3))


    @staticmethod
    def adjust_HED(img, alpha, betti):
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        img = np.array(img)

        s = np.reshape(color.rgb2hed(img), (-1, 3))
        ns = alpha * s + betti
        nimg = color.hed2rgb(np.reshape(ns, img.shape))

        imin = nimg.min()
        imax = nimg.max()
        rsimg = (255 * (nimg - imin) / (imax - imin)).astype('uint8')

        rsimg = Image.fromarray(rsimg)
        rsimg = cv2.cvtColor(np.asarray(rsimg), cv2.COLOR_RGB2BGR)

        return rsimg


    
    def __call__(self, img, bboxes, classes):
        return self.adjust_HED(img, self.alpha, self.betti), bboxes, classes
        
    
    

class RandomGaussBlur(object):
    """Random GaussBlurring on image by radius parameter.
    Args:
        radius (list, tuple): radius range for selecting from; you'd better set it < 2
    """
    def __init__(self, radius=None):
        if radius is not None:
            assert isinstance(radius, (tuple, list)) and len(radius) == 2, \
                "radius should be a list or tuple and it must be of length 2."
            self.radius = random.uniform(radius[0], radius[1])
        else:
            self.radius = 0.0

    def __call__(self, img, bboxes, classes):
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        rsimg = img.filter(ImageFilter.GaussianBlur(radius=self.radius))
        rsimg = cv2.cvtColor(np.asarray(rsimg), cv2.COLOR_RGB2BGR)

        return rsimg, bboxes, classes

    


class GeomTransform(object):
    def __init__(self):
        self.transform = A.Compose([
            A.OneOf([
            A.Rotate(limit=[-90, 90], interpolation=2, p=1),
            A.Flip(p=1),
        ], p=1)
        ], bbox_params=A.BboxParams(format='yolo', min_visibility=0.9, label_fields=['classes']))

    def __call__(self, img, bboxes, classes):
        print(bboxes)
        transformed = self.transform(image=img, bboxes=bboxes, classes=classes)

        return transformed['image'], transformed['bboxes'], transformed['classes']

