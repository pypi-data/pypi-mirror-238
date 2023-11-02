import scipy
from scipy import interpolate
from numba import njit
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from math import pi, sqrt, exp

@njit
def pick_null(event_times, interval, lpad, rpad):
    '''create a selection of times that will be used to construct the null 
    hypothesis. Goal is to avoid the stimulus times.
    Create a list of all the intervals between stimulae exceeding
    the duration of 'interval'. From within these intervals, times are 
    selected. Because I sometimes have a lead in or follow effect 
    around event times, the lpad and rpad will cut off the beginning 
    and end of each interval (respectively) so that these follow on 
    and lead up to firing are omited from the null hypothesis'''
    intrvl_idxs = np.argwhere(np.diff(event_times)>interval).flatten()
    rng_idx = np.arange(2,dtype=np.int_)
    intervals = np.zeros(intrvl_idxs.shape+(2,))
    for ii,idx in enumerate(intrvl_idxs):
        intervals[ii,:]=event_times[idx:idx+2]
    # now push the interval start and end time to the right and left 
    # making a little pad around the preceeding and following event.
    intervals[:,0]+=lpad
    intervals[:,1]-=rpad
    # now decide how many times to pick from each interval
    # based on the weighted average of the duration of the interval
    Nchoice_weight = np.diff(intervals)/np.sum(np.diff(intervals))
    # use ceil to take at least one time from each interval
    Nchoice = np.ceil(Nchoice_weight*len(event_times)).astype(np.int_).flatten()
    null_times = np.zeros(Nchoice.sum())
    _cnt = 0
    for i,(S,E) in enumerate(intervals):
        null_times[_cnt:_cnt+Nchoice[i]] = np.random.uniform(S,E,
                                                             size=Nchoice[i])
        _cnt+=Nchoice[i]
    # truncate the null times so it is the same length as event_times
    return null_times[0:len(event_times)]

# finally worked out the fold spikes function with ~ 500x speed up
# keys is np.searchsorted, very handy!!!
@njit
def fold_spikes(spike_times, stim_times, duration):
    '''create a single large time series, by stacking or folding all the spike
    times around each stimulus, make sure spike times are sorted,
    returns a single sorted array from 0--duration with the times of the
    stacked spikes'''
    Sidxs = np.searchsorted(spike_times,stim_times)
    Eidxs = np.searchsorted(spike_times,stim_times+duration)
    fold_st = np.zeros(np.sum(Eidxs-Sidxs)+2)
    fold_st[0]=0
    fold_st[-1]=duration
    _cnt = 1
    for i in range(len(Sidxs)):
        fold_st[_cnt:_cnt+Eidxs[i]-Sidxs[i]]=spike_times[Sidxs[i]:Eidxs[i]]-stim_times[i]
        _cnt+=Eidxs[i]-Sidxs[i]
    return(np.sort(fold_st))

def mattGum(st,stim_times,null_times,duration,ax=None):
    '''
    wrapper to calculate Gumbel and Pv for spikes based on stimulus times
    and explicitly selected null times. Pick a duration that makes sens
    based on what you see in rasters / data, this matters for sig testing.
    '''
    st = np.sort(st)
    stim_times = np.sort(stim_times)
    fold_st=fold_spikes(st, stim_times, duration)
    ResampN = null_times.shape[0]
    rand_resample = np.empty((ResampN,len(fold_st)))
    rand_resample[:] = np.nan
    for i in range(ResampN):
        fold_null = fold_spikes(st, null_times[i,:], duration)
        fold_cumprob = interpolate.interp1d(
            fold_null,
            np.linspace(0,1,len(fold_null))
        )(fold_st)
        rand_resample[i,:] = fold_cumprob-(fold_st/duration)
    rand_resample-=np.mean(rand_resample,axis=0)
    # this is a bit more complicated then I thought.
    fold_cumprob = interpolate.interp1d(
        np.r_[0,fold_st,duration],
        np.linspace(0,1,len(fold_st)+2)
    )(fold_st)
    fold_diff = fold_cumprob-(fold_st/duration)
    fold_diff_demean = fold_diff-np.mean(fold_diff)
    MaxRandD = np.max(np.abs(rand_resample),0)
    RandMu = np.mean(MaxRandD)
    RandVar = np.var(MaxRandD, ddof=1)
    ZETALoc = np.argmax(np.abs(fold_diff_demean))
    PosD = np.max(np.abs(fold_diff_demean))
    
    # get time and [amp] of stimulus locked peak
    MaxDTime = fold_st[ZETALoc]
    MaxD = (fold_diff_demean)[ZETALoc]
    
    # find peak of inverse sign
    PeakLocInvSign = np.argmax(-np.sign(MaxD)*fold_diff_demean)
    MaxDTimeInvSign = fold_st[PeakLocInvSign]
    D_InvSign = fold_diff_demean[PeakLocInvSign]
    
    #
    print('Python: Gumbel %0.7f, %0.7f, %0.7f' % (RandMu, RandVar, PosD))
    Pvalue, Gumbel = getGumbel(RandMu,RandVar,PosD)
    print(Pvalue, Gumbel)

    if (ax is not None) and (type(ax)==matplotlib.axes._axes.Axes):
        # lets plot
        ax.plot(fold_st,fold_diff_demean)
        ax.plot(MaxDTime,MaxD,'o', mec = 'red', ms = 3, mfc = 'none')
        ax.plot(MaxDTimeInvSign,D_InvSign,'o', mec = 'green',
                mfc = 'none', ms = 3)
        ax.text(0,0.9,"P=%.4f" % (Pvalue), transform = ax.transAxes, size=8)
        # maybe add a line collection for the null hypothesis distribution?
        segs = np.zeros(rand_resample.shape+(2,))
        segs[:,:,0] = np.linspace(0,duration,rand_resample.shape[1]) # plot xs
        segs[:,:,1] = rand_resample # plot ys
        lc = LineCollection(segs,linewidths = 0.2, alpha = 0.5, color = 'black')
        ax.add_collection(lc)

    return (Pvalue, Gumbel), (MaxDTime, MaxD, MaxDTimeInvSign, D_InvSign)

# here is getting the Gumbel, taken directly from Montijn and Heimel
# thanks guys.
def getGumbel(dblE,dblV,dblX):
    """"Calculate p-value and z-score for maximum value of N samples drawn from Gaussian
       [dblP,dblZ] = getGumbel(dblE,dblV,dblX)

        input:
        - dblE: mean of distribution of maximum values
        - dblV: variance of distribution of maximum values
        - dblX: maximum value to express in quantiles of Gumbel

        output:
        - dblP; p-value for dblX (chance that sample originates from distribution given by dblE/dblV)
        - dblZ; z-score corresponding to P

    Version history:
    1.0 - June 17, 2020, Created by Jorrit Montijn translated by Alexander Heimel

    Sources:
    Baglivo (2005), ISBN: 9780898715668
    Elfving (1947), https://doi.org/10.1093/biomet/34.1-2.111
    Royston (1982), DOI: 10.2307/2347982
    https://stats.stackexchange.com/questions/394960/variance-of-normal-order-statistics
    https://stats.stackexchange.com/questions/9001/approximate-order-statistics-for-normal-random-variables
    https://en.wikipedia.org/wiki/Extreme_value_theory
    https://en.wikipedia.org/wiki/Gumbel_distribution
    """

    ## define Gumbel parameters from mean and variance
    #derive beta parameter from variance
    dblBeta = sqrt(6) * sqrt(dblV) / pi

    # define Euler-Mascheroni constant
    dblEulerMascheroni = 0.5772156649015328606065120900824 #vpa(eulergamma)

    # derive mode from mean, beta and E-M constant
    dblMode = dblE - dblBeta * dblEulerMascheroni

    # define Gumbel cdf
    ###    fGumbelCDF = @(x) exp(-exp(-((x(:)-dblMode)./dblBeta)));
    fGumbelCDF = lambda x : exp(-exp(-((x-dblMode) /dblBeta)))

    ## calculate output variables
    # calculate cum dens at X
    dblGumbelCDF = fGumbelCDF(dblX)
    # define p-value
    dblP = 1-dblGumbelCDF
    # transform to output z-score
    ### dblZ = -norminv(dblP/2);
    dblZ = -scipy.stats.norm.ppf(dblP/2)

    # approximation for large X
    ### dblP[isinf(dblZ)] = exp( (dblMode-dblX(isinf(dblZ)))./dblBeta ) ;
    if dblZ>1E30:
        dblP = exp( (dblMode-dblX) / dblBeta )
    # transform to output z-score
    ### dblZ = -norminv(dblP/2);
    dblZ = -scipy.stats.norm.ppf(dblP/2)

    return dblP,dblZ

# sample use:
if __name__=='__main__':
    st = np.random.uniform(0,1000,10000)
    stim_times = np.random.uniform(100,900,100)
    f,ax = plt.subplots(1,1)
    # make sure the s
    NNullReps = 100
    null_times = np.array([pick_null(stim_times,10,2,2) for _ in range(NNullReps)])
    mattGum(st, stim_times, null_times, 5,ax=ax)
