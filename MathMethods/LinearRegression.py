# -*- coding: utf-8 -*-
# 线性回归方法总结：1.梯度下降；2.最小二乘法/正态方程法；3.Adam；4.奇异值分解（SVD）
import os
import numpy as np
import math
import seaborn as sns
from scipy import stats

from matplotlib import pyplot


class GradientDescent:
    """
    梯度下降法
    对于初学者来说，解决线性回归问题的最常见，最简单的方法之一就是梯度下降。
    梯度下降的工作原理：现在，让我们假设我们以散点图的形式绘制了数据，并且当我们对它应用成本函数时，我们的模型将做出预测。现在，此预测可能非常好，或者可能与我们的理想预测相去甚远（这意味着其成本将会很高）。
    因此，为了最小化该成本（误差），我们对其应用了梯度下降。现在，梯度下降将使我们的假设逐渐收敛到成本 最低的全局最小值 。为此，我们必须手动设置alpha的值 ， 并且假设的斜率相对于我们alpha的值而变化。如果alpha值较大，则将采取较大步骤。否则，在小阿尔法的情况下，我们的假设将缓慢收敛并通过小步伐收敛。
    优点：梯度下降的重要优点是与SVD或ADAM相比，计算成本更低运行时间为O（kn²）与更多功能一起使用效果很好
    缺点：梯度下降的重要缺点是需要选择一些学习率 α需要多次迭代才能收敛以卡在本地最小值如果学习率 α不合适，则可能无法收敛。
    """

    def __init__(self):
        # super().__init__()
        self.property = "线性回归之梯度下降法"
        print(self.property)

    def method_GradientDescent(self):
        print("我被调用了！")

        # creating our data
        X = np.random.rand(10, 1)
        y = np.random.rand(10, 1)
        m = len(y)
        theta = np.ones(1)
        # applying gradient descent
        a = 0.0005
        cost_list = []
        for i in range(len(y)):
            theta = theta - a*(1/m)*np.transpose(X)@(X@theta - y)
            cost_val = (1/m)*np.transpose(X)@(X@theta - y)
            cost_list.append(cost_val)
        # Predicting our Hypothesis
        b = theta
        yhat = X.dot(b)
        # Plotting our results
        pyplot.scatter(X, y, color='red')
        pyplot.plot(X, yhat, color='blue')
        pyplot.show()


class LSM:
    """
    最小二乘法：θ=(X_t*X)-1
    最小二乘法也称为 正态方程， 也是轻松求解线性回归模型的最常用方法之一。但是，这需要具有线性代数的一些基本知识。
    最小二乘法如何工作：在普通的LSM中，我们直接求解系数值。简而言之，我们一步就能达到光学的最低点，或者我们只能说一步就可以以最低的成本使我们的假设适合我们的数据。
    优点：LSM的重要优点是：没有学习率没有迭代；不需要功能缩放；当“功能数量”较少时，效果很好。
    缺点：重要的缺点是：当数据集很大时，计算量很大；功能数量多时速度慢；运行时间为O（n³）有时，您的X转置X是不可逆的，即，没有逆的奇异矩阵。您可以使用np.linalg.pinv代替 np.linalg.inv 来解决此问题。
    """

    def __init__(self):
        super().__init__()

    def method_LSM(self):
        # creating our data
        X = np.random.rand(10, 1)
        y = np.random.rand(10, 1)
        # Computing coefficient
        b = np.linalg.inv(X.T.dot(X)).dot(X.T).dot(y)
        # Predicting our Hypothesis
        yhat = X.dot(b)
        # Plotting our results
        pyplot.scatter(X, y, color='red')
        pyplot.plot(X, yhat, color='blue')
        pyplot.show()


class AdamOptimizer:
    """
    ADAM代表自适应矩估计，是一种在深度学习中广泛使用的优化算法。这是一种迭代算法，适用于嘈杂的数据。
    它是RMSProp和小批量梯度下降算法的组合。
    除了存储像Adadelta和RMSprop这样的过去平方梯度的指数衰减平均值之外，Adam还保留了过去梯度的指数衰减平均值，类似于动量。
    我们分别计算过去和过去平方梯度的衰减平均值，如下所示：

    """

    def __init__(self, weights, alpha=0.001, beta1=0.9, beta2=0.999, epsilon=1e-8):
        self.alpha = alpha
        self.beta1 = beta1
        self.beta2 = beta2
        self.epsilon = epsilon
        self.m = 0
        self.v = 0
        self.t = 0
        self.theta = weights

    def method_backward_pass(self, gradient):
        self.t = self.t + 1
        self.m = self.beta1*self.m + (1 - self.beta1)*gradient
        self.v = self.beta2*self.v + (1 - self.beta2)*(gradient**2)
        m_hat = self.m/(1 - self.beta1**self.t)
        v_hat = self.v/(1 - self.beta2**self.t)
        self.theta = self.theta - self.alpha * \
            (m_hat/(np.sqrt(v_hat) - self.epsilon))
        return self.theta


class SVD:
    """
    奇异值分解
    由于SVD是线性回归中最著名且使用最广泛的降维方法之一，因此缩短了奇异值分解。
    SVD（作为其他用途）被用作预处理步骤，以减少我们的学习算法的维数。SVD将矩阵分解为其他三个矩阵（U，S，V）的乘积。
    矩阵分解后，可以通过计算输入矩阵X的伪逆 并将其乘以输出向量 y来找到假设的系数 。在那之后，我们使我们的假设适合我们的数据，这使我们的成本最低。
    优点：使用更高维度的数据时效果更好;适用于高斯型分布式数据;对于小型数据集，真正稳定且高效;在求解线性回归线性方程时，它是更稳定且首选的方法。
    缺点：运行时间为O（n³）;多重危险因素;对异常值非常敏感;数据集很大时可能会变得不稳定
    """

    def __init__(self):
        super().__init__()

    def method_SVD(self):
        # Creating our data
        X = np.random.rand(10, 1)
        y = np.random.rand(10, 1)
        # Computing coefficient
        b = np.linalg.pinv(X).dot(y)
        # Predicting our Hypothesis
        yhat = X.dot(b)  # Plotting our results
        pyplot.scatter(X, y, color='red')
        pyplot.plot(X, yhat, color='blue')
        pyplot.show()
