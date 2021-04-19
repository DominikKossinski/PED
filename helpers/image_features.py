import cv2
import numpy as np
import pickle
import matplotlib.pyplot as plt

def calculate2(img):

    if img.shape[:2] != (90,120): return None
    img = img[11:-11,:]

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # srednie

    gray_mean = cv2.imread("reference_images/gray_mean_all.png",0)
    gray_score = np.sum(np.abs(gray - gray_mean))
    color_mean = cv2.imread("reference_images/color_mean_all.png")
    color_score = np.sum(np.abs(img[:,:,0] - color_mean[:,:,0]) + np.abs(img[:,:,1] - color_mean[:,:,1]) + np.abs(img[:,:,2] - color_mean[:,:,2]))

    # hist
    g,c = get_hist(img)
    
    hist_gray = pickle.load(open("reference_images/hist_gray_mean_all.pck",'rb'))
    hist_col = pickle.load(open("reference_images/hist_col_mean_all.pck",'rb'))
    hist_gray_score = np.sum(np.abs(g - hist_gray))
    hist_col_score = (np.sum(np.abs(c[0] - hist_col[0])), np.sum(np.abs(c[1] - hist_col[1])), np.sum (np.abs(c[2] - hist_col[2])))


            
    edges = cv2.Canny(img,100,200)
    edges_mean = cv2.imread("reference_images/edges_mean_all.png",0)
    edges_score = np.sum(np.abs(edges - edges_mean))

    # entropy        
    entr = calc_entropy(img)
    entr_mean,_ = pickle.load(open("reference_images/entr_mean_all.pck",'rb'))

    entr_score = np.sum(np.abs(entr - entr_mean))

    return edges_score
    return gray_score, color_score, hist_gray_score




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