from pAER import pAER
from os import listdir
from os.path import isfile, join
from pprint import pprint

# hello = pAER('/Users/darioml/src/fyp-aedata-matlab/left_to_right_1.aedat', max_events=1000000)

# data = hello.makeSparse(hello.data, 64)
# (x,y,t) = hello.unpackData(data)

# (x16,y16,t) = hello.convertTo16x16(x,y,t)
# hello.interactiveAnimation(x,y,t,step=1200,limits=(0,128),pause=1)


#
# hello = pAER('/Users/darioml/src/fyp-aedata-matlab/left_to_right_1.aedat', max_events=300000)
#
# data = hello.makeSparse(hello.data, 1)
# # data = hello.data
#
# (x,y,t)     = hello.unpackData(data)
# (x16,y16,t16) = hello.convertTo16x16(x,y,t)
#
# #hello.interactiveAnimation(x,y,t,step=1000,limits=(0,128),pause=1)
#
#
# # plt.imshow(hello.makeImgMatrix(x[0:999],y[0:999],t[0:999]), cmap = cm.Greys_r)
# # plt.show()
#
# # plt.imshow(hello.makeImgMatrix(x[100000:100999],y[100000:100999],t[100000:100999]), cmap = cm.Greys_r)
# # plt.show()
#
# hello.saveAsPngs(x16,y16,t16,'results/l_2_r_16x16_',step=3000, dim=(16,16))
#
# # Let's generate pngs for all the data now.

mypath = '../fyp-aedata-matlab'
onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) and f.endswith('.aedat')]

for file in onlyfiles:
    lib = pAER('/Users/darioml/src/fyp-aedata-matlab/' + str(file))
    (x,y,z) = lib.unpackData(lib.data)
    (x16,y16,t16) = lib.convertTo16x16(x,y,z)

    lib.saveAsPngs(x16,y16,t16,'16x16_' + str(file) + '_',path='results_all',step=3000, dim=(16,16))


