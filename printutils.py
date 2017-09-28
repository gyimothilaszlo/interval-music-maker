def printWorkout(worklengths, worklengthRepeats, recovFactor):
	print("Your workout:")
	for wl, rep in zip(worklengths, worklengthRepeats):
		if(rep):
			print(rep, "x", wl, "sec with", int(wl*recovFactor), "sec rest")

def printProgressBar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '#'):
	percent = ("{0:." + str(decimals) + "f}").format(100 * iteration / float(total))
	filledLength = int(length * iteration / total)
	bar = fill * filledLength + '-' * (length - filledLength)
	print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')

	if iteration == total:
		print("")
