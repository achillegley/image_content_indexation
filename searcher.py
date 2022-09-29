from lshash.lshash import LSHash
import pickle
import cv2 as cv
import os
import base64

def save_image(name,content):
    imgdata = base64.b64decode(content)
    with open(name, 'wb') as f:
        f.write(imgdata)
#chargement du lshash
def getLsh():
    with open("models/lsh.pickle", "rb") as file:
        lsh = pickle.load(file)
    return lsh

lsh=getLsh()



#conversion en gray

#fonction de conversion d'image en gray
def convert_to_gray(train_images):
  train_gray_images={}
  for key in train_images:
    train_gray_images[key]=cv.cvtColor(train_images[key], cv.COLOR_RGB2GRAY)
  return train_gray_images

#test_gray_images=convert_to_gray(test_images)
#calcul de descripteur
def describeImages(train_gray_images,train_images):
    sift = cv.SIFT_create(150)
    descriptors= {}
    keypoints={}
    for key in train_gray_images:
        current_kp, current_des = sift.detectAndCompute(train_gray_images[key],None)
        descriptors[key]=current_des;
        keypoints[key]=current_kp;
    return descriptors, keypoints

def requetter_document(req_descriptors):
  results={}
  for vector in req_descriptors:
    nn = lsh.query(vector, num_results=1, distance_func="euclidean")
    for ((vec,extra_data),distance) in nn:
        #current_result=(extra_data.split('.')[0]).split('__')[0]
        current_result=extra_data
        if current_result in results:
          results[current_result]+=1
        else:
          results[current_result]=1
  return results

#fonction de tri
def get_sorted_results(results):
  sorted_similiraties_values = sorted(results.values(), reverse=True)
  sorted_results = {}
  i=0
  for i in sorted_similiraties_values:
      for k in results.keys():
          if results[k] == i:
              sorted_results[k] = results[k]
      if len(sorted_results.keys())>=10:
          break
  return sorted_results

#final function
def final_searcher(name,content):
    frame={}
    gray_frame={}
    results={}
    save_image(name,content)
    if os.path.exists(name):
        frame[name]=cv.imread(name)
        gray_frame=convert_to_gray(frame)
        frame_descriptors,_=describeImages(gray_frame,frame)
        results=requetter_document(frame_descriptors[name])
        results=get_sorted_results(results)
    os.remove(name)
    return results

def true_final_search(name):
    name="uploads/"+str(name)
    frame = {}
    gray_frame = {}
    results = {}
    if os.path.exists(name):
        frame[name]=cv.imread(name)
        gray_frame=convert_to_gray(frame)
        frame_descriptors,_=describeImages(gray_frame,frame)
        results=requetter_document(frame_descriptors[name])
        results=get_sorted_results(results)
    os.remove(name)
    return results