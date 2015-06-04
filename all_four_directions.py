from pAER import pAER
import numpy as np

file1 = '../fyp-aedata-matlab/left_to_right_1.aedat'
file2 = '../fyp-aedata-matlab/right_to_left_1.aedat'
file3 = '../fyp-aedata-matlab/top_to_bottom_1.aedat'
file4 = '../fyp-aedata-matlab/bottom_to_top_1.aedat'

# Each ball movement should be .5s long
animation_time = 0.5

# 3,280 events per second for 16*16 is reasonable for ball movement (might be even too high!)
num_events_p_s = 3280

# Helper function to read a file. Given (min,max) which are data ranges for extraction, this will return a cropped and
#  suitably sparse output.
def get_data(file, min, max, animation_time=animation_time, num_events=num_events_p_s*animation_time, offset=0):
    lib = pAER(file, max_events=max+1)
    print 'Points: %i, Time: %0.2f. Sparsity: %i' % (len(lib.data), (lib.timestamps[-1]-lib.timestamps[0])/1000000,
                                                  np.floor(len(lib.data)/num_events))

    (sparse_data, sparse_ts) = lib.makeSparse(lib.data[min:max], lib.timestamps[min:max], np.floor(len(lib.data)/num_events))

    actual_time = (sparse_ts[-1]-sparse_ts[0])/1000000
    scale = actual_time/animation_time
    sparse_ts = (offset * 1000000) + np.round((sparse_ts-sparse_ts[0])/scale)
    # print sparse_ts[0], sparse_ts[-1], sparse_ts[-1]-sparse_ts[0], (sparse_ts[-1]-sparse_ts[0])/1000000

    return sparse_data, sparse_ts

# Loop through all files - indexes are extrapolated.
(d_1,t_1) = get_data(file1, 300000, 750000, offset=0*animation_time)
(d_2,t_2) = get_data(file2, 300000, 600000, offset=1*animation_time)
(d_3,t_3) = get_data(file3,  85000, 140000, offset=2*animation_time)
(d_4,t_4) = get_data(file4,  65200, 131800, offset=3*animation_time)

# This library is badly written, hence the need to do this...
lib = pAER(file1, max_events=1)

# concatenate results
final_data = np.concatenate((d_1,d_2,d_3,d_4))
final_ts = np.concatenate((t_1,t_2,t_3,t_4))

# reduce to 16*16
(x,y,z) = lib.unpackData(final_data)
(x,y,z) = lib.convertTo16x16(x,y,z)
data_16_16 = lib.packData(x,y,z)

# save!
lib.save('all_directions.aedat', data_16_16, final_ts)