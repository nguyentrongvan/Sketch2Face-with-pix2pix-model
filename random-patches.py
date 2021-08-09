from  augmentation import RandomPatches,getPosition
import cv2
import numpy as np
import argparse
import ast
import os
from glob import glob
from skimage.io import imread, imsave


def main(args):
    image_folder = args.inputDir
    save_folder = args.outputDir
        
    if not os.path.exists(save_folder):
        os.mkdir(save_folder)
        
    types = ('*.jpg','*.png')
        
    image_path_list= []
    for files in types:
        image_path_list.extend(glob(os.path.join(image_folder, files)))
    total_num = len(image_path_list)

    count=1
    for i, image_path in enumerate(image_path_list):
        name = image_path.strip().split('/')[-1][:-4]
        print('Image {}/{} is processing...'.format(count,total_num))
        print('=========================================================')
        count_new=0
        for c in range(args.numNew):
            x_visited=[]
            y_visited=[]

            x=[]
            y=[]
            for i in range(12):
                x_t,y_t=getPosition(256,256,16,16)
                x.append(x_t)
                y.append(y_t)

            while (x in x_visited) and (y in y_visited):
                x=[]
                y=[]
                for i in range(12):
                    x_t,y_t=getPosition(height,width,16,16)
                    x.append(x_t)
                    y.append(y_t)

            x_visited.append(x)
            y_visited.append(y)
            count_new+=1

  
            image=cv2.imread(image_path)
            #image=cv2.resize(image,(256,256))
            height=int(image.shape[0])
            width=int(image.shape[1])
                
            ag_frame=image.copy()
            for i in range(len(x)):
                ag_frame=RandomPatches(ag_frame,(16,16),(x[i],y[i]),0)
                
            imsave(os.path.join(save_folder, name +'aug'+str(c+1)+ '.jpg'),ag_frame[...,::-1])
        
        count+=1
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Joint 3D Face Reconstruction and Dense Alignment with Position Map Regression Network')
	parser.add_argument('-i', '--inputDir', default='TestImages/', type=str,
                        help='path to the input directory, where input images are stored.')
	parser.add_argument('-o', '--outputDir', default='TestImages/results', type=str,
                        help='path to the output directory, where results(obj,txt files) will be stored.')
	parser.add_argument('--numNew', default=3, type=int,
                        help='number of new image after augmentation.')
	main(parser.parse_args())

