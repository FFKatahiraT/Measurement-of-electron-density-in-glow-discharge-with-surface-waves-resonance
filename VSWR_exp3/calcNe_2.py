import numpy as np
import matplotlib.pyplot as plt

def read_data(name):
	file = open(name, 'r')
	data = file.read().split('\n')
	Freq, Rs, Xs = [], [], []
	for line in data:
		if line!='' and line[0]!='"':
			split_char = line.index(',')
			Freq_temp, Rs_temp, Xs_temp = line.split(',')
			Freq.append(float(Freq_temp))
			Rs.append(float(Rs_temp))
			Xs.append(float(Xs_temp))
	return Freq, Rs, Xs

def calcNe(length, f):
	epsilon = (length / (c/f - l_met))**2	#epsilon = (1 - (l_met - length)/(c/f))**2
	print(epsilon, "epsilon", length, "length", f, "f")
	return eps0_const*me_const/e_const**2*(1-epsilon)*(6.28*f)**2

def plotter(r_list, Func_list, xLabel, yLabel, name, Label=[""], ylog=False):
	plt.rcParams.update({'font.size': 14})
	for i in range(len(Func_list)):
		plt.plot(r_list, Func_list[i], label=Label[i])
	# plt.scatter(r_list[i], Func_list[i], label=Label[i], marker=pointstyle[i])
	if Label[0]!="": plt.legend(loc="best")
	plt.grid()
	if ylog: plt.yscale("log") 
	plt.ylabel(yLabel)
	plt.xlabel(xLabel)
	plt.tight_layout()
	plt.savefig("plots/"+name[:-4]+'.svg')
	# plt.show()
	plt.close()

def processing(name, length):
	Freq, Rs, Xs = read_data("raw/"+name)
	Zs = 50 #Ohm source impedance
	VSWR, absXs = [], []
	for i in range(len(Xs)):
		Gamma = ((Rs[i]-Zs)**2+Xs[i]**2)**0.5/((Rs[i]+Zs)**2+Xs[i]**2)**0.5#abs(50**2-(Rs[i]**2-Xs[i]**2))**0.5+1
		if Gamma>99/101: Gamma=99/101
		VSWR_temp = (1+Gamma)/(1-Gamma)		
		VSWR.append(VSWR_temp)
	
	for i in range(len(Xs)*2//3):
		absXs.append(abs(Xs[i]))

	minXsIndex = absXs.index(min(absXs))
	minVSWRIndex = VSWR.index(min(VSWR))
	plotter(Freq, [VSWR], 'Freq [MHz]',"VSWR", "VSWR"+name, ylog=True)
	return calcNe(length, Freq[minVSWRIndex]*1e6)


names = ["sark_009.csv", 
	"sark_010.csv", "sark_011.csv", 
	"sark_012.csv", "sark_013.csv", 
	"sark_014.csv", "sark_015.csv", 
	"sark_016.csv", 

	"sark_020.csv", "sark_021.csv", 
	"sark_022.csv", "sark_023.csv", 
	"sark_024.csv", "sark_025.csv", 
	"sark_026.csv", "sark_027.csv", 
	
	"sark_030.csv", "sark_031.csv", 
	"sark_032.csv", "sark_023.csv", 
	"sark_034.csv", "sark_035.csv", 
	"sark_036.csv", "sark_037.csv", ]
names.reverse()

VR = [573,509,439,368,306,230,175,117,
	585,515,448,380,321,246,188,123,
	596,515,444,377,312,246,184,120]	#V
VP = [62,63,64,66,68,70,72,77,
	61,62,63,64,66,68,70,73,
	60,62,63,65,67,68,71,73	]	#V
R = 3520	#Ohm
powers = []
for i in range(len(VP)):
	powers.append(VP[i]*VR[i]/R)

l_met = 0.6 #m
c = 3e8 #m/s
eps0_const = 8.85e-12
e_const = 1.6e-19
me_const = 3.1e-31
Ne = []

for i in range(len(names)):
	Ne.append(processing(names[i], 0.34))

print("Ne[1/m^3]\t Power[W]")
for i in range(len(Ne)):
	print(str(round(Ne[i]/1e13,2))+"e13\t", powers[i])

Ne_average, powers_av = [], []
std_error = []
for i in range(len(Ne)//3):
	powers_av.append((powers[i]+powers[i+8]+powers[i+16])/3)
	Ne_average.append((Ne[i]+Ne[i+8]+Ne[i+16])/3)
	std_error.append(((Ne_average[i]-Ne[i])**2 + (Ne_average[i]-Ne[i+8])**2 + (Ne_average[i]-Ne[i+16])**2)**0.5/3**0.5)
	std_error[i] *= 880/(62+573)*1.01*1.05*1.01 #instrumental errors

x_comsol = [ 10.314, 8.6196, 6.9349, 5.2969, 3.7435]
y_comsol = [ 1.1714348165658072E14, 1.027125356226745E14, 8.814780413122358E13,
 	7.341168208550155E13, 5.847486514655857E13, ]

plt.rcParams.update({'font.size': 14})
plt.plot(x_comsol, y_comsol, label="Comsol Multiphysics", color="red")
plt.errorbar(powers_av[:-1], Ne_average[:-1],
 yerr = std_error[:-1],
 capsize = 4,
 fmt='o',
 label = "VSWR measurements",
 color="blue"
 )
plt.legend(loc="best")
plt.xlabel("Power [W]")
plt.ylabel(r"Electron density [$\frac{1}{m^3}$]")
#plt.ylim(1.02e19,1.1e19)
plt.grid()
plt.savefig('Ne_W.svg')
plt.show()
plt.close()