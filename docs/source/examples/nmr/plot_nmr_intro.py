# coding: utf-8
"""
Introduction to NMR processing
===========================================

Here we explain how to display and perform basic processing of NMR file

"""

from spectrochempy.api import *
import os


##########################################################
#
# Here we import two dataset, one is 1D and the other is 2D
# 
# Because , we will sometimes need to recall the original dataset, we create to getting functions

##########################################################
# 1D dataset getting function
# ---------------------------

def get_source1D():
    source1D = NDDataset()
    path = os.path.join(data, 'nmrdata', 'bruker', 'tests', 'nmr', 'bruker_1d')
    source1D.read_bruker_nmr(path, expno=1, remove_digital_filter=True)
    return source1D


##########################################################
# 2D dataset getting function
# ---------------------------

def get_source2D():
    source2D = NDDataset()
    path = os.path.join(data, 'nmrdata', 'bruker', 'tests', 'nmr', 'bruker_2d')
    source2D.read_bruker_nmr(path, expno=1, remove_digital_filter=True)
    return source2D


##########################################################
# get the 1D source
# -----------------
source1D = get_source1D()
source1D

##########################################################
# get the 2D source
source2D = get_source2D()
source2D

##########################################################
# Plot the 1D dataset raw data

figure()

# plot the real data
source1D.plot(xlim=(0, 25000), style='paper')
# `hold=True` to make that the following plot commands will be on the same graph

# plot the imaginary data on the same plot
source1D.plot(imag=True, data_only=True)
# `data_only=True` to plot only the additional data, without updating the figure setting
# such as xlim and so on.
show()

##########################################################
# To display the imaginary part, one can also simply use the show_complex commands.


figure()  # this is necessary to create a new figure
# and so avoid that the output of the next command
# is displayed on the previous figure

ax = source1D.plot(show_complex=True, color='green',
                   xlim=(0., 20000.), zlim=(-2., 2.))

show()

###############################@@
# Plot the 2D dataset raw data

figure()
source2D = get_source2D()
ax = source2D.plot(xlim=(0., 25000.))
show()

##############################
# probably less util, but multiple display is also possible for 2D

figure()
source2D.plot()
ax = source2D.plot(imag=True, cmap='jet', data_only=True)
show()

#################
# Apodization

figure()  # again becessary

source1D = get_source1D()  # restore original
p = source1D.plot()

# create the apodized dataset
lb_source = source1D.em(lb=100. * ur.Hz)

p = lb_source.plot(xlim=(0, 25000), zlim=(-2, 2))

t = p.text(12500, 1.70, 'Dual display (original & apodized fids)', ha='center',
           fontsize=16)

show()

############################
# Note that the apodized dataset actually replace the original data
# check that both dataset are the same
lb_source is source1D  # note here, that the original data are modified by default
# when applying apodization function.
# Use the `inplace` keyword to modify this behavior

#################################
# If we want to avoid this behavior and create a new dataset instead, we use the `inplace` flag.

source1D = get_source1D()

lb2_source = source1D.em(lb=100. * ur.Hz, inplace=False)

# check that both dataset are different
lb2_source is not source1D

###############################################
# We can also get only the apodization function

figure()  # again necessary to start a new figure

source1D = get_source1D()  # restore original
p = source1D.plot()

show()

################################################
# create the apodized dataset (if apply is False, the apodization function is not applied to the dataset,
# but returned)

figure()

apodfunc = source1D.em(lb=100. * ur.Hz, apply=False)

p = apodfunc.plot(xlim=(0, 25000), zlim=(-2, 2))

source1D.em(lb=100. * ur.Hz, apply=True)
p = source1D.plot(data_only=True)

t = p.text(12500, 1.70,
           'Multiple display (original & em apodized fids + apod.function)',
           ha='center', fontsize=14)
show()

######################################
# Apodization function can be em, gm, sp ...

figure()  # again necessary to start a new figure

source1D = get_source1D()  # restore original
p = source1D.plot()

LB = 50. * ur.Hz
GB = 100. * ur.Hz
apodfunc = source1D.gm(gb=GB, lb=LB, apply=False)

p = apodfunc.plot(xlim=(0, 25000), zlim=(-2, 2))

source1D.gm(gb=GB, lb=LB)  # apply=True by default
p = source1D.plot(data_only=True)

t = p.text(12500, 1.70,
           'Multiple display (original & gm apodized fids + apod.function)',
           ha='center', fontsize=14)

show()

# **TODO**: sp function

################################################
# Apodization of 2D data

figure()

source2D = get_source2D()
ax = source2D.plot(xlim=(0., 25000.))

LB = 20. * ur.Hz
source2D.em(lb=LB)
source2D.em(lb=LB / 2, axis=0)
ax = source2D.plot(data_only=True, cmap='copper')

show()

################################################
# Time-frequency trasforms : FFT

figure()

source1D = get_source1D()  # restore original
LB = 10. * ur.Hz
source1D.em(lb=LB)
source1D.zf_auto(inplace=True)
transf1 = source1D.fft()  # by defauut fft create a new dataset

source1D = get_source1D()  # restore original
LB = 10. * ur.Hz
GB = 50. * ur.Hz
source1D.gm(gb=GB, lb=LB)
source1D.zf_auto()
transf2 = source1D.fft()

transf1.plot()
p = transf2.plot()
t = p.text(12500, 1.70, 'fft transform after em or gm broadening', ha='center',
           fontsize=14)
show()



