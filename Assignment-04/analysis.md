# Assignment 4 – Analysis

Name: <YOUR NAME>

## Problem 1

**(a)** Gen: choose k uniformly from {0,1}^128.
Mac_k(m), with m = m_1 || ... || m_l (l >= 1, each block 16 bytes): set x_0 = 0^128 and
x_i = F_k(x_{i-1} XOR m_i) for i = 1..l. The tag is t = x_l.
Vrfy_k(m, t): if m is empty/not a whole number of blocks or t is not 16 bytes, output 0;
otherwise recompute t' = Mac_k(m) and output 1 iff t' = t.

**(b)** (1) CBC-MAC uses a fixed IV of 0^128; CBC encryption uses a fresh random IV that is
sent along with the ciphertext. Using a fixed IV is fine here because a MAC is deterministic
and nothing is being hidden. (2) CBC-MAC outputs only the last chaining value x_l; CBC
encryption outputs every block c_1..c_l (and the IV). CBC encryption must also be
decryptable and randomized to be CPA-secure, while CBC-MAC needs neither.

**(c)** If F is a secure PRF, basic CBC-MAC is a secure MAC only when all messages
(queried and forged) have the same fixed length l, chosen in advance and independent of
the message. It is not secure for variable length under one key (Problem 2).

## Problem 2

**(a)** Let x_i be the chain values of m and x'_j those of m'. So x_l = t and x'_{l'} = t'.
For m* the first l blocks equal m, so the chain values are x_0..x_l and x_l = t.
Block l+1: x*_{l+1} = F_k(x_l XOR (m'_1 XOR t)) = F_k(t XOR m'_1 XOR t) = F_k(m'_1) = x'_1
(using x'_0 = 0, so x'_1 = F_k(0 XOR m'_1)).
Block l+j (j >= 2): x*_{l+j} = F_k(x*_{l+j-1} XOR m'_j) = F_k(x'_{j-1} XOR m'_j) = x'_j,
by induction. At the last block, x*_{l+l'} = x'_{l'} = t'. Hence Mac_k(m*) = t'.
m* has l + l' blocks. Since l, l' >= 1, l + l' > l and l + l' > l', so m* differs in length
from both m and m' and is a new message. (The Lecture 10 forgery is m' = m, l = 1: m* = m_1 || (m_1 XOR t), tag t.)

**(b)** Target M = M_1 || ... || M_L, L >= 2. Take m = M_1 (l = 1) and
m' = (M_2 XOR t) || M_3 || ... || M_L (l' = L-1 >= 1).
- Query 1: M_1, returns t.
- Query 2: (M_2 XOR t) || M_3 || ... || M_L, returns t'.
Then m* = M_1 || ((M_2 XOR t) XOR t) || M_3 || ... || M_L = M, so by (a) the tag on M is t'.
Query 1 has 1 block and query 2 has L-1 blocks; M has L >= 2 blocks, and 1 != L and L-1 != L,
so neither query equals M. The identity in (a) holds for every key, so the success
probability is 1.

**(c)** With fixed length l, every query and the forged message must have exactly l blocks.
In (a), m* has l + l' = 2l blocks, which is rejected. In (b), query 1 has 1 block, so
it is legal only if l = 1; but then the target M would need L = l = 1 block, contradicting
L >= 2. So some query is rejected, or the target is not a valid message. (Also, query 2 has
L-1 = l-1 blocks, which is not l.) This matches the fixed-length security theorem in 1(c).

## Problem 3 output

Tests: `python3 -m unittest -v` -> 4 tests, all OK.

3(b), `python3 forgery.py` (random key; values differ per run):
```text
=== 3(b) demo ===
query 1: msg=66726f6d3d616c69636526746f3d6d61
         tag=3dd91defb459b9396c7161496f6259a3
query 2: msg=51b5729dcd7fd85403040f3d5253699330303030266e6f74653d72656e742121
         tag=f9aaae94cb04d784405142d70fff617d
forged tag:         f9aaae94cb04d784405142d70fff617d
oracle saw target:  False
verify(target,tag): True

successful forgeries in 100 runs: 100/100
```

3(c), oracle and verifier accept only 3-block messages:
```text
attack failed at query 1: oracle accepts only 3-block messages; got 16 bytes
queries accepted by oracle: 0
2-block query would be rejected: True
```
The attack fails at the very first query (M_1 is 1 block), and the second query
(M_2 XOR t) || M_3 is only 2 blocks, so it would fail as well. No tag is obtained.
