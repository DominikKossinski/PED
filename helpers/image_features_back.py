import cv2
import numpy as np
import pickle
import matplotlib.pyplot as plt


def get_hist(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hist_gray = cv2.calcHist([gray],[0],None,[256],[0,256])
    hists = []
    color = ('b','g','r')
    for i,col in enumerate(color):
        histr = cv2.calcHist([img],[i],None,[256],[0,256])
        hists.append(histr)  
    return hist_gray, hists
    


def draw_hist(hist1,t1, hist2,t2, color=True):
    fig, axs = plt.subplots(1,2,figsize=(16,5))
    if not color:
        axs[0].plot(hist1)
        axs[1].plot(hist2)
    else:
        for hst,col in zip(hist1, ('b','g','r')):
            axs[0].plot(hst,color = col)
        for hst,col in zip(hist2, ('b','g','r')):
            axs[1].plot(hst,color = col)
    axs[0].title.set_text(t1)
    axs[1].title.set_text(t2)
    plt.xlim([-10,266])
    plt.show()


def histogram(d):
    grays, colors = calculate(d,'hist')

    gray_mean = np.mean(grays, axis = 0)
    gray_med = np.median(grays, axis = 0)
    colors = list(zip(*colors))
    color_mean = [np.mean(x, axis = 0) for x in colors]
    color_median = [np.median(x, axis = 0) for x in colors]



def entropy(signal):
        lensig=signal.size
        symset=list(set(signal))
        numsym=len(symset)
        propab=[np.size(signal[signal==i])/(1.0*lensig) for i in symset]
        ent=np.sum([p*np.log2(1.0/p) for p in propab])
        return ent
    
    
def layer_entropy(img,N=5):
    S=img.shape
    E=np.array(img)
    for row in range(S[0]):
          for col in range(S[1]):
            Lx=np.max([0,col-N])
            Ux=np.min([S[1],col+N])
            Ly=np.max([0,row-N])
            Uy=np.min([S[0],row+N])
            region=img[Ly:Uy,Lx:Ux].flatten()
            E[row,col]=entropy(region)
    return E


def calc_entropy(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    scale = 0.3
    img = cv2.resize(img, (int(img.shape[1]*scale),int(img.shape[0]*scale)))
    img = layer_entropy(img,3)
    
    return img
    


def show_entropy(img,t1,img2,t2):
    fig, axs = plt.subplots(1,2,figsize=(16,5))
    im1 = axs[0].imshow(img, cmap=plt.cm.jet)
    fig.colorbar(im1,ax=axs[0], shrink=0.6)
    im2 = axs[1].imshow(img2, cmap=plt.cm.jet)
    fig.colorbar(im2,ax=axs[1], shrink=0.6)
    axs[0].title.set_text(t1)
    axs[1].title.set_text(t2)
    
    plt.show()