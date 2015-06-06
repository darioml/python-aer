import paer

data = paer.aedata(paer.aefile('/Users/darioml/src/fyp-aedata-matlab/left_to_right_1.aedat', max_events=1000000))

data = data.make_sparse(64).downsample((16,16))
data.interactive_animation(step=1000,limits=(0,16))