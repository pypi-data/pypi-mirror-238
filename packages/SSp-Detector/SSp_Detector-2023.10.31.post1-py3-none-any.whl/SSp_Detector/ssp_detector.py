# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Copyright (c) 2023. Simon J. Guillot. All rights reserved.                            +
#  Redistribution and use in source and binary forms, with or without modification, are strictly prohibited.
#                                                                                        +
#  THIS CODE IS PROVIDED BY THE COPYRIGHT HOLDER "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING,
#  BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
#  IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
#  OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
#  STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS CODE,
#  EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import logging
import os
import mne
import glob
import scipy
import numpy as np
from scipy import signal
from mne.filter import filter_data
from scipy.interpolate import interp1d


LOGGING_TYPES=dict(DEBUG=logging.DEBUG,
                     INFO=logging.INFO,
                     WARNING=logging.WARNING,
                     ERROR=logging.ERROR,
                     CRITICAL=logging.CRITICAL,
                     )

def spindles_abs(raw,sf,thresh={'abs_pow':1.25})->int:
	"""Detects sleep spindles using absolute Sigma power.

	Notes
	----------
	If you use this toolbox, please cite as followed:

	* Simon J Guillot, Sleep Spindles Detector toolbox (version "build_number", https://github.com/sjg2203/) in Python.

	We provide below some key points on the toolbox.

	If you have any questions, feel free to reach out on `GitHub <https://github.com/sjg2203/>`_.

	Example
	----------
	>>> import mne
	>>> import numpy as np
	>>> from scipy import signal
	>>> from mne.filter import filter_data
	>>> from SSp_Detector import spindles_abs
	>>> from scipy.interpolate import interp1d
	>>> #Load an EDF file using MNE
	>>> raw=mne.io.read_raw_edf("myfile.edf",preload=True)
	>>> sfreq=raw.info['sfreq']
	>>> #Return sleep spindles count into an array
	>>> spindles_abs(raw,sf=sfreq,thresh={'abs_pow':1.25})

	Parameters
	----------
	raw : :py:class:`mne.io.BaseRaw`
		An MNE Raw instance.
	sf : float
		Sampling frequency in Hz.
	thresh : dict, optional
		Detection thresholds:
		``'abs_pow'``: Absolute Sigma power (=power ratio freq_sigma/freq_broad; 1.25).

		If None is given, ``'abs_pow'``:0.2 automatically.

	Returns
	-------
	int
		count of sleep spindles using absolute Sigma power.
	"""

	if 'abs_pow' not in thresh.keys():
		thresh['abs_pow']=1.25
	#If the sf<100Hz, then data will be resampled to meet the 100Hz requirement
	if sf<100:
		raw=raw.resample(100)
		#raw_data=raw_data.get_data()[0]*1000000
		sf=float(100)
	freq_broad=[1,30]
	raw=raw.get_data()[0]*1000000
	data=filter_data(raw,sf,freq_broad[0],freq_broad[1],method='fir',verbose=0)  #Apply a low and high bandpass filter
	data_sigma=data.copy()
	N=20  #N order for the filter
	nyquist=sf/2
	Wn=11/nyquist
	sos=signal.iirfilter(N,Wn,btype='Highpass',output='sos')
	data_sigma=signal.sosfiltfilt(sos,data_sigma)
	Wn=16/nyquist
	sos=signal.iirfilter(N,Wn,btype='lowpass',output='sos')
	data_sigma=signal.sosfiltfilt(sos,data_sigma)
	duration=0.3
	halfduration=duration/2
	total_duration=len(data_sigma)/sf
	last=len(data_sigma)-1
	step=0.1
	len_out=int(len(data_sigma)/(step*sf))
	out=np.zeros(len_out)
	tt=np.zeros(len_out)
	for i,j in enumerate(np.arange(0,total_duration,step)):
		beg=max(0,int((j-halfduration)*sf))
		end=min(last,int((j+halfduration)*sf))
		tt[i]=(np.column_stack((beg,end)).mean(1)/sf)
		out[i]=np.mean(np.square(data_sigma[beg:end]))
	dat_det_w=out
	dat_det_w[dat_det_w<=0]=0.000000001
	abs_sig_pow=np.log10(dat_det_w)
	interop=interp1d(tt,abs_sig_pow,kind='cubic',bounds_error=False,fill_value=0,assume_sorted=True)
	tt=np.arange(data_sigma.size)/sf
	abs_sig_pow=interop(tt)
	#Count of sleep spindles using absolute sigma power
	text='spindles'
	spindles_count_abs_pow={}
	name=0
	for item in abs_sig_pow:
		if item>=thresh['abs_pow']:
			spindles_count_abs_pow['item'+str(name)]=[item]
		else:
			name+=1
	if len(spindles_count_abs_pow)==1:
		text='spindle'
	spindles_abs_count=len(spindles_count_abs_pow)
	print('Using absolute Sigma power:',spindles_abs_count,text)
	return spindles_abs_count

def spindles_rel(raw,sf,thresh={'rel_pow':0.2})->int:
	"""Detects sleep spindles using relative Sigma power.

	Notes
	----------
	If you use this toolbox, please cite as followed:

	* Simon J Guillot, Sleep Spindles Detector toolbox (version "build_number", https://github.com/sjg2203/) in Python.

	We provide below some key points on the toolbox.

	If you have any questions, feel free to reach out on `GitHub <https://github.com/sjg2203/>`_.

	Example
	----------
	>>> import mne
	>>> import numpy as np
	>>> from scipy import signal
	>>> from mne.filter import filter_data
	>>> from SSp_Detector import spindles_rel
	>>> from scipy.interpolate import interp1d
	>>> #Load an EDF file using MNE
	>>> raw=mne.io.read_raw_edf("myfile.edf",preload=True)
	>>> sfreq=raw.info['sfreq']
	>>> #Return sleep spindles count into an array
	>>> spindles_abs(raw,sf=sfreq,thresh={'rel_pow':0.2})

	Parameters
	----------
	raw : :py:class:`mne.io.BaseRaw`
		An MNE Raw instance.
	sf : float
		Sampling frequency in Hz.
	thresh : dict, optional
		Detection thresholds:
		``'rel_pow'``: Relative Sigma power (=power ratio freq_sigma/freq_broad; 0.2).

		If None is given, ``'rel_pow'``:0.2 automatically.

	Returns
	-------
	int
		count of sleep spindles using relative Sigma power.
	"""

	if 'rel_pow' not in thresh.keys():
		thresh['rel_pow']=0.2
	#If the sf<100Hz, then data will be resampled to meet the 100Hz requirement
	if sf<100:
		raw=raw.resample(100)
		#raw_data=raw_data.get_data()[0]*1000000
		sf=float(100)
	freq_broad=[1,30]
	raw=raw.get_data()[0]*1000000
	data=filter_data(raw,sf,freq_broad[0],freq_broad[1],method='fir',verbose=0)  #Apply a low and high bandpass filter
	f,t,SXX=signal.stft(data,sf,nperseg=int((2*sf)),noverlap=int(((2*sf)-(0.2*sf))))  #Using STFT to compute the point-wise relative power
	idx_band=np.logical_and(f>=freq_broad[0],f<=freq_broad[1])  #Keeping only the frequency of interest and Interpolating
	f=f[idx_band]
	SXX=SXX[idx_band,:]
	SXX=np.square(np.abs(SXX))
	sum_pow=SXX.sum(0).reshape(1,-1)
	np.divide(SXX,sum_pow,out=SXX)
	idx_sigma=np.logical_and(f>=11,f<=16)  #Extracting the relative sigma power
	rel_power=SXX[idx_sigma].sum(0)
	#Count of sleep spindles using relative sigma power
	text='spindles'
	spindles_count_rel_pow={}
	name=0
	for item in rel_power:
		if item>=thresh['rel_pow']:
			spindles_count_rel_pow['item'+str(name)]=[item]
		else:
			name+=1
	if len(spindles_count_rel_pow)==1:
		text='spindle'
	spindles_rel_count=len(spindles_count_rel_pow)
	print('Using relative Sigma power:',spindles_rel_count,text)
	return spindles_rel_count
