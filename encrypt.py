import numpy as np
#from IPython.display import Image, display
import cv2 as cv
import os

def get_image(file_name):
    path = 'static/uploaded_images/'
    img = cv.imread(os.path.join(path, file_name))
    # print(img)
    # img = img.astype(np.uint8)
    # cv.imshow('lamp', img)
    # cv.waitKey(0)

    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # cv.imshow('lamp', img)
    # cv.waitKey(0)

    img=cv.resize(img,(256,256))
    # cv.imshow('lamp', img)
    # cv.waitKey(0)
    #print('\n',img.shape)
    return img

# Image Encryption key
def get_array_key(number):
    np.random.seed(1)
    
    # Creating a array of 256 length by repeating the 16 digit key
    arr = []
    for i in number:
        arr.append(ord(i)-48)
    # arr = [1, 2, 3, 5, 6, 8, 5, 4, 2, 9, 8, 2, 1, 5, 6, 7]
    for _ in range(4):
        arr = arr + arr

    # Round Key generation from range 0-256
    array_key=np.random.randint(27,size=(256,256))
    for i in range(256):
        x = array_key[i]
        array_key[i] = [arr[j] * x[j] for j in range(256)]
    # print(array_key)

    return array_key


# Substitute Byte Transformation
def sub_byte_transform(img):
    sbox = [
            0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
            0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
            0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
            0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
            0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
            0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
            0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
            0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
            0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
            0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
            0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
            0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
            0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
            0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
            0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
            0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
            ]
    
    # Coverting int image matrix to hex
    vhex = np.vectorize(hex)
    img_hex = vhex(img)
    # print(img_hex)

    # Substitute byte transformation
    img_sbt=np.zeros((256,256),int)
    for i in range(256):
        for j in range(256):
            k=int(img_hex[i][j],0)
            img_sbt[i][j]=sbox[k]
    return img_sbt


# Shift Rows Transformation
def shift_row_transform(img_sbt):
    img_srt=np.zeros((256,256),int)

    # Converting array to lists so that to lists can be added using '+' sign
    img_sbt=img_sbt.tolist()

    #  Shift rows transformation
    for i in range(256):
        img_srt[i]=img_sbt[i][i:]+img_sbt[i][0:i]
    
    return img_srt


# Galois Multiplication
def galoisMult(a, b):
    p = 0
    hiBitSet = 0
    for i in range(8):
        if b & 1 == 1:
            p ^= a
        hiBitSet = a & 0x80
        a <<= 1
        if hiBitSet == 0x80:
            a ^= 0x1b
        b >>= 1
    return p % 256


# Mix Columns Transformation
def mix_col_transform(img_srt):
    img_mct=np.zeros((256,256),int)
    temp=[0]*4

    # Applying the transformation on columns of size (4,1) at a time
    for i in range(0,256,4):
        for j in range(256):
            temp[0]=img_srt[i][j]
            temp[1]=img_srt[i+1][j]
            temp[2]=img_srt[i+2][j]
            temp[3]=img_srt[i+3][j]
            
            img_mct[i][j] = galoisMult(temp[0],2) ^ galoisMult(temp[3],1) ^ galoisMult(temp[2],1) ^ galoisMult(temp[1],3)
            img_mct[i+1][j] = galoisMult(temp[1],2) ^ galoisMult(temp[0],1) ^ galoisMult(temp[3],1) ^ galoisMult(temp[2],3)
            img_mct[i+2][j] = galoisMult(temp[2],2) ^ galoisMult(temp[1],1) ^ galoisMult(temp[0],1) ^ galoisMult(temp[3],3)
            img_mct[i+3][j] = galoisMult(temp[3],2) ^ galoisMult(temp[2],1) ^ galoisMult(temp[1],1) ^ galoisMult(temp[0],3)

    return img_mct


# Add Round Key Transformation
def add_round_key_transform(img_mct,roundKey):
    img_arkt=np.zeros((256,256),int)
    img_arkt=img_mct^roundKey

    return img_arkt




def main_encrypt(number, file_name):
# if __name__ == '__main__':
    img = get_image(file_name)
    # cv.imshow('img', img)
    # cv.waitKey(0)

    #number = input('Enter a 16 digit key')
    if len(number) == 16:
        roundKey = get_array_key(number)
    else:
        print('Invalid Input')
        

    # Substitute Byte Transformation
    img_sbt=np.zeros((256,256),int)
    img_sbt=sub_byte_transform(img)
    # print(img_sbt)
    # img_sbt = img_sbt.astype(np.uint8)
    # cv.imshow('img_sbt', img_sbt)
    # cv.waitKey(0)

    # Shift Rows Transformation
    img_srt=np.zeros((256,256),int)
    img_srt=shift_row_transform(img_sbt)
    # print(img_srt)
    # img_srt = img_srt.astype(np.uint8)
    # cv.imshow('img_srt', img_srt)
    # cv.waitKey(0)

    # Mix Columns Transformation
    img_mct=np.zeros((256,256),int)
    img_mct=mix_col_transform(img_srt)
    # print(img_mct)
    # img_mct = img_mct.astype(np.uint8)
    # cv.imshow('img_mct', img_mct)
    # cv.waitKey(0)

    # Add Round Key Transformation
    img_arkt=np.zeros((256,256),int)
    img_arkt=add_round_key_transform(img_mct,roundKey)
    # print(img_arkt)
    # img_arkt = img_arkt.astype(np.uint8)
    # cv.imshow('img_arkt', img_arkt)
    # cv.waitKey(0)
    path = 'static/encrypted_images/'
    cv.imwrite(path + file_name, img_arkt)
