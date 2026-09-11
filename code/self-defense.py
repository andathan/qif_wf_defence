import numpy as np

from qif import *

np.set_printoptions(precision=5, suppress=True)


#### Section 3 ###########################

print("\nSection 3 ###############\n")

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

# test lemma1
n = 3
pi = probab.randu(n)
C = channel.randu(n, n)

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

n = 100
C = channel.randu(n)

(r1,q1) = metric.optimize.simplex_l1_min_enclosing_ball(C)

print("exact solution", measure.bayes_vuln.mult_capacity(extend(q1, C)))

# 6.3 approximation via the Euclidean SEB

(r2,q2) = metric.optimize.l2_min_enclosing_ball(C)

print("approximation", measure.bayes_vuln.mult_capacity(extend(q2, C)))






