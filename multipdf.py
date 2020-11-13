
import base64
import io
import matplotlib
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.image as mpimg
import cv2
import numpy as np
import importlib

def readb64(uri):
   encoded_data = uri.split(',')[1]
   nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
   img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
   return img

def make_pdf(images,title):
    importlib.reload(matplotlib)
    
    with PdfPages("pdfs/"+title + ".pdf") as pdf:
        for image in images:

            #images from other possible sources, depending on format of image
            #f = io.BytesIO(urlopen(filename).read())
            #f = open(filename, "rb")
            plt.rc('text', usetex=True)
            plt.figure()
            #plt.cla()
            image = readb64(image)
            plt.imshow(image[...,::-1],interpolation="nearest",aspect='auto')
            #img.set_cmap('hot')
            plt.axis('off')
            pdf.savefig(dpi=400,facecolor="white")
            plt.close()

        d = pdf.infodict()
        d['Title'] = 'Multipage PDF Example'
        d['Author'] = 'Jouni K. Sepp\xe4nen'
        d['Subject'] = 'How to create a multipage pdf file and set its metadata'
        d['Keywords'] = 'PdfPages multipage keywords author title subject'