from StreamReaderThread import StreamReaderThread

import sys
import time
#import csv
import numpy
import matplotlib.pyplot as plt
from sklearn.svm import OneClassSVM
from numpy import quantile, where


def main(argv):
    try:
        final_list= get_data_bytefreq()
        arr = numpy.array(final_list)
        print(arr)
        #ocsvm(arr)

    except IndexError:
        print("Usage: python pcap_to_csv.py <pcap_filename>")

def get_data_bytefreq():
    
    filename = "test2.pcap"
    protocol = "tcp"
    prt = StreamReaderThread(filename, protocol, "443")
    prt.delete_read_connections = True
    prt.start()

    counter = 0
    final_list= []

    while not prt.done or prt.has_ready_message():
        if not prt.has_ready_message():
            time.sleep(0.0001)
            continue
        buffered_packets = prt.pop_connection()
        buffered_packets.get_byte_frequency("server")
        if buffered_packets is not None:
            #print(buffered_packets.get_byte_frequency("client"))
            counter += 1
            list_temp=[]
            byte_frequency = buffered_packets.get_byte_frequency("server")
            list_temp.extend(byte_frequency)
            final_list.append(list_temp)
            sys.stdout.write("\r{} flows.".format(counter))
            sys.stdout.flush()
        
    #print(final_list)
    return final_list
    
def ocsvm(x):
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

if __name__ == '__main__':
	main(sys.argv)