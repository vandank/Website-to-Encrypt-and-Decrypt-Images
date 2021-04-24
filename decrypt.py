import numpy as np
import cv2 as cv
import os


def get_image(file_name):
    path = 'static/uploaded_images(decrypte)/'
    img = cv.imread(os.path.join(path, file_name))
    # print(img)
    # img = img.astype(np.uint8)
    # cv.imshow('lamp', img)
    # cv.waitKey(0)

    # img = cv.IMREAD_GRAYSCALE(img, cv.COLOR_BGR2GRAY)
    # cv.imshow('lamp', img)
    # cv.waitKey(0)

    # img=cv.resize(img,(256,256))
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


def inverse_add_round_key_transform(img_arkt,roundKey):
    img_iarkt=np.zeros((256,256),int)
    img_iarkt=img_arkt^roundKey

    return img_iarkt
    

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


def inv_mix_col_transform(img_iarkt):
    img_imct=np.zeros((256,256),int)
    temp=[0]*4

    # Applying the transformation on columns of size (4,1) at a time
    for i in range(0,256,4):
        for j in range(256):
            temp[0]=img_iarkt[i][j]
            temp[1]=img_iarkt[i+1][j]
            temp[2]=img_iarkt[i+2][j]
            temp[3]=img_iarkt[i+3][j]
            
            img_imct[i][j] = galoisMult(temp[0],14) ^ galoisMult(temp[3],9) ^ galoisMult(temp[2],13) ^ galoisMult(temp[1],11)
            img_imct[i+1][j] = galoisMult(temp[1],14) ^ galoisMult(temp[0],9) ^ galoisMult(temp[3],13) ^ galoisMult(temp[2],11)
            img_imct[i+2][j] = galoisMult(temp[2],14) ^ galoisMult(temp[1],9) ^ galoisMult(temp[0],13) ^ galoisMult(temp[3],11)
            img_imct[i+3][j] = galoisMult(temp[3],14) ^ galoisMult(temp[2],9) ^ galoisMult(temp[1],13) ^ galoisMult(temp[0],11)

    return img_imct


def inv_shift_row_transform(img_imct):
    img_isrt=np.zeros((256,256),int)

    # Converting array to lists so that to lists can be added using '+' sign
    img_imct=img_imct.tolist()

    # Shift rows transformation
    for i in range(256):
        img_isrt[i]=img_imct[i][-i:]+img_imct[i][0:-i]
    
    return img_isrt


def inv_sub_byte_transform(img_isrt):
    sboxInv = [
            0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb,
            0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb,
            0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,
            0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25,
            0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92,
            0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84,
            0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06,
            0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b,
            0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
            0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e,
            0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
            0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4,
            0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f,
            0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef,
            0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61,
            0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d
            ]
    
    # Coverting int image matrix to hex
    vhex = np.vectorize(hex)
    img_isrt_hex = vhex(img_isrt)
    # print(img_isrt_hex)

    # Inverse substitute byte transformation
    img_isbt=np.zeros((256,256),int)
    for i in range(256):
        for j in range(256):
            k=int(img_isrt_hex[i][j],0)
            img_isbt[i][j]=sboxInv[k]
    
    return img_isbt


def main_decrypt(number, file_name):
# if __name__ == '__main__':
    img = get_image(file_name)
    # cv.imshow('img', img)
    # cv.waitKey(0)

    # number = '1236549879876543'
    #number = input('Enter a 16 digit key')
    if len(number) == 16:
        roundKey = get_array_key(number)
    else:
        print('Invalid Input')
    
    
    b, g, r    = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    x = []
    x.append(b)
    x.append(g)
    x.append(r)

    for i in range(3):
        img_iarkt=np.zeros((256,256),int)
        img_iarkt=inverse_add_round_key_transform(x[i],roundKey)
        

        img_imct=np.zeros((256,256),int)
        img_imct=inv_mix_col_transform(img_iarkt)


        img_isrt=np.zeros((256,256),int)
        img_isrt=inv_shift_row_transform(img_imct)
        

        img_isbt=np.zeros((256,256),int)
        img_isbt=inv_sub_byte_transform(img_isrt)
        x[i] = img_isbt
    
    img = np.dstack((x[0],x[1],x[2]))
    
    path = 'static/decrypted_images/'
    cv.imwrite(path + file_name, img)
    return file_name
