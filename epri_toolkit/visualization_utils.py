import matplotlib.pyplot as plt
import numpy as np


def disp_1x1(img1):
    plt.imshow(img1, cmap=plt.jet())
    plt.show()


def disp_2x2(img1, img2, img3, img4):
    plt.subplot(2, 2, 1)
    plt.imshow(img1, cmap=plt.jet(), vmax=np.max(img1), vmin=0)
    plt.subplot(2, 2, 2)
    plt.imshow(img2, cmap=plt.jet(), vmax=np.max(img2), vmin=0)
    plt.subplot(2, 2, 3)
    plt.imshow(img3, cmap=plt.jet(), vmax=np.max(img3), vmin=0)
    plt.subplot(2, 2, 4)
    plt.imshow(img4, cmap=plt.jet(), vmax=np.max(img4), vmin=0)
    plt.show()


def disp_4D(img1, img2, img3, img4):
    plt.subplot(2, 2, 1)
    plt.imshow(img1, cmap=plt.jet(), vmax=np.max(img1), vmin=0)
    plt.subplot(2, 2, 2)
    plt.imshow(img2, cmap=plt.jet(), vmax=np.max(img2), vmin=0)
    plt.subplot(2, 2, 3)
    plt.imshow(img3, cmap=plt.jet(), vmax=np.max(img3), vmin=0)
    plt.subplot(2, 2, 4)
    plt.plot(img4)
    plt.show()
