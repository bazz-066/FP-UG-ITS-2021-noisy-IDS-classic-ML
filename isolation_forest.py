from StreamReaderThread import StreamReaderThread

import sys
import time
#import csv
import numpy
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from numpy import quantile, where


def main(argv):
    try:
        final_list= get_data_bytefreq()
        arr = numpy.array(final_list)
        #print(arr)
        IsoForest(arr)

    except IndexError:
        print("Usage: python pcap_to_csv.py <pcap_filename>")

def get_data_bytefreq():
    
    filename = "test4.pcap"
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
    
def IsoForest(x):
    plt.scatter(x[:,0], x[:,1])
    plt.show()
    print(x)
    svm = IsolationForest(random_state=0)
    print(svm)
    svm.fit(x)
    pred = svm.predict(x)
    print(pred)
    anom_index = where(pred==-1)
    values = x[anom_index]
    plt.scatter(x[:,0], x[:,1])
    plt.scatter(values[:,0], values[:,1], color='r')
    plt.show()

if __name__ == '__main__':
	main(sys.argv)