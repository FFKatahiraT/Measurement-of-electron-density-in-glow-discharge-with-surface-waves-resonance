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

def processing(name, yLabel):
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
	minVSWRIndex = VSWR.index(min(VSWR))
	minXsIndex = absXs.index(min(absXs))
	TextOutput = (str(Freq[minVSWRIndex])+"\t"+str(min(VSWR))+"\t"+
		str(Freq[minXsIndex])+"\t"+str(min(absXs))+"\t"+str(name))
	print(TextOutput)
	# plotter(Freq, [Rs, Xs], 'Freq [MHz]',yLabel, name, Label=["Rs", "Xs"])
	plotter(Freq, [VSWR], 'Freq [MHz]',"VSWR", "VSWR"+name, ylog=True)

names = ["sark_008.csv", "sark_009.csv", 
	"sark_010.csv", "sark_011.csv", 
	"sark_012.csv", "sark_013.csv", 
	"sark_014.csv", "sark_015.csv", 
	"sark_016.csv", "sark_017.csv", ]

print("min\tVSWR Freq\tmin Xs Freq\tname")
for name in names:
	processing(name, r"VSWR")
# processing('H_f.txt', r'Magnetic field strength [A/m]')
# processing('nu_c_omega_p.txt', r'$\nu_c/\omega_p$ [A/m]')
# processing('Te(f).txt', r'Electron temperature [$eV$]')
# processing('T(f).txt', r'Temperature [$K$]')