import os

import numpy as np
from PIL import Image

#---------------------------------------------------------#
#   将图像转换成RGB图像，防止灰度图在预测时报错。
#   代码仅仅支持RGB图像的预测，所有其它类型的图像都会转化成RGB
#---------------------------------------------------------#
def cvtColor(image):
    if len(np.shape(image)) == 3 and np.shape(image)[2] == 3:
        return image 
    else:
        image = image.convert('RGB')
        return image 
    
#---------------------------------------------------#
#   对输入图像进行resize
#---------------------------------------------------#
def resize_image(image, size, letterbox_image):
    iw, ih  = image.size
    w, h    = size
    if letterbox_image:
        scale   = min(w/iw, h/ih)
        nw      = int(iw*scale)
        nh      = int(ih*scale)

        image   = image.resize((nw,nh), Image.BICUBIC)
        new_image = Image.new('RGB', size, (128,128,128))
        new_image.paste(image, ((w-nw)//2, (h-nh)//2))
    else:
        new_image = image.resize((w, h), Image.BICUBIC)
    return new_image

#---------------------------------------------------#
#   获得类
#---------------------------------------------------#
def get_classes(classes_path):
    with open(classes_path, encoding='utf-8') as f:
        class_names = f.readlines()
    class_names = [c.strip() for c in class_names]
    return class_names, len(class_names)

#---------------------------------------------------#
#   获得先验框
#---------------------------------------------------#
def get_anchors(anchors_path):
    '''loads the anchors from a file'''
    with open(anchors_path, encoding='utf-8') as f:
        anchors = f.readline()
    anchors = [float(x) for x in anchors.split(',')]
    anchors = np.array(anchors).reshape(-1, 2)
    return anchors, len(anchors)

#---------------------------------------------------#
#   获得学习率
#---------------------------------------------------#
def get_lr(optimizer):
    for param_group in optimizer.param_groups:
        return param_group['lr']

def preprocess_input(image):
    image /= 255.0
    return image

def show_config(**kwargs):
    print('Configurations:')
    print('-' * 70)
    print('|%25s | %40s|' % ('keys', 'values'))
    print('-' * 70)
    for key, value in kwargs.items():
        print('|%25s | %40s|' % (str(key), str(value)))
    print('-' * 70)

#---------------------------------------------------#
#   写XML
#---------------------------------------------------#

def writeInXml(pic_number,predicted_classes,tops, lefts, bottoms, rights, xml_file):
    name = {
        'CD': '灰斑病',
        'Pp': '南方型锈病',
        'ML': '叶斑病',
        'Bt': '纹枯病',
        'CR': '普通锈病'
    }
    objs = []
    for i in range(len(tops)):
        objs.append(
        '\n\t<object>\n\t\t<name>' + predicted_classes[i] + '</name>\n\t\t<pose>Unspecified</pose>\n\t\t<truncated>0</truncated>' \
        '\n\t\t<difficult>0</difficult>\n\t\t<bndbox>\n\t\t\t<xmin>'+ str(lefts[i]) +'</xmin>\n\t\t\t<ymin>'+ str(tops[i]) +'</ymin>\n\t\t\t' \
        '<xmax>'+ str(rights[i]) +'</xmax>\n\t\t\t<ymax>'+ str(bottoms[i]) +'</ymax>\n\t\t</bndbox>\n\t</object>')
    objs = ''.join(objs)
    with open(xml_file + pic_number + '.txt', 'w') as f:
        f.write(
            '<annotation>\n\t<folder></folder>\n\t<filename>'+
            pic_number +'.jpg</filename>\n\t<path></path>\n\t<source>\n\t\t<database>Unknown</database>\n\t</source>\n\t<size>\n\t\t'
                        '<width>500</width>\n\t\t<height>800</height>\n\t\t<depth>3</depth>\n\t</size>\n\t<segmented>0</segmented>\n\t'+ objs +'</annotation>')



