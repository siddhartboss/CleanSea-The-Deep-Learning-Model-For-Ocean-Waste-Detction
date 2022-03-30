# Importing all necessary libraries 

import cv2 

import os 

import tkinter as tk

from tkinter import filedialog

  
# Read the video from specified path 

file_path = filedialog.askopenfilename()

print(file_path)

cam = cv2.VideoCapture(file_path) 

  

try: 

      

    # creating a folder named data 

    if not os.path.exists('data'): 

        os.makedirs('data') 

  
# if not created then raise error 

except OSError: 

    print ('Error: Creating directory of data') 

  
# frame 

currentframe = 0
count = 0
  

while(True): 

      

    # reading from frame 

    ret,frame = cam.read() 

  
    if count <=100 :
        if ret: 

            # if video is still left continue creating images 

            name = './data/frame' + str(currentframe) + '.jpg'

            print ('Creating...' + name) 

  

            # writing the extracted images 

            cv2.imwrite(name, frame) 

  

            # increasing counter so that it will 

            # show how many frames are created 

            currentframe += 1
            count +=1

        else: 

            break
    else :
        break
  
# Release all space and windows once done 
cam.release() 
cv2.destroyAllWindows()

import tensorflow as tf
import sys
import os
import matplotlib.pyplot as plt

# Disable tensorflow compilation warnings
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import tensorflow as tf
import tensorboard as tb
tf.io.gfile = tb.compat.tensorflow_stub.io.gfile
def analyse(imageObj):
    # Read the image_data
    image_data = tf.io.gfile.GFile(imageObj, 'rb').read()

    # Loads label file, strips off carriage return
    #label_lines = [line.rstrip() for line in tf.io.gfile.GFile("tf_files/retrained_labels.txt")]
    label_lines = ['cardboard','glass','metal','paper','plastic','trash']

    # Unpersists graph from file
    with tf.io.gfile.GFile("tf_files/retrained_graph.pb", 'rb') as f:
        graph_def = tf.compat.v1.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    with tf.compat.v1.Session() as sess:
        # Feed the image_data as input to the graph and get first prediction
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
        
        predictions = sess.run(softmax_tensor, \
                    {'DecodeJpeg/contents:0': image_data})
        
        # Sort to show labels of first prediction in order of confidence
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
        obj = {}
        for node_id in top_k:
            human_string = label_lines[node_id]
            score = predictions[0][node_id]
            obj[human_string] = float(score)
        
        return obj

import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

#file_path = []
keyList = ["cardboard", "glass", "metal", "paper", "plastic", "trash"]
output = {}
for i in keyList:
    output[i] = 0.0

#for x in range(0,3):
file_path = filedialog.askopenfilenames()
n = float(len(file_path))
for x in file_path:
    result=analyse(x)
    for key in result:
        output[key]=output[key]+result[key]
for key in output:
        output[key]=output[key]/n
print(output)
names = list(output.keys())
values = list(output.values())

plt.bar(range(len(output)), values, tick_label=names)

fig = plt.figure(figsize =(10, 7))

#plt.pie(values, labels = names)
colors=['blue', 'yellow', 'green', 'orange' , 'indigo' , 'grey']
plt.pie(values,labels=names, colors=colors, startangle=90, shadow=True,explode=(0.1, 0.1, 0.1, 0.1, 0.1, 0.1), autopct='%1.2f%%')

plt.show()
#print(file_path)
