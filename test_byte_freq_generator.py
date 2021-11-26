import sys
import time
import binascii
import numpy
from StreamReaderThread import StreamReaderThread
from BufferedPackets import BufferedPackets
from PcapReaderThread import PcapReaderThread


def main():
     try:
         #root_directory = "/home/baskoro/Documents/Dataset/ISCX12/without retransmission/"
         filename = "test3.pcap"
         protocol = "tcp"
         port = "443"
         batch_size=10000
         data = byte_freq_generator(filename, protocol, port, batch_size)

         counterdata= 0

         for item in data:
             counterdata=counterdata+1
             #print(item)
         print (counterdata)

     except IndexError:
         print ("IndexError")
     except KeyboardInterrupt:
         print ("Keyboard Intterupt")

def byte_freq_generator(filename, protocol, port, batch_size):
    global prt
    global conf
    global done
    prt = StreamReaderThread(filename, protocol, port)
    prt.start()
    counter = 0
    done = False

    while not done:
        while not prt.done or prt.has_ready_message():
            if not prt.has_ready_message():
                prt.wait_for_data()
                continue
            else:
                buffered_packets = prt.pop_connection()
                if buffered_packets is None:
                    time.sleep(0.0001)
                    continue
                if buffered_packets.get_payload_length("server") > 0:
                    byte_frequency = buffered_packets.get_byte_frequency("server")
                    X = numpy.reshape(byte_frequency, (1, 256))

                    if counter == 0 or counter % batch_size == 1:
                        dataX = X
                    else:
                        dataX = numpy.r_["0,2", dataX, X]

                    counter += 1

                    if counter % batch_size == 0:
                        yield dataX, dataX

        if dataX.shape[0] > 0:
            yield dataX, dataX

        prt.reset_read_status()

if __name__ == "__main__":
    main()