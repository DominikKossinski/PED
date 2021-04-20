import cv2
import numpy as np
import pickle
import matplotlib.pyplot as plt
import pytesseract

from helpers.image_features_back import *


def preprocess_image(img):
    if img.shape[:2] != (90,120): return None
    img = img[11:-11,:]
    return img


def get_gray_score(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_mean = cv2.imread("reference_images/gray_mean_all.png",0)
    gray_score = np.sum(np.abs(gray - gray_mean))

    return gray_score

def get_color_score(img):
    color_mean = cv2.imread("reference_images/color_mean_all.png")
    color_score = np.sum(np.abs(img[:,:,0] - color_mean[:,:,0]) + np.abs(img[:,:,1] - color_mean[:,:,1]) + np.abs(img[:,:,2] - color_mean[:,:,2]))

    return color_score

def get_hist_score(img):
    g,c = get_hist(img)

    hist_gray = pickle.load(open("reference_images/hist_gray_mean_all.pck",'rb'))
    hist_col = pickle.load(open("reference_images/hist_col_mean_all.pck",'rb'))
    hist_gray_score = np.sum(np.abs(g - hist_gray))
    hist_col_score = (np.sum(np.abs(c[0] - hist_col[0])), np.sum(np.abs(c[1] - hist_col[1])), np.sum (np.abs(c[2] - hist_col[2])))

    return hist_gray_score, hist_col_score

def get_edges_score(img):        
    edges = cv2.Canny(img,100,200)
    edges_mean = cv2.imread("reference_images/edges_mean_all.png",0)
    edges_score = np.sum(np.abs(edges - edges_mean))

    return edges_score


def get_entr_score(img):    
    entr = calc_entropy(img)
    entr_mean,_ = pickle.load(open("reference_images/entr_mean_all.pck",'rb'))
    entr_score = np.sum(np.abs(entr - entr_mean))

    return entr_score


# def get_vevo(img):
#     text = pytesseract.image_to_string(img)
#     text = text.lower()
#     if text.find("vevo") != -1: return True
#     else: return False

def get_vevo(text):
    # text = pytesseract.image_to_string(img)
    text = str(text)
    text = text.lower()
    if text.find("vevo") != -1: return True
    else: return False