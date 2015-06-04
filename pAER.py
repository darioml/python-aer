from PIL import Image
import math
import numpy as np

import os, datetime,time

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import cm


class pAER:
    def __init__(self, filename, max_events=1e6):
        self.filename = filename
        self.max_events = max_events
        self.header = []

        self.load()

    def load(self):
        with open(self.filename, 'r') as f:
            line = f.readline()
            while (line[0] == '#'):
                self.header.append(line)
                if (line[0:9] == '#!AER-DAT'):
                    aer_version = line[9];
                current = f.tell();
                line = f.readline()


            if (aer_version != '2'):
                raise Exception('Invalid AER version. Expected 2, got %s' % aer_version)

            f.seek(0,2)
            numEvents = math.floor( ( f.tell() - current ) / 8 )
            
            if numEvents > self.max_events:
                print 'There are %i events, but max_events is set to %i. Will only use %i events.' % (numEvents, self.max_events, self.max_events)
                numEvents = self.max_events

            f.seek(current)

            self.timestamps = np.zeros( numEvents )
            self.data       = np.zeros( numEvents )


            for i in range(int(numEvents)):
                self.data[i] = int(f.read(4).encode('hex'), 16)
                self.timestamps[i] = int(f.read(4).encode('hex'), 16)

            return self

    def save(self, filename, data, ts):
        with open(filename, 'w') as f:
            for item in self.header:
                f.write(item)
            print
            print
            no_items = len(data)
            for i in range(no_items):
                f.write(hex(int(data[i]))[2:].zfill(8).decode('hex'))
                f.write(hex(int(ts[i]))[2:].zfill(8).decode('hex'))

    def unpackData(self, data):
        noData = len(data)
        
        x = np.zeros(noData)
        y = np.zeros(noData)
        t = np.zeros(noData)

        for i in range(noData):

            d = int(data[i])

            t[i] = d & 0x1          
            x[i] = 128-((d >> 0x1) & 0x7F)
            y[i] = (d >> 0x8) & 0x7F
        return (x,y,t)

    def packData(self, x,y,t):
        noData = len(x)

        packed = np.zeros(noData)

        for i in range(noData):
            packed[i] =  (int(t[i]) & 0x1)
            packed[i] += (int(128-x[i]) & 0x7F) << 0x1
            packed[i] += (int(y[i]) & 0x7F) << 0x8

        return packed


    def makeSparse(self, data, ts, ratio):
        indexes = np.random.randint(0,len(data),math.floor(len(data)/ratio))
        indexes.sort()
        return data[indexes], ts[indexes]

    def interactiveAnimation(self,x,y,t,step=5000,limits=(0,128),pause=0):
        plt.ion()
        fig = plt.figure(figsize=(6,6))
        plt.show()

        ax = fig.add_subplot(111)
        ax.set_xlim(limits)
        ax.set_ylim(limits)

        start = 0;
        end = step-1;
        ax.scatter(x[start:end],y[start:end],s=20,c=t[start:end], marker = 'o', cmap = cm.jet );

        while(start < len(x)):
            time.sleep(pause)
            ax.clear()
            ax.set_xlim(limits)
            ax.set_ylim(limits)
            ax.scatter(x[start:end],y[start:end],s=20,c=t[start:end], marker = 'o', cmap = cm.jet );
            start = start + step;
            end   = end   + step;
            plt.draw()


    def convertTo16x16(self,x,y,t):
        new_x = np.floor(x/8)
        new_y = np.floor(y/8)
        return (new_x, new_y, t)

    def makeImgMatrix(self,x,y,t,dim=(128,128)):
        image = np.zeros(dim)
        events= np.zeros(dim)

        for i in range(len(x)):
            image[y[i]-1,x[i]-1]  -= t[i]-0.5
            events[y[i]-1,x[i]-1] += 1

        # http://stackoverflow.com/questions/26248654/numpy-return-0-with-divide-by-zero
        np.seterr(divide='ignore', invalid='ignore')
        
        result = 0.5+(image / events)
        result[events == 0] = 0.5
        return result
        
        # np.set_printoptions(threshold='nan')
        # from pprint import pprint
        # pprint(image)

    def saveAsPngs(self,x,y,t,prepend,path="",step=3000,dim=(128,128)):
        # im = Image.fromarray(A)
        # im.save("your_file.jpeg")

        if not os.path.exists(path):
            os.makedirs(path)

        idx = 0
        start = 0;
        end = step-1;
        while(start < len(x)):
            image = self.makeImgMatrix(x[start:end],y[start:end],t[start:end], dim=dim)
            img_arr = (image*255).astype('uint8')
            im = Image.fromarray(img_arr)
            im.save(path+'/'+prepend+("%05d" % idx)+".png")
            idx += 1

            # plt.imshow(self.makeImgMatrix(x[start:end],y[start:end],t[start:end]), cmap = cm.Greys_r)
            # plt.savefig(path+prepend+("%05d" % idx)+".png", transparent=True)
            start = start + step;
            end   = end   + step;


    # def betterAnimation(self,data,step=5000):
        # start = 0;
        # step = 5000;
        # end = step-1;

        # fig, ax = plt.subplots()
        # ax.set_xlim(0,128)
        # ax.set_ylim(0,128)

        # scatt = ax.scatter(x[start:end],y[start:end],s=20,c=t[start:end], marker = 'o', cmap = cm.jet );

        # def update(data):

        #   # scatt.set_color(c=data)
        #   scatt.set_offsets(data)

        #   # start = start + 5000;
        #   # end   = end   + 5000;
        #   # line.set_ydata(data)
        #   return scatt

        # def data_gen():
        #   start = 0;
        #   step = 5000;
        #   end = step-1;
        #   while True: 
        #       data = (x[start:end],y[start:end])
        #       start = start + 5000;
        #       end   = end   + 5000;
        #       yield data
        #        # 128*np.random.rand(5000,1)

        # ani = animation.FuncAnimation(fig, update, data_gen, interval=100)
        # plt.show()


