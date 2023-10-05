VR = [573,509,439,368,306,230,175,117,52]	#V
VP = [62,63,64,66,68,70,72,77,92]	#V
R = 3520	#Ohm

W = []
for i in range(len(VP)):
	W.append(VP[i]*VR[i]/R)

print(W)