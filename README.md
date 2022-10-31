# LZW Text Compressor and Decompressor
[![GitHub license](https://img.shields.io/github/license/amycardoso/LZW-Text-File-Compression)](https://github.com/amycardoso/LZW-Text-File-Compression/blob/master/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/amycardoso/LZW-Text-File-Compression)](https://github.com/amycardoso/LZW-Text-File-Compression/stargazers)

The main objective of this project is to put into practice the theoretical concepts approached in the classroom related to media coding techniques. For this, a compressor and a decompressor of text were developed using the Lempel-Ziv-Welch (LZW) algorithm with fixed dictionary size. 
Data entry is a TXT document whose output is a binary file containing the compressed data.

### Requirements
* Python 3

### Usage

The compressor operates by command-line, accepting as parameter the name and path of the original TXT file, as well as the name and path of the binary file to be generated. The decompressor will also be command-line operated, accepting both parameters as well (binary input file and output TXT file). The following execution format must be obeyed: 

For compression:

```
$ python3 lzw.py compress -i original_file.txt -o binary_file.bin

```
For decompression:
```
$ python3 lzw.py decompress -i binary_file.bin -o uncompressed_file.txt

```
For help:
```
$ python3 lzw.py -h

```

#LZW Compression

LZW, which is short for, Lempel-Ziv-Welch coding, is an image compression technique. It assign fixed length code words to variable length sequences of source symbols, rather than individual source symbols. Unlike other techniques like Huffman coding, this method requires no prior knowledge of the probability of occurrence of the symbols to be encoded.

The codebook or dictionary containing the source symbols to be coded is constructed. For 8-bit monochrome images, the first 256 words of the dictionary are assigned to intensities 0,1,2, .. 255. As the encoder sequentially examines image pixels, intensity sequences that are not in the dictionary are placed in algorithmically determined (next unused locations). Ex: if the first two pixels of the image are white, i.e. the sequence "255-255", this is assigned to location 256, the next unused location. The next time two consecutive white pixels are encountered, code word 256, the address of the location containing the sequence "255-255" is used to represent then. Thus, we see that, originally, two consecutive white pixels were represented by 16 bits (8+8), but now just by 9 bits for representing the number 256.
