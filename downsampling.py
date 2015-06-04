from pAER import pAER
import scipy.io as io

file = '../fyp-aedata-matlab/left_to_right_1.aedat'

lib = pAER(file, max_events=750001)

(sparse_data, sparse_ts) = lib.makeSparse(lib.data[300000:750000], lib.timestamps[300000:750000], 64)

(x,y,z) = lib.unpackData(sparse_data)
(x16,y16,t16) = lib.convertTo16x16(x,y,z)
p_data = lib.packData(x16,y16,t16)

io.savemat('downsample_left_to_right_1_1.mat', {'X':x16, 'Y':y16, 't': t16, 'ts': sparse_ts})
lib.save('downsample_left_to_right_1_1.aedat', p_data, sparse_ts)


# (x16,y16,t16) = lib.convertTo16x16(x,y,z)


