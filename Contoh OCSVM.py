from sklearn.svm import OneClassSVM
from sklearn.datasets import make_blobs
from numpy import quantile, where, random
import matplotlib.pyplot as plt


def main():
    try:
        random.seed(13)
        x, _ = make_blobs(n_samples=200, centers=1, cluster_std=.3, center_box=(8, 8))
        plt.scatter(x[:,0], x[:,1])
        plt.show()
        print(x)
        svm = OneClassSVM(kernel='rbf', gamma=0.001, nu=0.03)
        print(svm)
        svm.fit(x)
        pred = svm.predict(x)
        anom_index = where(pred==-1)
        values = x[anom_index]
        plt.scatter(x[:,0], x[:,1])
        plt.scatter(values[:,0], values[:,1], color='r')
        plt.show()
        svm = OneClassSVM(kernel='rbf', gamma=0.001, nu=0.02)
        print(svm)
        pred = svm.fit_predict(x)
        scores = svm.score_samples(x)
        thresh = quantile(scores, 0.03)
        print(thresh)
        index = where(scores<=thresh)
        values = x[index]
        plt.scatter(x[:,0], x[:,1])
        plt.scatter(values[:,0], values[:,1], color='r')
        plt.show()
    except IndexError:
         print ("IndexError")
    except KeyboardInterrupt:
         print ("Keyboard Interrupt")

if __name__ == "__main__":
    main()
