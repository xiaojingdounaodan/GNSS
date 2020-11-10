# -*- coding: UTF-8 -*-

from MathMethods.LinearRegression import GradientDescent, LSM, AdamOptimizer, SVD

if __name__ == "__main__":

    m1 = GradientDescent()
    m1.method_GradientDescent()

    m2 = LSM()
    m2.method_LSM()

    m3 = AdamOptimizer(5)
    m3.method_backward_pass(1)

    m4 = SVD()
    m4.method_SVD()
