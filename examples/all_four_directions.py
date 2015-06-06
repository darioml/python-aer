import paer
import numpy as np

base_dir = '/path/to/some/dir/'
file1 = 'left_to_right_1.aedat'
file2 = 'right_to_left_1.aedat'
file3 = 'top_to_bottom_1.aedat'
file4 = 'bottom_to_top_1.aedat'

# Each ball movement should be .5s long
animation_time = 0.2

# 3,280 events per second for 16*16 is reasonable for ball movement (might be even too high!)
num_events_p_s = 3280

# Helper function to read a file. Given (min,max) which are data ranges for extraction, this will return a cropped and
#  suitably sparse output.
def get_data(file, min, max, animation_time=animation_time, num_events=num_events_p_s*animation_time, offset=0):
    aefile = paer.aefile(file, max_events=max+1)
    aedata = paer.aedata(aefile)
    print 'Points: %i, Time: %0.2f. Sparsity: %i' % (len(aefile.data), (aefile.timestamp[-1]-aefile.timestamp[0])/1000000,
                                                  np.floor(len(aefile.data)/num_events))

    sparse = aedata[min:max].make_sparse(np.floor(len(aefile.data)/num_events))

    actual_time = (sparse.ts[-1]-sparse.ts[0])/1000000
    scale = actual_time/animation_time
    sparse.ts = (offset * 1000000) + np.round((sparse.ts-sparse.ts[0])/scale)
    # print sparse_ts[0], sparse_ts[-1], sparse_ts[-1]-sparse_ts[0], (sparse_ts[-1]-sparse_ts[0])/1000000

    return sparse

# Loop through all files - indexes are extrapolated.
d1 = get_data(file1, 300000, 750000, offset=0*animation_time)
d2 = get_data(file2, 300000, 600000, offset=1*animation_time)
d3 = get_data(file3,  85000, 140000, offset=2*animation_time)
d4 = get_data(file4,  65200, 131800, offset=3*animation_time)

# Need to pre-load a file, to get the correct headers when writing!
lib = paer.aefile(file1, max_events=1)

final = paer.concatenate( (d1,d2,d3,d4) )
final_16 = final.downsample((16,16))

lib.save(final, 'test.aedat')
lib.save(final_16, 'test_16.aedat')

d1.save_to_mat('test_1.mat')
d2.save_to_mat('test_2.mat')
d3.save_to_mat('test_3.mat')
d4.save_to_mat('test_4.mat')