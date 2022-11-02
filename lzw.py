import argparse
import os
import pickle
import cv2
from PIL import Image
import numpy as np

def compress(input):
    DICTIONARY_SIZE = 256
    PixelsInput=set(input)
    dictionary = {}
    result = []
    temp = ""

    for pixel in range(DICTIONARY_SIZE):
        # The zfill() method adds zeros (0) at the beginning of the string, until it reaches the specified length
        dictionary[str(pixel).zfill(3)] = pixel
    
    
    # Read the next pixel:
    for p in input:
        # We convert the pixels into str to concatenate them
        p=str(p).zfill(3) 
        # temp2 is the next pixel
        temp2 = temp+p
        if temp2 in dictionary: #if temp+p is in the Dictionary
            temp = temp2 #temp=temp+p
        else:
            # Production of output code:
            result.append(dictionary[temp]) #output (code (w))
            dictionary[temp2] = DICTIONARY_SIZE #Dictionary <- wk
            DICTIONARY_SIZE+=1
            # Update of the temporary sub string:
            temp = ""+p 

    if temp != "":
        result.append(dictionary[temp])  

    return result

def decompress(input,width,height):
    DICTIONARY_SIZE=256
    dictionary = {}
    result = []

    # Create a dictionary of all possible pixel values:
    # '000' -> '255'
    
    for pixel in range(256):
        dictionary[pixel] = str(pixel).zfill(3)

    # Read the first pixel coded:  
    previous = input[0]
    input = input[1:] 
    result.append(dictionary[previous])# Output Dict[k]
    
    for pixels in input:
        aux = ""

        #If the pixel is in the dictionary we decode its value:
        if pixels in dictionary:
            aux = dictionary[pixels]
        else:
            aux = str(previous).zfill(3)+str(previous[:3])
  
        # Production of the output decoding (Output Dict[k]):           
        result.append(aux)

        # Add previous Dict[aux][0] to dictionary:
        dictionary[DICTIONARY_SIZE] = str(previous)+ aux[:3]
        DICTIONARY_SIZE+= 1
        # previous = Dict[k]
        # Update of the temporary sub string:       
        previous = aux

    #transform a list (result) into an image  
    toImage(result,width,height)

    return result

def toImage(result,width,height):
    # Go through the decoded values and decompose them on 3 characters to convert them afterwards
    ListImage=[]
    for value in result:
        for i in range(0,len(value),3):
            ListImage.append(value[i:i+3])

    # Convert the values to int :       
    ListImage = [int(x) for x in ListImage]  

    # Convert the pixels into an array using numpy :  
    image = np.array(ListImage, dtype=np.uint8)
    image = np.reshape(image,(width,height))      

    # Use PIL to create an image from the new array of pixels :
    new_image = Image.fromarray(image)
    new_image.save('decompressed.png')



# Loading an image in grayscale mode:
# Using cv2.imread() method
# Using 0 to read image in grayscale mode
img = cv2.imread('test.png',0)

# Displaying the image:
cv2.imshow('image', img)

width,height = img.shape
# Flatten the image
input = img.flatten().tolist()

# Compression: 
result=compress(input)

# Decompression:
decompress(result,width,height)








           
