import collections
import serial, numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import threading

with plt.style.context("dark_background"):
    fig, ax = plt.subplots()

    de = collections.deque([0]*532, maxlen=532)

    port = 'COM6'
    baud_rate = 112500
    ser = serial.Serial(port, baud_rate, timeout=1)

    def thread1():
        while True:
            if ser.in_waiting > 0:
                try:
                    data = ser.readline().decode().strip().split(",")
                    if int(data[2]) == 0:
                        de.append(int(data[0]))
                except :
                    print("Received invalid data from the serial port")
                    
    t1 = threading.Thread(target=thread1)
    t1.start()

    def updatewavelet(i):
        ax.clear()  # Clear the current plot
        sig  = list(de)
        widths = np.arange(1, 31)
        cwtmatr = signal.cwt(sig, signal.ricker, widths)
        cwtmatr_yflip = np.flipud(cwtmatr)
        im = ax.imshow(cwtmatr_yflip, extent=[-1, 1, 1, 31], cmap='plasma', aspect='auto',
                       vmax=abs(cwtmatr).max(), vmin=-abs(cwtmatr).max())  # Update the plot
        return im,
        
    ani = FuncAnimation(fig, updatewavelet, frames=range(2), interval=int(1000/10), blit=True)
    plt.show()