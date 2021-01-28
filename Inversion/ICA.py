# 独立分量算法
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import FastICA


class ICA:
    """
    ICA独立分量反演算法
    """

    def __init__(self):
        print("ICA 反演算法被调用了！")

    def ICA_gnss(self):
        C = 200
        x = np.arange(C)
        a = np.linspace(-2, 2, 25)
        s1 = np.array([a, a, a, a, a, a, a, a]).reshape(200, )
        s2 = 2 * np.sin(0.02 * np.pi * x)
        s3 = np.array(20 * (5 * [2] + 5 * [-2]))
        ax1 = plt.subplot(311)
        ax2 = plt.subplot(312)
        ax3 = plt.subplot(313)
        ax1.plot(x, s1)
        ax2.plot(x, s2)
        ax3.plot(x, s3)
        plt.show()
        s = np.array([s1, s2, s3])
        ran = 2*np.random.random([3, 3])
        mix = ran.dot(s)
        ax1 = plt.subplot(311)
        ax2 = plt.subplot(312)
        ax3 = plt.subplot(313)
        ax1.plot(x, mix[0, :])
        ax2.plot(x, mix[1, :])
        ax3.plot(x, mix[2, :])
        plt.show()
        ica = FastICA(n_components=2)
        mix = mix.T
        u = ica.fit_transform(mix)
        u = u.T
        ax1 = plt.subplot(311)
        ax2 = plt.subplot(312)
        ax3 = plt.subplot(313)
        ax1.plot(x, u[0, :])
        ax2.plot(x, u[1, :])
        ax3.plot(x, u[2, :])
        plt.show()
