import numpy as np
import matplotlib.pyplot as plt
from qif import *
import sys 
import csv




np.set_printoptions(precision=5, suppress=True)


#### Section 3 ###########################

print("\nSection 3 ###############\n")



def create_first_row (method,n):
	random_values = []
	row = []
	for i in range(n):
		if (method=="normal"):
			random_values.append(np.random.normal(loc = 5, scale = 0.5))
		elif(method=="random"):
			random_values.append(np.random.random())
		elif(method == "only_one_one"):
			for i in range (n):
				row.append(0)
			random_pos = np.random.randint(0,n-1)
			row[i] = 1
			return row
		elif(method == "constant"):
			each = 1/n
			for i in range (n):
				row.append(each)
			assert(abs(sum(row)-1) <= 0.02)
			return row
	#print(random_values)
	for value in random_values:
		row.append(value/sum(random_values))
	#print(row)
	#print(sum(row))
	assert(abs(sum(row)-1) <= 0.02)
	return row

# Returns the vector [1, 0, ..., 0] which denotes the predicate that is true for secret x and false for all others
def s_dist_pred(n, x=0):
    P = np.zeros(n)
    P[0] = 1
    return P

# returns the rho and Q of lemma 1
def pred_rho_and_Q(pi, P):
    p = np.dot(P, pi)       # probability of secrets for which P holds
    rho = np.array([p, 1-p])

    Q = np.empty((2,pi.size))

    Q[0:] = np.multiply(P, pi) / rho[0]
    Q[1:] = np.multiply(1-P, pi) / rho[1]

    return (rho,Q)

def apply_mechanism(adv_type, how_to_create_row,n ):
	total = 0
	for i in range(0,MAX_RUNS_INNER):
		q0 = create_first_row (how_to_create_row,n)
		if (adv_type == "exact"):
			capacity_when_doing_nothing = measure.bayes_vuln.mult_capacity(extend(q0, C))
		else:
			capacity_when_doing_nothing =  measure.pred_vuln.mult_capacity(P, extend(q0, C))[0]
		total +=capacity_when_doing_nothing
	return total/MAX_RUNS_INNER

# test lemma1
n = 4
pi = probab.randu(n)

C = channel.randu(n, n)
print(C)


P = s_dist_pred(pi.size)
(rho,Q) = pred_rho_and_Q(pi, P)

print("lemma1, should be the same: ", measure.pred_vuln.mult_leakage(P, pi, C), measure.bayes_vuln.mult_leakage(rho, Q.dot(C)))



#### Section 4 ###########################

print("\nSection 4 ###############\n")

# extend channel with one row
def extend(q, C):
    return np.concatenate(([q], C))

# The example
C = np.array([
    # without the row to compute
    [.05, .95],
    [.58, .42]
])
pi = np.array([0.47, 0.29, 0.24])

# Find the best q for the s-distinguishing adversary
P = s_dist_pred(pi.size)
(rho,Q) = pred_rho_and_Q(pi, P)
q = probab.uniform(2)                   # dummy solution q, just to add to C in the line below to get the correct size
q_star = Q[1].dot(extend(q, C))
print("q_star", q_star)

# find the best q for the exact adversary
# This is the solution of the optimization problem of Proposition 2
q = mechanism.bayes_vuln.min_vuln_for_row(pi[1:], pi[0], C)

print("q", q)       # Note: it's not the one in the draft paper! but it works...

Cq = extend(q, C)
Cqstar = extend(q_star, C)

print("qstar should give optimal leakage 1 for the s-distringuishing adversary:", measure.pred_vuln.mult_leakage(P, pi, Cqstar))
print("qstar should NOT give optimal leakage for the exact adversary:", measure.bayes_vuln.mult_leakage(pi, Cqstar))
print("but q does give optimal exact leakage:", measure.bayes_vuln.mult_leakage(pi, Cq))


#### Section 5 ###############################

print("\nSection 5 ###############\n")

# Example of 5.1

C1 = np.array([
    [1, 0],
    [1, 0],
    [0, 1],
])
C2 = np.array([
    [.5, .5],
    [1, 0],
    [0, 1],
])

print("Both channels have capacity 2 for the exact adversary")
print(measure.bayes_vuln.mult_capacity(C1))
print(measure.bayes_vuln.mult_capacity(C2))

print("But C2 has smaller capacity for the s-distinguishing adversary")
print(measure.pred_vuln.mult_capacity(P, C1))
print(measure.pred_vuln.mult_capacity(P, C2))



#### Section 6 #################################

print("\nSection 6 ###############\n")

# 6.2 exact polynomial time solution

n_list = []
nothing_list = []
optimize_list_approx = []
random_list = []
normal_list = []
constant_list = []
optimize_list = []
real_optimal = []
#n_cols  = 50
#C = channel.randu(100) 


filename= type_of_adversary + ".pdf"


print("RUNNING FOR ", filename)


print("---- MAX_RUNS =", MAX_RUNS, "------")

for n in range (4,4,1):
	#C1 = create_first_row("random",n_cols )	
	#C = extend (C1,C)

	avg_capacity_one_one = 0
	optimized_capacity_approx = 0
	accurate_result = 0

	avg_capacity_random = 0
	avg_capacity_constant = 0 
	avg_capacity_normal = 0
	for j in range (MAX_RUNS):
		pi = probab.randu(n)

		P = s_dist_pred(pi.size)

		#print(C)
	
		avg_capacity_one_one  += apply_mechanism(type_of_adversary, "only_one_one",n )
		avg_capacity_random   += apply_mechanism(type_of_adversary, "random",n )
		avg_capacity_constant += apply_mechanism(type_of_adversary, "constant",n )
		avg_capacity_normal += apply_mechanism(type_of_adversary, "normal",n )


	

		#print("Avg capacity when doing nothing:",avg_capacity)

		(r1,q1) = metric.optimize.simplex_l1_min_enclosing_ball(C)
		#print(q1)
		#print("SEB: exact solution", optimized_capacity)
		if (filename == "exact.pdf"):
			accurate_result += measure.bayes_vuln.mult_capacity(extend(q1, C))
		else:
			accurate_result +=measure.pred_vuln.mult_capacity(P,extend(q1, C))[0]

		# 6.3 approximation via the Euclidean SEB

		(r2,q2) = metric.optimize.l2_min_enclosing_ball(C)

		if (filename == "exact.pdf"):
			optimized_capacity_approx += measure.bayes_vuln.mult_capacity(extend(q2, C))
		else:
			optimized_capacity_approx +=measure.pred_vuln.mult_capacity(P,extend(q2, C))[0]
				
		#print("SEB: approximation", optimized_capacity_approx)

		
		
		#optimize_list.append(optimized_capacity)
	n_list.append(n)
	nothing_list.append(avg_capacity_one_one/MAX_RUNS)
	normal_list.append(avg_capacity_normal/MAX_RUNS)
	random_list.append(avg_capacity_random/MAX_RUNS)
	constant_list.append(avg_capacity_constant/MAX_RUNS)
	optimize_list_approx.append(optimized_capacity_approx/MAX_RUNS)
	real_optimal.append(accurate_result/MAX_RUNS)

plt.plot(n_list,nothing_list, label="One 1 rest 0")
plt.plot(n_list,random_list, label="Unif. Random")
plt.plot(n_list, constant_list, label="Constant 1/n")
plt.plot(n_list, normal_list, label="Normal Distrib.")
plt.plot(n_list,optimize_list_approx, label ="Optimize (Approx.)")
plt.plot(n_list,real_optimal, label ="Optimize (Exact.)")
#plt.plot(n_list,optimize_list, label ="Optimize (Exact.)")
plt.show()
#plt.legend()
plt.ylabel("Mult Capacity")
plt.xlabel("Channel Size")
plt.savefig(filename, format="pdf", bbox_inches="tight")





'''
MAX_RUNS = 1000
total = 0

capacity_list = []
for i in range(0,MAX_RUNS):
	q0 = create_first_row ("random",channel_size)
	print(q0)
	capacity_when_doing_nothing =  measure.bayes_vuln.mult_capacity(extend(q0, C)) 
	print(capacity_when_doing_nothing)
	capacity_list.append(capacity_when_doing_nothing)
	total +=capacity_when_doing_nothing
	avg_capacity = total/MAX_RUNS
print("Avg capacity when doing nothing RANDOM:",avg_capacity)

(r2,q2) = metric.optimize.l2_min_enclosing_ball(C)

optimized_capacity_approx = measure.bayes_vuln.mult_capacity(extend(q2, C)) 
print("SEB: approximation", optimized_capacity_approx)

plt.xlabel("Box Plot for 2x2 array")
plt.ylim(0,3)
plt.ylabel("Mult Leakage")
plt.boxplot(capacity_list)
#plt.boxplot(optimized_capacity_approx)
plt.savefig("box_plot.pdf", format="pdf", bbox_inches="tight")

plt.show()

exit()

total = 0
for i in range(0,MAX_RUNS):
	q0 = create_first_row ("only_one_one",channel_size)
	capacity_when_doing_nothing =  measure.bayes_vuln.mult_capacity(extend(q0, C)) 
	total +=capacity_when_doing_nothing
	avg_capacity = total/MAX_RUNS
print("Avg capacity when doing nothing ONLY ONE ONE:",avg_capacity)

(r2,q2) = metric.optimize.l2_min_enclosing_ball(C)

optimized_capacity_approx = measure.bayes_vuln.mult_capacity(extend(q2, C)) 
print("SEB: approximation", optimized_capacity_approx)

(r1,q1) = metric.optimize.simplex_l1_min_enclosing_ball(C)
	#print(q1)
optimized_capacity = measure.bayes_vuln.mult_capacity(extend(q1, C)) 
print("SEB: exact solution", optimized_capacity)


total = 0
for i in range(0,MAX_RUNS):
	q0 = create_first_row ("random",channel_size)
	capacity_when_doing_nothing =  measure.bayes_vuln.mult_capacity(extend(q0, C)) 
	total +=capacity_when_doing_nothing
	avg_capacity = total/MAX_RUNS
print("Avg capacity when doing nothing RANDOM:",avg_capacity)

(r2,q2) = metric.optimize.l2_min_enclosing_ball(C)

optimized_capacity_approx = measure.bayes_vuln.mult_capacity(extend(q2, C)) 
print("SEB: approximation", optimized_capacity_approx)


total = 0
for i in range(0,MAX_RUNS):
	q0 = create_first_row ("normal",channel_size)
	capacity_when_doing_nothing =  measure.bayes_vuln.mult_capacity(extend(q0, C)) 
	total +=capacity_when_doing_nothing
	avg_capacity = total/MAX_RUNS
print("Avg capacity when doing nothing NORMAL:",avg_capacity)


total = 0
for i in range(0,MAX_RUNS):
	q0 = create_first_row ("constant",channel_size)
	capacity_when_doing_nothing =  measure.bayes_vuln.mult_capacity(extend(q0, C)) 
	total +=capacity_when_doing_nothing
	avg_capacity = total/MAX_RUNS
print("Avg capacity when doing nothing CONSTANT:",avg_capacity)
'''

