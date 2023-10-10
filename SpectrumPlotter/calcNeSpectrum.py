dlmb = 6.8	#A
lmb0 = 2530	#A
k_B_const = 1.38e-23
Te = 7000 #K
e_const = 1.6e-19
eps_const = 8.85e-12
n1 = 7
n2 = 6
Zp = 1
Ze = 80
dNe = (eps_const*k_B_const*Te/(4*3.14*e_const**2))**0.5	#Debay radius * Ne**0.5

X = 8.16e-19*lmb0**2*(n1**2-n2**2)*Zp**(0.33)/Ze
Y = 0.7*(4/3*3.14*dNe**3)**-0.33
# print(Y, " Y")
# calcNe = (Y/2+(Y**2/4+dlmb/X)**0.5)**3
calcNe = (dlmb/(X*(1-Y)))**(3/2)

Ne = 1.2e20 #1/m**3
ND = 4/3*3.14*(dNe/Ne**0.5)**3*Ne
calculated_dlmb = 8.16e-19*lmb0**2*Ne**(0.67)*(1-0.7*ND**(-0.33))*(n1**2-n2**2)*Zp**(0.33)/Ze
print(calculated_dlmb, " calculated_dlmb")
print(dlmb, "dlmb")
print(dNe/Ne**0.5, " Debay radius")
print(calcNe, " calculated_Ne")