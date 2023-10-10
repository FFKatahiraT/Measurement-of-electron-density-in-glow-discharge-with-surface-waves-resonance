import matplotlib.pyplot as plt
from os import walk
import math

class PeakProperties():
	def __init__(self, lmb, A, E, g, dn_12_sqr=0):
		self.lmb = lmb
		self.g = g
		self.A = A
		self.E = E
		self.I = 0	#Intensity
		self.index = 0 #peak index
		self.dn_12_sqr = dn_12_sqr #n1^2-n2^2
		self.dlmb = 6.8	#A
	
	def calcNe(self, Te):
		if self.dn_12_sqr == 0: return 0
		k_B_const = 1.38e-23
		Te = Te*11600 #K
		e_const = 1.6e-19
		eps_const = 8.85e-12
		Zp = 1
		Ze = 80
		dNe = (eps_const*k_B_const*Te/(4*3.14*e_const**2))**0.5	#Debay radius * Ne**0.5
		eps = 0.1
		NeMax = 1e20
		NeMin = 1e16
		Ne = 1e16 #1/m**3
		calculated_dlmb = 1
		
		while abs(calculated_dlmb-self.dlmb) > eps:
			if calculated_dlmb > self.dlmb:
				NeMax = Ne
				Ne = (Ne+NeMin)/2
			else:
				NeMin = Ne
				Ne = (Ne+NeMax)/2
			ND = 4/3*3.14*(dNe/Ne**0.5)**3*Ne
			calculated_dlmb = 8.16e-19*(self.lmb*10)**2*Ne**(0.67)*(1-0.7*ND**(-0.33))*self.dn_12_sqr*Zp**(0.33)/Ze
		
		# print(calculated_dlmb, " calculated_dlmb")
		# print(dNe/Ne**0.5, " Debay radius")
		print(Ne, " calculated_Ne")
		return Ne
			

def read_data(name):
	file = open(name, 'r')
	data = file.read().split('\n')
	r, val = [], []
	for line in data[7:]:
		if line!='' and line[0]!='%':
			r_temp, val_temp = line[1:-1].split('","')
			r.append(float(r_temp.replace(",",".")))
			val.append(float(val_temp.replace(",",".")))
	return r, val

def del_offset(val):
	minVal = min(val)
	for i in range(len(val)):
		val[i] -= minVal
	return val

def find_peaks(r, val):
	val_temp = val[:]
	for i in range(len(val)):
		if val[i]<400:	val_temp[i] = 0

	derivative = []
	peaks = []
	for i in range(len(val_temp[:-1])):
		derivative.append(val_temp[i+1]-val_temp[i])

	for i in range(len(derivative)):
		if derivative[i]>0 and derivative[i+1]<0:
			peak_tmp = find_nearest_peak(r[i+1])
			if peak_tmp != None:
				peaks.append(peak_tmp)
				peaks[-1].I = val[i+1]
				peaks[-1].index = i+1

	return peaks

def find_nearest_peak(wavelength):
	delta = 10
	peak = None
	for i in range(len(AllPeaks)):
		diff = abs(wavelength - AllPeaks[i].lmb)
		if diff < delta and diff<10:
			delta = diff
			peak = AllPeaks[i]
	return peak

def FindNe(peaks, Te):
	NeSum = 0
	i = 0
	for peak in peaks:
		if peak.dn_12_sqr != 0:
			NeSum += peak.calcNe(Te)
			i+=1

	return NeSum/i

def calcTe(peaks):
	temperatures = []
	for l in range(len(peaks)):
		for j in range(len(peaks)):
			if j==l: continue
			if (j==1 and l==3) or (j==3 and l==1): continue

			dE = peaks[j].E - peaks[l].E
			alpha = (peaks[j].I/peaks[l].I * peaks[l].g/peaks[j].g * 
				peaks[l].A/peaks[j].A * peaks[j].lmb/peaks[l].lmb)

			if alpha!=0 and alpha!=1: 
				Te_temp = -dE/math.log(alpha)
				if Te_temp > 0:	
					temperatures.append(Te_temp*1.23981e-4)	#eV
					print(Te_temp, peaks[j].lmb, peaks[l].lmb)

	if len(temperatures) == 0: return 0
	Te_av = sum(temperatures)/len(temperatures)
	return Te_av

def plotter(x, y, xPeaks, yPeaks, xLabel, yLabel, name):
	plt.rcParams.update({'font.size': 14})
	plt.plot(x, y)
	plt.scatter(xPeaks, yPeaks)
	# plt.legend(loc='best')
	plt.grid()
	plt.ylabel(yLabel)
	plt.xlabel(xLabel)
	plt.title(name[:-4])
	plt.tight_layout()
	# plt.show()
	plt.savefig("Images/"+name[:-4]+'.svg')
	plt.close()


def processing(directory, name, yLabel):
	r, val = read_data(directory+name)
	val = del_offset(val)
	peaks = find_peaks(r, val)
	Te = calcTe(peaks)
	# Ne = FindNe(peaks, Te)

	xPeaks, yPeaks = [], []
	for peak in peaks:
		xPeaks.append(r[peak.index])
		yPeaks.append(peak.I)

	print(name)
	print(Te, "Te [eV]")
	# print(Ne, "Ne [1/m^3]")
	print()
	plotter(r, val, xPeaks, yPeaks, 'wavelength [nm]',yLabel, name)

# names = ["spec_Hg_primary.csv"]
# names = ["spec_Hg2 (2 sm,0 grad).csv","spec_Hg2 (2 sm,90 grad).csv",
# 	"spec_Hg2 (2 sm,180 grad).csv", "spec_Hg2 (2 sm,270 grad).csv",
# 	"spec_Hg2 (5 sm,0 grad).csv","spec_Hg2 (5 sm,90 grad).csv",
# 	"spec_Hg2 (5 sm,180 grad).csv", "spec_Hg2 (5 sm,270 grad).csv",
# 	"spec_Hg2 (8 sm,0 grad).csv","spec_Hg2 (8 sm,90 grad).csv",
# 	"spec_Hg2 (8 sm,180 grad).csv", "spec_Hg2 (8 sm,270 grad).csv",
# 	"spec_Hg2 (11 sm).csv","spec_Hg2 (14 sm,180 grad).csv",
# 	"spec_Hg2 (17 sm).csv", "spec_Hg2 (17 sm, 5mm from centre).csv",
# 	"spec_Hg2 (17 sm, 10mm from centre).csv", "spec_Hg2 (17 sm, centre, 0).csv",
# 	]
# directory = "Spec_Hg2/"

# names = ['009,602V_2.csv', '010, 514V_2.csv', '011, 445V_2.csv',
# '012, 381V_2.csv', '013, 316V_2.csv', '014, 241V_2.csv',
# '015, 181V_2.csv', '016, 124V_2.csv', '017, 67V_2.csv', ]

directory = "Spectrum_exp3/data/"
names = next(walk(directory), (None, None, []))[2]  
AllPeaks = []
AllPeaks.append(PeakProperties(253.65210, 8.40e+06, 39412.237, 3))	#5d106s6p --> 5d106s2
AllPeaks.append(PeakProperties(365.48420, 1.84e+07, 71396.073, 5))	#5d106s6d --> 5d106s6p 
# AllPeaks.append(PeakProperties(404.7740, 3.0e+05, 135302.600, 8, dn_12_sqr=7**2-6**2)) #5d106s7s --> 5d106s6p
AllPeaks.append(PeakProperties(435.83350, 5.6e+07, 62350.325, 3, dn_12_sqr=7**2-6**2)) #5d106s7s --> 5d106s6p
# AllPeaks.append(PeakProperties(546.07500, 4.9e+07, 62350.325 , 3, dn_12_sqr=7**2-6**2)) #5d106s7s --> 5d106s6p

for name in names:
	processing(directory, name, r'Intensity')
# processing('H_f.txt', r'Magnetic field strength [A/m]')
# processing('nu_c_omega_p.txt', r'$\nu_c/\omega_p$ [A/m]')
# processing('Te(f).txt', r'Electron temperature [$eV$]')
# processing('T(f).txt', r'Temperature [$K$]')