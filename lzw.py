import argparse
import os
import pickle

DICTIONARY_SIZE = 256

def compress(input):
    #print(type(input)) le type de input est byte
    global DICTIONARY_SIZE
    dictionary = {}
    result = []
    temp = ""

    for i in range(0, DICTIONARY_SIZE):
        dictionary[str(chr(i))] = i

    #Lecture du caractère suivant:
    for c in input:# le type de c est int
        #temp howa w
        #temp2 howa k le caractère suivant 
        temp2 = temp+str(chr(c))
        if temp2 in dictionary.keys(): #if wk fi Dictionary
            temp = temp2 #w = wk
        else:
            #Production du code en sortie:
            result.append(dictionary[temp]) #output (code (w))
            dictionary[temp2] = DICTIONARY_SIZE #Dictionary <- wk
            DICTIONARY_SIZE+=1
            #Mise à jour de la sous chaine temporaire (w):
            temp = ""+str(chr(c)) #w=k

    if temp != "":
        result.append(dictionary[temp])  
        
    return result

def decompress(input):
    #print(type(input)) le type de input est une liste
    global DICTIONARY_SIZE
    dictionary = {}
    result = []

    for i in range(0, DICTIONARY_SIZE):
        dictionary[i] = str(chr(i))

    # Read k: 
    # Lecture du code k suivant  
    previous = chr(input[0])
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

parser = argparse.ArgumentParser(description = 'Text compressor and decompressor.')
parser.add_argument('action', choices={"compress", "decompress"}, help="Define action to be performed.")
parser.add_argument('-i', action = 'store', dest = 'input', required = True,
                           help = 'Input file.')
parser.add_argument('-o', action = 'store', dest = 'output', required = True,
                           help = 'Output file.')
arguments = parser.parse_args()

ABSOLUTE_PATH = os.getcwd()

if arguments.action == 'compress':
    input = open(ABSOLUTE_PATH+"//"+arguments.input, "rb").read()
    output = open(ABSOLUTE_PATH+"//"+arguments.output, "wb")

    compressedFile = compress(input)
    pickle.dump(compressedFile, output)
else:
    input = pickle.load(open(ABSOLUTE_PATH+"//"+arguments.input, "rb"))
    output = open(ABSOLUTE_PATH+"//"+arguments.output, "w")
    
    uncompressedFile = decompress(input)
    for l in uncompressedFile:
            output.write(l)
    output.close()
           