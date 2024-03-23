import collections, random
import serial, numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import threading

ani = None
NORM_SCALE = 0.2
FFT_SCALE = 100000*0.3
with plt.style.context("dark_background"):
    changed = False
    opt = 0
    pstate = 0
    fig, ax = plt.subplots()

    de = collections.deque([0]*532, maxlen=532)

    x = list(range(0, 532))
    y = list(de)
    # define axis limits
    ax.set_ylim(0, NORM_SCALE)
    line, = ax.plot(x, y)

    port = 'COM6'
    baud_rate = 112500

    def thread1():
        global opt, pstate, changed, de
        ser = serial.Serial(port, baud_rate, timeout=1)

        while True:
            if ser.in_waiting > 0:
                try:
                    data = ser.readline().decode().strip().split(",")
                    if int(data[2]) == 0:
                        de.append(int(data[0]))
                    opt = int(data[1])
                    if opt != pstate:
                        changed = True
                        
                        
                except Exception as e:
                    print(e)

    t1 = threading.Thread(target=thread1)
    t1.start()

    def updatemain(i):
        global changed, de
        if changed:            
            changed = False
            if opt == 0:
                de = collections.deque([0]*532, maxlen=532)
        if opt == 0:
            ax.set_ylim(0, NORM_SCALE)
            return update(i)
        elif opt == 1:
            ax.set_ylim(0, FFT_SCALE)
            return updatefft(i)
        elif opt == 2:
            return updatewavelet(i)
        else:
            ax.set_ylim(0, NORM_SCALE)
            return update(i)
    def update(i):
        
        y = list(de)
        y = [i*(3.1/4095) for i in y]
        line.set_ydata(y)
        return line,

    def updatefft(i):
        global de, line, y, x, ax
        #print(de[-1]) # always 0
        y = np.abs(np.fft.fft(de))
        line.set_ydata(y)
        return  line,

    def updatewavelet(i):
        ax.clear()  # Clear the current plot
        sig  = list(de)
        widths = np.arange(1, 31)
        cwtmatr = signal.cwt(sig, signal.ricker, widths)
        cwtmatr_yflip = np.flipud(cwtmatr)
        im = ax.imshow(cwtmatr_yflip, extent=[-1, 1, 1, 31], cmap='plasma', aspect='auto',
                       vmax=abs(cwtmatr).max(), vmin=-abs(cwtmatr).max())  # Update the plot
        return im

    ani = FuncAnimation(fig, updatemain, frames=range(2), interval=int(1000/10), blit=True)
    plt.show()