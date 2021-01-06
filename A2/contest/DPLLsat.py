#!/usr/bin/python3
# CMPT310 A2
#####################################################
#####################################################
# Please enter the number of hours you spent on this
# assignment here
"""
num_hours_i_spent_on_this_assignment = 20
"""
#
#####################################################
#####################################################

#####################################################
#####################################################
# Give one short piece of feedback about the course so far. What
# have you found most interesting? Is there a topic that you had trouble
# understanding? Are there any changes that could improve the value of the
# course to you? (We will anonymize these before reading them.)
"""
<Your feedback goes here>
None

"""
#####################################################
#####################################################
import sys, getopt
import copy
import random
import time
import numpy as np
sys.setrecursionlimit(10000)

class SatInstance:
	def __init__(self):
		pass

	def from_file(self, inputfile):
		self.clauses = list()
		self.VARS = set()
		self.p = 0
		self.cnf = 0
		with open(inputfile, "r") as input_file:
			self.clauses.append(list())
			maxvar = 0
			for line in input_file:
				tokens = line.split()
				if len(tokens) != 0 and tokens[0] not in ("p", "c"):
					for tok in tokens:
						lit = int(tok)
						maxvar = max(maxvar, abs(lit))
						if lit == 0:
							self.clauses.append(list())
						else:
							self.clauses[-1].append(lit)
				if tokens[0] == "p":
					self.p = int(tokens[2])
					self.cnf = int(tokens[3])
			assert len(self.clauses[-1]) == 0
			self.clauses.pop()
			if (maxvar > self.p):
				print("Non-standard CNF encoding!")
				sys.exit(5)
		# Variables are numbered from 1 to p
		for i in range(1, self.p + 1):
			self.VARS.add(i)

	def __str__(self):
		s = ""
		for clause in self.clauses:
			s += str(clause)
			s += "\n"
		return s


def main(argv):
	inputfile = ''
	verbosity = False
	inputflag = False
	try:
		opts, args = getopt.getopt(argv, "hi:v", ["ifile="])
	except getopt.GetoptError:
		print('DPLLsat.py -i <inputCNFfile> [-v] ')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print('DPLLsat.py -i <inputCNFfile> [-v]')
			sys.exit()
		##-v sets the verbosity of informational output
		## (set to true for output veriable assignments, defaults to false)
		elif opt == '-v':
			verbosity = True
		elif opt in ("-i", "--ifile"):
			inputfile = arg
			inputflag = True
	if inputflag:
		instance = SatInstance()
		instance.from_file(inputfile)
		#start_time = time.time()
		solve_dpll(instance, verbosity)
		#print("--- %s seconds ---" % (time.time() - start_time))

	else:
		print("You must have an input file!")
		print('DPLLsat.py -i <inputCNFfile> [-v]')


# Finds a satisfying assignment to a SAT instance,
# using the DPLL algorithm.
# Input: a SAT instance and verbosity flag
# Output: print "UNSAT" or
#    "SAT"
#    list of true literals (if verbosity == True)
#
#  You will need to define your own
#  DPLLsat(), DPLL(), pure-elim(), propagate-units(), and
#  any other auxiliary functions
def solve_dpll(instance, verbosity):
	# print(instance)
	# instance.VARS goes 1 to N in a dict
	# print(instance.VARS)
	# print(verbosity)
	###########################################
	# Start your code

	clauses = instance.clauses
	variables = instance.VARS

	model = DPLL(clauses, variables)
	if model:
		print('SAT')
		if verbosity:
			trueList = []
			for var, domain in model.items():
				if domain:
					trueList.append(var)
			trueList.sort()
			print(trueList)
	else:
		print('UNSAT')

	###########################################
#pick the variable that occurs the most in the formula
def pickSymbol(clauses, variables, model):
	counts = {}
	for p in variables:
		counts[p] = 0
	for c in clauses:
		for s in c:
			if abs(s) in variables:
				counts[abs(s)] = counts[abs(s)] + 1
	max_key = 0
	max_value = 0
	for key, value in counts.items():
		if value > max_value and key not in model:
			max_key = key
			max_value = value
	return max_key

def propagateunits(clauses, symbols, model):
	found = False
	for clause in clauses:
		if len(clause) == 1:
			found = True
			p = clause[0]
			if abs(p) not in model:
				if p < 0:
					model[-p] = False
				else:
					model[p] = True
				clauses.remove(clause)
			else:
				if p > 0:
					if model[p] == False:
						return -1
				else:
					if model[-p] == True:
						return -1
	return found


def DPLL(clauses, symbols, model = {}):
	# base cases
	modelcopy = model.copy()
	clausescopy = listcopy(clauses)

	if propagateunits(clausescopy, symbols, modelcopy) == -1:
		return False
				
	if DPLLsat(clausescopy, symbols, modelcopy):
		return modelcopy

	p = pickSymbol(clausescopy, symbols, modelcopy)
	for value in [True, False]:
		modelcopy[p] = value
		ret = DPLL(clausescopy.copy(), symbols, modelcopy)
		if ret:
			return ret
	return False

def DPLLsat(clauses, variables, model):
	return len(variables) == len(model)

def listcopy(clauses):
	copy = []
	for m in clauses:
		copy.append(m.copy())
	return copy


if __name__ == "__main__":
	main(sys.argv[1:])

