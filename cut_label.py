##不考慮被割成兩塊的STAS

import re
import os

def write_ob(fp, xmin, ymin, xmax, ymax):
    fp.write("	<object>\n		<name>stas</name>\n		<pose>unspecified</pose>\n		<truncated>0</truncated>\n		<difficult>0</difficult>\n")
    fp.write("		<bndbox>\n")
    fp.write("			<xmin>"+str(xmin)+"</xmin>\n")
    fp.write("			<ymin>"+str(ymin)+"</ymin>\n")
    fp.write("			<xmax>"+str(xmax)+"</xmax>\n")
    fp.write("			<ymax>"+str(ymax)+"</ymax>\n")
    fp.write("		</bndbox>\n	</object>\n")



file_i = 0
# annotation_dir = './OBJ_Train_Datasets/Train_Annotations/'
# saving_dir = './Cut_Train_Datasets/Train_Annotations/'

annotation_dir = './datasets_origin/valid/lables/'
saving_dir = './datasets_cut/valid/lables/'
saving_i = 0



# for file_i in range(1053): #1053
#     path = annotation_dir + str(file_i).zfill(8) + '.xml'
#     with open(path) as f:
dirs = os.listdir(annotation_dir)
for file in dirs:
    path = annotation_dir+file
    with open(path) as f:
        start_saving_i = saving_i
        lines = f.readlines()
        for i in range(6):
            #saving_path = saving_dir + str(saving_i).zfill(8)+'.xml'
            saving_path = saving_dir + file.split(".")[0] + '_' +str(i)+'.xml'
            fp = open(saving_path, "w")
            fp.write("<?xml version='1.0' encoding='UTF-8'?>\n")
            fp.write("<annotation>\n")
            fp.write("	<folder />\n")
            fp.write("	<filename />\n")
            fp.write("	<path />\n")
            fp.write("	<source>\n")
            fp.write("		<database>unknown</database>\n")
            fp.write("	</source>\n")
            fp.write("	<size>\n")
            fp.write("		<width>572</width>\n")
            fp.write("		<height>471</height>\n")
            fp.write("		<depth>3</depth>\n")
            fp.write("	</size>\n")
            fp.write("	<segmented>0</segmented>\n")
            fp.close()
 
            saving_i = saving_i + 1
        
        for j in range(len(lines)): #read in file
            line = lines[j]
            #print(line)
            regex = re.compile(r'<xmin>')
            match = regex.search(line)
            if( match != None): #object!!
                xmin = 0
                ymin = 0
                xmax = 0
                ymax = 0
                for k in range(4): #get (xmin, ymin, xmax, ymax)
                    regex = re.compile(r'(\d+)')
                    match = regex.search(lines[j])
                    if(k==0): xmin = match[0]
                    elif(k==1): ymin =  match[0]
                    elif(k==2): xmax = match[0]
                    else: ymax =  match[0]
                    j = j+1
                #print(xmin, ymin, xmax, ymax)
                xmin = int(xmin)
                ymin = int(ymin)
                xmax = int(xmax)
                ymax = int(ymax)
                if( xmin < 572 and ymin < 471 and xmax < 572 and ymax < 471): #1
                    fp = open(saving_dir + file.split(".")[0] + '_' +str(0)+'.xml', "a")
                    write_ob(fp, xmin, ymin, xmax, ymax)
                elif( xmin>=572 and xmin < 1144 and ymin < 471 and xmax>=572 and xmax < 1144 and ymax < 471): #2
                    fp = open(saving_dir + file.split(".")[0] + '_' +str(1)+'.xml', "a")
                    write_ob(fp, xmin-572, ymin, xmax-572, ymax)
                elif( xmin>=1144 and xmin < 1716 and ymin < 471 and xmax>=1144 and xmax < 1716 and ymax < 471): #3
                    fp = open(saving_dir + file.split(".")[0] + '_' +str(2)+'.xml', "a")
                    write_ob(fp, xmin-1144, ymin, xmax-1144, ymax)
                elif( xmin < 572 and ymin>=471 and ymin < 942 and xmax < 572 and ymax >= 471 and ymax < 942): #4
                    fp = open(saving_dir + file.split(".")[0] + '_' +str(3)+'.xml', "a")
                    write_ob(fp, xmin, ymin-471, xmax, ymax-471)
                elif( xmin>=572 and xmin < 1144 and ymin>=471 and ymin < 942 and xmax>=572 and xmax < 1144 and ymax >= 471 and ymax < 942): #5
                    fp = open(saving_dir + file.split(".")[0] + '_' +str(4)+'.xml', "a")
                    write_ob(fp, xmin-572, ymin-471, xmax-572, ymax-471)
                elif( xmin>=1144 and xmin < 1716 and ymin>=471 and ymin < 942 and xmax>=1144 and xmax < 1716 and ymax >= 471 and ymax < 942): #6
                    fp = open(saving_dir + file.split(".")[0] + '_' +str(5)+'.xml', "a")
                    write_ob(fp, xmin-1144, ymin-471, xmax-1144, ymax-471)
                ##elif( xmin < 572 and ymin < 471 and xmax <=572 and xmax < 1144 and ymax <471): # 1,2


                
        
        for i in range(6):
            saving_path = saving_dir + file.split(".")[0] + '_' +str(i)+'.xml'
            fp = open(saving_path, "a")
            fp.write("</annotation>")
            fp.close() 
                #print()
          

        #print(lines[0], file_i)
