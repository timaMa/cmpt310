#!/usr/bin/python3

import sys
import os
import random
import math

import numpy as np
import operator

#####################################################
#####################################################
# Please enter the number of hours you spent on this
# assignment here
num_hours_i_spent_on_this_assignment = 47
#####################################################
#####################################################

#####################################################
#####################################################
# Give one short piece of feedback about the course so far. What
# have you found most interesting? Is there a topic that you had trouble
# understanding? Are there any changes that could improve the value of the
# course to you? (We will anonymize these before reading them.)
# <Your feedback goes here>
# For this assignment, it is really hard to understand what should we do. 
# Hidden Markov Model is really interesting topic. However, it's also really
#   hard to understand. 
#####################################################
#####################################################



# Outputs a random integer, according to a multinomial
# distribution specified by probs.
def rand_multinomial(probs):
    # Make sure probs sum to 1
    assert(abs(sum(probs) - 1.0) < 1e-5)
    rand = random.random()
    for index, prob in enumerate(probs):
        if rand < prob:
            return index
        else:
            rand -= prob
    return 0

# Outputs a random key, according to a (key,prob)
# iterator. For a probability dictionary
# d = {"A": 0.9, "C": 0.1}
# call using rand_multinomial_iter(d.items())
def rand_multinomial_iter(iterator):
    rand = random.random()
    for key, prob in iterator:
        if rand < prob:
            return key
        else:
            rand -= prob
    return 0


class HMM():

    def __init__(self):
        self.num_states = 2
        self.prior      = np.array([0.5, 0.5])
        self.transition = np.array([[0.999, 0.001], [0.01, 0.99]])
        self.emission   = np.array([{"A": 0.291, "T": 0.291, "C": 0.209, "G": 0.209},
                                    {"A": 0.169, "T": 0.169, "C": 0.331, "G": 0.331}])

    # Generates a sequence of states and characters from
    # the HMM model.
    # - length: Length of output sequence
    def sample(self, length):
        sequence = []
        states = []
        rand = random.random()
        cur_state = rand_multinomial(self.prior)
        for i in range(length):
            states.append(cur_state)
            char = rand_multinomial_iter(self.emission[cur_state].items())
            sequence.append(char)
            cur_state = rand_multinomial(self.transition[cur_state])
        return sequence, states

    # Generates a emission sequence given a sequence of states
    def generate_sequence(self, states):
        sequence = []
        for state in states:
            char = rand_multinomial_iter(self.emission[state].items())
            sequence.append(char)
        return sequence

    # Outputs the most likely sequence of states given an emission sequence
    # - sequence: String with characters [A,C,T,G]
    # return: list of state indices, e.g. [0,0,0,1,1,0,0,...]
    def viterbi(self, sequence):
        ###########################################
        # Start your code
        print("My code here")
        result = []
       	lowPath = []
       	highPath = []
       	lastLowProbability = self.emission[0][sequence[0]] * self.prior[0]
       	lastHighProbability = self.emission[1][sequence[0]] * self.prior[1]
       	lowToLow = self.transition[0][0]
       	lowToHigh = self.transition[0][1]
       	highToLow = self.transition[1][0]
       	highToHigh = self.transition[1][1]
       	for i in range(1,len(sequence)):
       		lowFromPreLow = self.emission[0][sequence[i]] * lastLowProbability * lowToLow
       		lowFromPreHigh = self.emission[0][sequence[i]] * lastHighProbability * highToLow
       		highFromPreLow = self.emission[1][sequence[i]] * lastLowProbability * lowToHigh
       		highFromPreHigh = self.emission[1][sequence[i]] * lastHighProbability * highToHigh
       		tempLow = lowPath.copy()
       		if lowFromPreLow > lowFromPreHigh:
       			lastLowProbability = lowFromPreLow
       			lowPath.append(0)
       		else:
       			lastLowProbability = lowFromPreHigh
       			lowPath = highPath.copy()
       			lowPath.append(1)
       		if highFromPreLow > highFromPreHigh:
       			lastHighProbability = highFromPreLow
       			highPath = tempLow.copy()
       			highPath.append(0)
       		else:
       			lastHighProbability = highFromPreHigh
       			highPath.append(1)
       		if i == len(sequence) - 1:
       			if lastLowProbability < lastHighProbability:
       				highPath.append(1)
       				result = highPath.copy()
       				# return highPath
       			else:
       				lowPath.append(0)
       				result = lowPath.copy()
       	return result
        # End your code
        ###########################################


    def log_sum(self, factors):
        if abs(min(factors)) > abs(max(factors)):
            a = min(factors)
        else:
            a = max(factors)

        total = 0
        for x in factors:
            total += math.exp(x - a)
        return a + math.log(total)

    # - sequence: String with characters [A,C,T,G]
    # return: posterior distribution. shape should be (len(sequence), 2)
    # Please use log_sum() in posterior computations.
    def posterior(self, sequence):
        ###########################################
        # Start your code
        print("My code here")
        
       	lowToLow = math.log(self.transition[0][0])
       	lowToHigh = math.log(self.transition[0][1])
       	highToLow = math.log(self.transition[1][0])
       	highToHigh = math.log(self.transition[1][1])
       	lastLowProbability1 = math.log(self.emission[0][sequence[0]]) + math.log(self.prior[0])+lowToLow
        lastLowProbability2 = math.log(self.emission[0][sequence[0]]) + math.log(self.prior[0])+highToLow
        lastLowProbability = self.log_sum([lastLowProbability1,lastLowProbability2])
       	lastHighProbability1 = math.log(self.emission[1][sequence[0]]) + math.log(self.prior[1])+ lowToHigh
       	lastHighProbability2 = math.log(self.emission[1][sequence[0]]) + math.log(self.prior[1])+ highToHigh
       	lastHighProbability = self.log_sum([lastHighProbability1,lastHighProbability2])
       	forwardArr = np.array([[lastLowProbability,lastHighProbability]])
       	for i in range(1,len(sequence)):
       		lowFromPreLow = math.log(self.emission[0][sequence[i]]) + lastLowProbability + lowToLow
       		lowFromPreHigh = math.log(self.emission[0][sequence[i]]) + lastHighProbability + highToLow
       		highFromPreLow = math.log(self.emission[1][sequence[i]]) + lastLowProbability + lowToHigh
       		highFromPreHigh = math.log(self.emission[1][sequence[i]]) + lastHighProbability + highToHigh
       		lastLowProbability = self.log_sum([lowFromPreLow , lowFromPreHigh])
       		lastHighProbability = self.log_sum([highFromPreLow , highFromPreHigh])
       		forwardArr=np.append(forwardArr, [[lastLowProbability,lastHighProbability]],axis = 0)
       	

       	
       	blastLowProbability = math.log(1)
       	blastHighProbability = math.log(1)
       	
       	backwardArr = np.array([[blastLowProbability,blastHighProbability]])
       	for j in range(len(sequence)-1, 0, -1):
       		lowFromPreLow = math.log(self.emission[0][sequence[j]]) + blastLowProbability + lowToLow
       		lowFromPreHigh = math.log(self.emission[1][sequence[j]]) + blastHighProbability + lowToHigh
       		highFromPreLow = math.log(self.emission[0][sequence[j]]) + blastLowProbability + highToLow
       		highFromPreHigh = math.log(self.emission[1][sequence[j]]) + blastHighProbability + highToHigh
       		blastLowProbability = self.log_sum([lowFromPreLow , lowFromPreHigh])
       		blastHighProbability = self.log_sum([highFromPreLow , highFromPreHigh])
       		backwardArr=np.append(backwardArr, [[blastLowProbability,blastHighProbability]],axis = 0)
       	backwardArr = backwardArr[::-1]
       	
       	for k in range(len(forwardArr)):
       		alpha = self.log_sum(forwardArr[k])
       		forwardArr[k] = (np.multiply(forwardArr[k],backwardArr[k]))/alpha
       	return forwardArr
        # End your code
        ###########################################


    # Output the most likely state for each symbol in an emmision sequence
    # - sequence: posterior probabilities received from posterior()
    # return: list of state indices, e.g. [0,0,0,1,1,0,0,...]
    def posterior_decode(self, sequence):
        nSamples  = len(sequence)
        post = self.posterior(sequence)
        best_path = np.zeros(nSamples)
        for t in range(nSamples):
            best_path[t], _ = max(enumerate(post[t]), key=operator.itemgetter(1))
        return list(best_path.astype(int))


def read_sequences(filename):
    inputs = []
    with open(filename, "r") as f:
        for line in f:
            inputs.append(line.strip())
    return inputs

def write_sequence(filename, sequence):
    with open(filename, "w") as f:
        f.write("".join(sequence))

def write_output(filename, viterbi, posterior):
    vit_file_name = filename[:-4]+'_viterbi_output.txt' 
    with open(vit_file_name, "a") as f:
        for state in range(2):
            f.write(str(viterbi.count(state)))
            f.write("\n")
        f.write(" ".join(map(str, viterbi)))
        f.write("\n")

    pos_file_name = filename[:-4]+'_posteri_output.txt' 
    with open(pos_file_name, "a") as f:
        for state in range(2):
            f.write(str(posterior.count(state)))
            f.write("\n")
        f.write(" ".join(map(str, posterior)))
        f.write("\n")


def truncate_files(filename):
    vit_file_name = file[:-4]+'_viterbi_output.txt'
    pos_file_name = file[:-4]+'_posteri_output.txt' 
    if os.path.isfile(vit_file_name):
        open(vit_file_name, 'w')
    if os.path.isfile(pos_file_name):
        open(pos_file_name, 'w')


if __name__ == '__main__':

    hmm = HMM()

    file = sys.argv[1]
    truncate_files(file)
    
    sequences  = read_sequences(file)
    for sequence in sequences:
        viterbi   = hmm.viterbi(sequence)
        posterior = hmm.posterior_decode(sequence)
        write_output(file, viterbi, posterior)


