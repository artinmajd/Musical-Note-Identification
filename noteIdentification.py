import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.io import wavfile
from scipy.signal import find_peaks
import numpy as np
import Envelope
from findPitch import findPitch
from musicalNote import musicalNote
import difference


def noteIdentification(path):

    fs, data = wavfile.read(path)# load the data

    print('sampling rate : ',fs)
    a = data.T[0] # this is a two channel soundtrack, I get the first track
    b=[(ele/2**8.)*2-1 for ele in a] # this is 8-bit track, b is now normalized on [-1,1)
    temptemp =b

    plt10 = plt.figure(10)
    plt.plot(temptemp)
    plt10.show()

    mean = sum(b)/len(b)
    b = b - mean     # removing the DC



    #########################################################################################
    ################################# Time Domain Envelope###################################
    #########################################################################################

    # envl = Envelope.getEnvelope(b,500)  # Envelope
    # beatsTemp =find_peaks(envl,distance=440,prominence=max(envl)/3)
    # beats = beatsTemp[0]
    #
    # print('detected notes being played at seconds: ' ,beats/44100)
    # plt3 = plt.figure(3)
    #
    # for i in beats:
    #     plt.plot(i,envl[i],"rx")
    #
    #
    # plt.plot(envl[:])
    # plt3.show()
    ##########################################################################################
    ##########################################################################################

    timeSlices =[]

    start =0
    interval = 1
    slice = b[int(start * fs):(int((start + interval) * fs)) - 1]  # a slice of b
    sampleNumber = 44100

    fourier_transform = fft(slice,n=sampleNumber) # calculate fourier transform (complex numbers list)
    print('most significant frequency is: ',(np.argmax(abs(fourier_transform))*fs)/sampleNumber)
    half_length_fourier = int(len(fourier_transform)/2)  # you only need half of the fft list (real signal symmetry)




    plt1 = plt.figure(1)
    halfFourier = abs(fourier_transform[:half_length_fourier-1])
    # print(halfFourier[0:1000])
    plt.plot(halfFourier,'r')
    plt1.show()              #Plot the fourier transform

    plt2 = plt.figure(2)
    plt.plot((b[:]),'r')
    plt2.show()              #Plot the normalized Amplitude signal



    # df = difference.dif(envl) #Difference computation
    # df2 = difference.dif(df)  #Second difference
    # changePoints = (np.argsort(df[:]))  #Sorting and keeping the args
    # print(changePoints[1:40])
    # print(np.sort(df)[len(df)-1:len(df)-500:-1], '\n\n\n')  #500 of the biggest differeces among all
    # print (sorted(df[222000:224000]),'\n\n\n\n\n')          #2000 of the biggest differences in 222 to 224 thousand
    # print (sorted(df[264800:265000]))                       #200 of the biggest differences in 264800 to 265 thousand

    # plt4 =plt.figure(4)
    # plt.plot(df)
    # plt4.show()
    #
    # plt6 = plt.figure(6)
    # plt.plot(df2)
    # plt6.show()

    segment =4410;
    freq_list=[]
    # for i in range(0,len(b),segment):
    #     freq_list.append()



    # plt5 = plt.figure(5)
    # plt.plot(slice)
    # plt5.show()


    ###################################################################################
    ################calculating the pitch using the envelope of the fft#################
    ###################################################################################


    resultEnv = Envelope.getEnvelope(halfFourier,10)
    plt7 =plt.figure(7)
    plt.plot(resultEnv)
    result1 = find_peaks(resultEnv,prominence= max(abs(fourier_transform))/10)
    result2 =[]
    for j in result1[0]:
        if j >= np.argmax(abs(fourier_transform))-7:
            result2.append(j)

    finalResult = findPitch(result2)
    print("the pitch of the tone is: ",finalResult)
    print(musicalNote(finalResult))


    for i in result2:
        plt.plot(i,0,"rx") #### marking the detected peaks

    plt7.show()

    ##################################################################################

    plt.show()


