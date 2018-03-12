import numpy as np
import cv2

def GetMaxElementArray(array):
    val = 0
    for element in array:
        if val<element:
            val=element
    return val

def GetMinElementMatrix(matrix):
    val = matrix[0,0]
    for array in matrix:
        for element in array:
            if val>element:
                val=element
    return val

def GetMaxElementMatrix(matrix):
    val = matrix[0,0]
    for array in matrix:
        for element in array:
            if val<element:
                val=element
    return val

def PrintMatrix(matrix):
    cols, rows = matrix.shape
    for y in range(0,cols):
        for x in range(0, rows):
            print matrix[y,x]

def getFilteredValue(img, kernel, i, j):
    value = 0
    imgx,imgy = img.shape
    kx,ky = kernel.shape
    #print "Filtered"
    for ix in range (-(kx/2),kx/2 +1):
        for iy in range (-(ky/2),ky/2 +1):
            #print "Loop"
            #print "i+ix "+str(i+ix)
            #print "ix "+str(ix)
            #print "imgx "+str(imgx)
            #print "j+iy "+str(j+iy)
            #print "iy "+str(iy)
            #print "imgy "+str(imgy)
            
            if(i+ix>=0 and i+ix < imgx and j+iy >=0 and j+ iy < imgy):
                value = value + img[i+ix][j+iy]*kernel[ix+kx/2][iy+ky/2]
                #print "Value! "+str(value)
    return value

def strechValue(value, minV, maxV, strechValue = 1.0):
    return ((value - minV)/(maxV - minV))*(strechValue)

def toAbs(matrix):
    cols, rows = matrix.shape
    for i in range(0,cols):
        for j in range(0,rows):
            matrix[i][j] = abs(matrix[i][j])
            
def ApplyKernel(img_to_apply, kernel):
    #print "Image"
    #print img_to_apply
    cols, rows = img_to_apply.shape
    new_img = np.zeros(img_to_apply.shape, np.float)
    for i in range(0,cols):
        for j in range(0,rows):
            new_img[i][j] = getFilteredValue(img_to_apply,kernel,i,j)

    #print "Without Abs"
    #print new_img

    toAbs(new_img)

    min_val = GetMinElementMatrix(new_img)
    max_val = GetMaxElementMatrix(new_img)
    
    #print "Abs"
    #print new_img
    
    for i in range(0,cols):
        for j in range(0,rows):
            new_img[i][j] = strechValue(new_img[i][j], min_val, max_val)

    #print "Normalized"
    #print new_img

    return new_img

img = cv2.imread('ricalin.png',0)

kernel1 = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
kernel2 = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
kernel44 = np.array([[1, 4, 6, 4, 1], [4, 16, 24, 16, 4], [6, 24, 36, 24, 6],
                     [4, 16, 24, 16, 4], [1, 4, 6, 4, 1]])
img2 = ApplyKernel(img, kernel1)
img3 = ApplyKernel(img, kernel2)

cv2.imshow('Normal', img)
cv2.imshow('Kernel 1', img2)
cv2.imshow('Kernel 2', img3)
cv2.imshow('Kernel 3', ApplyKernel(img, kernel44))

#filename = input("Introduce Image path: ")

k = cv2.waitKey(0)

if k == 27:
    # Wait for ESC key to exit
    cv2.destroyAllWindows()
