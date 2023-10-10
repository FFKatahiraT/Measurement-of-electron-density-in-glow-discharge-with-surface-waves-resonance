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

def plotter(r_list, Func_list, xLabel, yLabel, name, ylog=False):
	plt.rcParams.update({'font.size': 14})
	plt.plot(r_list, Func_list)
	# plt.scatter(r_list[i], Func_list[i], label=Label[i], marker=pointstyle[i])
	plt.grid()
	if ylog: plt.yscale("log") 
	plt.ylabel(yLabel)
	plt.xlabel(xLabel)
	plt.tight_layout()
	plt.savefig(name+'.svg')
	# plt.show()
	plt.close()

def processing(name, length):
	Freq, Rs, Xs = read_data(name)
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
	return calcNe(length, Freq[minVSWRIndex]*1e6)


names = ["sark_009.csv", 
	"sark_010.csv", "sark_011.csv", 
	"sark_012.csv", "sark_013.csv", 
	"sark_014.csv", "sark_015.csv", 
	"sark_016.csv", "sark_017.csv", ]
names.reverse()

powers = [10, 9.1, 8, 6.9, 5.9, 4.6, 3.6, 2.6, 1.4]
l_met = 0.6 #m
c = 3e8 #m/s
eps0_const = 8.85e-12
e_const = 1.6e-19
me_const = 3.1e-31
Ne = []

for i in range(len(names)):
	Ne.append(processing(names[i], 0.34))

print("Ne[1/m^3]\tlength[m]")
for i in range(len(Ne)):
	print(str(round(Ne[i]/1e13,2))+"e13\t", powers[i])
plotter(powers, Ne, 'W [W]',"Ne", "ElectronDensity", ylog=False)