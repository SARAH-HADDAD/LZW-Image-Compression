import argparse
import os
import pickle
import cv2
from PIL import Image
import numpy as np


DICTIONARY_SIZE = 256
#Transformer ces deux codes pour leur permettre de compresser et décompresser une
#image (noir et blanc).

def compress(input,bits):
    #print(type(input)) le type de input est byte
    global DICTIONARY_SIZE
    DICTIONARY_SIZE=2**bits
    dictionary = {}
    result = []
    temp = ""

    for i in range(0, DICTIONARY_SIZE):
        #str(i).zfill(3)
        dictionary[str(i)] = i
    
    #print(dictionary)
    #Lecture du caractère suivant:
    for c in input:# le type de c est int
        #temp howa w
        #temp2 howa k le caractère suivant 
        temp2 = temp+str(c)
        if temp2 in dictionary.keys(): #if wk fi Dictionary
            temp = temp2 #w = wk
        else:
            #Production du code en sortie:
            result.append(dictionary[temp]) #output (code (w))
            dictionary[temp2] = DICTIONARY_SIZE #Dictionary <- wk
            DICTIONARY_SIZE+=1
            #Mise à jour de la sous chaine temporaire (w):
            temp = ""+str(c) #w=k

    if temp != "":
        result.append(dictionary[temp])  
    print(result)    
    return result

def decompress(input,bits):
    #print(type(input)) le type de input est une liste
    global DICTIONARY_SIZE
    DICTIONARY_SIZE=2**bits
    dictionary = {}
    result = []

    #padding pour les valeurs avec 2 chifres ou 1
    for i in range(0, DICTIONARY_SIZE):
        dictionary[i] = str(i)

    # Read k: 
    # Lecture du code k suivant  
    previous = str(input[0])
    input = input[1:] 
    result.append(previous) # Output Dict[k]
    
    # While ( read k )
    for bit in input:
        aux = ""
        if bit in dictionary.keys():
            aux = dictionary[bit]
        else:
            aux = previous+previous[0] 

            #Bit is not in the dictionary
                 # Get the last character printed + the first position of the last character printed
                 #because we must decode bits that are not present in the dictionary, so we have to guess what it represents, for example:
                 #let's say bit 37768 is not in the dictionary, so we get the last character printed, for example it was 'uh'
                 #and we take it 'uh' plus its first position 'u', resulting in 'uhu', which is the representation of bit 37768
                 #the only case where this can happen is if the substring starts and ends with the same character ("uhuhu").

        # Output Dict[k]:   
        # Production du décodage en sortie:                  
        result.append(aux)
        # Insertion dans le dictionnaire de la sous chaine (w+décodage(k)[0]):
        # Add w Dict[k][0] to dictionary:
        dictionary[DICTIONARY_SIZE] = previous + aux[0]
        DICTIONARY_SIZE+= 1
        #w = Dict[k]
        #Mise à jour de la sous chaine temporaire (w):        
        previous = aux
    return result

def toImage(ListImage,width,height):
    print("List Image:")
    print(ListImage)
    StrImage=''.join(map(str,ListImage))
    print("Str Image:")
    print(StrImage)
    list = []
    list[:0] = StrImage
    print("Liste:")
    print(list)
    for i in range(len(list)): 
        if list[i]=='1':
            list[i]=255
        else: list[i]=0   
    # Convert the pixels into an array using numpy      
    array=np.array(list, dtype=np.uint8)
    array = np.reshape(array, (width,height))
    # Use PIL to create an image from the new array of pixels
    new_image = Image.fromarray(array)
    new_image.save('decompressed.png')





img_gray = cv2.imread('Image.png', cv2.IMREAD_GRAYSCALE)
width,height = img_gray.shape
# Applatir l'image
string_image = img_gray .flatten().tolist()
for i in range(len(string_image)): 
    if string_image[i]==255:
        string_image[i]=1
print(string_image)
print(type(string_image))
bits=1
result=compress(string_image,bits)
ListImage=decompress(result,bits)
toImage(ListImage,width,height)

#The second argument is the threshold value which is used to classify the pixel values
#The third argument is the maximum value which is assigned to pixel values exceeding the threshold
#_, img_bw = cv2.threshold(img_gray, 100, 255, cv2.THRESH_BINARY)
#cv2.imwrite('newImage.png', img_bw)
#height, width = img_bw.shape # 787x444 = 349428
#print(type(img_bw))#numpy.ndarray
#print(img_bw)
#print(img_bw.tobytes())



           