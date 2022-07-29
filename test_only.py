from StreamReaderThread import StreamReaderThread

import sys
import time
import timeit
#import csv
import numpy
import matplotlib.pyplot as plt
from sklearn.svm import OneClassSVM
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from numpy import quantile, where
import joblib

tcp_tuple1= []
tcp_tuple2= []
tcp_tuple3= []
tcp_tuple4= []

def main(argv):
    try:
        start_time = timeit.default_timer()
        final_list= get_data_bytefreq()
        arr = numpy.array(final_list)
        ocsvm(arr)
        IsoForest(arr)
        lof(arr)
        stop = timeit.default_timer()
        execution_time = stop - start_time
        print("Program Executed in "+str(execution_time))

    except IndexError:
        print("Usage: python pcap_to_csv.py <pcap_filename>")

    
def get_data_bytefreq():
    
    filename = "combined-00080.pcap"
    protocol = "tcp"
    prt = StreamReaderThread(filename, protocol, "80")
    prt.delete_read_connections = True
    prt.start()

    counter = 0
    final_list= []

    while not prt.done or prt.has_ready_message():
        if not prt.has_ready_message():
            time.sleep(0.0001)
            continue
        buffered_packets = prt.pop_connection()
        #buffered_packets.get_byte_frequency("server")
        if buffered_packets is not None:
            #print(buffered_packets.get_byte_frequency("client"))
            counter += 1
            #list_temp=[]
            byte_frequency = buffered_packets.get_byte_frequency("server")
            #list_temp.extend(byte_frequency)
            final_list.append(byte_frequency)
            tcp_tuple1.append(buffered_packets.tcp_tuple[0])
            tcp_tuple2.append(buffered_packets.tcp_tuple[1])
            tcp_tuple3.append(buffered_packets.tcp_tuple[2])
            tcp_tuple4.append(buffered_packets.tcp_tuple[3])
            sys.stdout.write("\r{} flows.".format(counter))
            sys.stdout.flush()
        
    #print(final_list)
    return final_list

def ocsvm(x):
    
    svm = joblib.load('ocsvm.pkl')
    #svm.predict(x)
    pred = svm.predict(x)
    print(pred)
    #anom_index = where(pred==-1)
    #values = x[anom_index]
    #plt.scatter(x[:,0], x[:,1])
    #plt.scatter(values[:,0], values[:,1], color='r')
    #plt.show()
    csv_name="ocsvm_result.csv"
    result_csv(pred,csv_name)

def IsoForest(x):
    
    svm = joblib.load('IsoForest.pkl')
    pred = svm.predict(x)
    print(pred)
    #anom_index = where(pred==-1)
    #values = x[anom_index]
    #plt.scatter(x[:,0], x[:,1])
    #plt.scatter(values[:,0], values[:,1], color='r')
    #plt.show()
    csv_name="Isoforest_result.csv"
    result_csv(pred,csv_name)

def lof(x):
    
    svm = joblib.load('lof.pkl')
    pred = svm.predict(x)
    print(pred)
    #anom_index = where(pred==-1)
    #values = x[anom_index]
    #plt.scatter(x[:,0], x[:,1])
    #plt.scatter(values[:,0], values[:,1], color='r')
    #plt.show()
    csv_name="lof_result.csv"
    result_csv(pred,csv_name)

def result_csv(prediction,csv_name):
    fcsv = open(csv_name, "w")
    counter_csv=0
    for i in prediction:
        fcsv.write("{},{},{},{},{}\n".format(tcp_tuple1[counter_csv], tcp_tuple2[counter_csv], tcp_tuple3[counter_csv], tcp_tuple4[counter_csv],prediction[counter_csv]))
        sys.stdout.write("\r{} flows.".format(counter_csv+1))
        sys.stdout.flush()
        counter_csv=counter_csv+1
    fcsv.close()

if __name__ == '__main__':
	main(sys.argv)