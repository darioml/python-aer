import paer

file = '../fyp-aedata-matlab/left_to_right_1.aedat'

lib = paer.aefile(file, max_events=750001)
data = paer.aedata(lib)

sparse = data[300000:750000].make_sparse(64).downsample((16,16))

sparse.save_to_mat('downsample_left_to_right_1_1.mat')
lib.save(sparse, 'downsample_left_to_right_1_1.aedat')
