import zipfile
from zipfile import ZipFile

from PIL import Image, ImageDraw
import pytesseract
import cv2 as cv
import numpy as np
from IPython.display import display

face_cascade = cv.CascadeClassifier('readonly/haarcascade_frontalface_default.xml')

def search_name(file_name, search_name): # takes in the name of image
    print("---- converting image to text -----")
    text = pytesseract.image_to_string(file_name) # convert to text
    print("----- Done! ------")
    print("----- Look to see if the search_name is in the text ------")
    if search_name in text:
        string = "Results found in file {}".format(file_name)
        return ("T", string)
    else:
        return "F"
        
def open_zipfile(zipfilepath):
    zip_file_object = ZipFile(zipfilepath)
    images_name_list = zip_file_object.namelist()
    return images_name_list
    
def make_image_list(list_of_names, zipfilepath):  # takes in list of filenames, returns a list of image objects 
    processed_images_list = []
    zip_file_object = ZipFile(zipfilepath)
    for image in list_of_names:
        image_file = zip_file_object.open(image)
        image_png = Image.open(image_file)
        processed_images_list.append(image_png)
    return processed_images_list
    
# make sure that the image files have been saved in the same directory as this script
def convert_to_grey(image_name): # takes in name of the file (not file object) and converts i
    print("--- reading the image file and converting to cv image object---")
    image_cv = cv.imread(image_name)
    print("--- converting the image file to greyscale ---")
    gray = cv.cvtColor(image_cv, cv.COLOR_BGR2GRAY)
    print("--- Done! ---")
    return gray
    
def extract_faces(gray_image, image_name, scale = 1.35): # takes in gray image and the name of that image
    print("--- starting with a gray image ---")
    print("--- detecting the faces using face_cascade detectMultiScale and making faces variable--- ")
    faces = face_cascade.detectMultiScale(gray_image, scale)
    # open the original image
    print("--- making new image object ---")
    pil_img=Image.open(image_name)
    list_faces = [] # initialize the list to collect the faces
    print("--- iterating over the dimensions in the faces ---")
    for x,y,w,h in faces:
        # crops the faces
        print("--- crop the faces ---")
        pil_img2 = pil_img.crop((x,y,x+w,y+h)) 
        # make each face into thumbnail size
        print("--- makes the faces into thumbnail size ---")
        pil_img2.thumbnail((100, 100))
        # add each cropped face to the list
        print("--- add the faces to the list ---")
        list_faces.append(pil_img2) 
    return list_faces
    
def put_contactsheet(faces_list):
    first_image = faces_list[0]
    # create a new image for contact sheet
    contact_sheet = Image.new(first_image.mode, (first_image.width*5,first_image.height*2))
    x = 0
    y = 0
    for img in faces_list:
        contact_sheet.paste(img, (x, y))
        if x+first_image.width == contact_sheet.width:
            x=0
            y=y+first_image.height
        else:
            x=x+first_image.width
    return contact_sheet


############

file_names_list = open_zipfile('readonly/small_img.zip')

image_object_list = make_image_list(file_names_list, 'readonly/small_img.zip')

# save the images in the same directory for cvs to access
zip_file_object = ZipFile('readonly/small_img.zip')

for image in file_names_list:
    image_file = zip_file_object.open(image)
    image_png = Image.open(image_file)
    image_png.save(image)
    
dictionary = {}

for filename in file_names_list:
    print("---- starting a file ----")
    print("---- use search_name function to evaluate ----")
    tuple_file = search_name(filename, "Christopher")
    if tuple_file[0] == "T":
        print("----- it has the name in the text ----")
        dictionary[filename] = ["T"]
    else:
        print("----- it does not have the name in the text ----")
        dictionary[filename] = ["F"]
print(dictionary)


for file in dictionary.keys():
    if dictionary[file][0] == "T":
        print("--- it has the name ---")
        print("--- creating grey image ----")
        grey_image = convert_to_grey(file)
        print("--- identifying and extracting cropped faces from the grey image ---")
        cropped_faces = extract_faces(grey_image, file, 1.45)
        print("--- appending grey image to the list in the dictionary --- ")
        dictionary[file].append(grey_image)
        print("--- appending cropped faces object to the list in the dictionary ---")
        dictionary[file].append(cropped_faces)
        dictionary[file].append(len(cropped_faces))
print(dictionary)

for file in dictionary.keys():
    if dictionary[file][0] == "T" and dictionary[file][3]>0:
        string = "Results found in file {}".format(file)
        print(string)
        display(put_contactsheet(dictionary[file][2]))
    elif dictionary[file][0] == "T" and dictionary[file][3]==0:
        string = "Results found in file {}".format(file)
        print(string)
        print("But there were no faces in that file!")
        
 
#############
file_names_list = open_zipfile('readonly/images.zip')

image_object_list = make_image_list(file_names_list, 'readonly/images.zip')

zip_file_object = ZipFile('readonly/images.zip')

for image in file_names_list:
    image_file = zip_file_object.open(image)
    image_png = Image.open(image_file)
    image_png.save(image)
    
dictionary = {}

for filename in file_names_list:
    print("---- starting a file ----")
    print("---- use search_name function to evaluate ----")
    tuple_file = search_name(filename, "Mark")
    if tuple_file[0] == "T":
        print("----- it has the name in the text ----")
        dictionary[filename] = ["T"]
    else:
        print("----- it does not have the name in the text ----")
        dictionary[filename] = ["F"]
print(dictionary)

for file in dictionary.keys():
    if dictionary[file][0] == "T":
        print("--- it has the name ---")
        print("--- creating grey image ----")
        grey_image = convert_to_grey(file)
        print("--- identifying and extracting cropped faces from the grey image ---")
        cropped_faces = extract_faces(grey_image, file, 1.45)
        print("--- appending grey image to the list in the dictionary --- ")
        dictionary[file].append(grey_image)
        print("--- appending cropped faces object to the list in the dictionary ---")
        dictionary[file].append(cropped_faces)
        dictionary[file].append(len(cropped_faces))
print(dictionary)

for file in dictionary.keys():
    if dictionary[file][0] == "T" and dictionary[file][3]>0:
        string = "Results found in file {}".format(file)
        print(string)
        display(put_contactsheet(dictionary[file][2]))
    elif dictionary[file][0] == "T" and dictionary[file][3]==0:
        string = "Results found in file {}".format(file)
        print(string)
        print("But there were no faces in that file!")


