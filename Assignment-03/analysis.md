**By: Savar Shrestha**
 
 ---

 ## 1: Key Concepts

 ### a. PRG (Pseudorandom Generator)

 PRG (Pseudorandom Generator) is an efficient, deterministic algorithm that takes a  small, truly random input string called a seed and stretches it into a longer output string of pseudorandom bits. It is not a keyed function. 

### b. PRF (Pseudorandom Function)

PRF (Pseudorandom Function) is a keyed algorithm that takes a secret key and an input value and produces a computationally indistinguishable output from a truly random function. It is a collection of keyed functions that act like a random oracle to anyone that doesn't know the key.

### c. PRP (Pseudorandom Permutation)

PRP (Pseudorandom Permutation) is a keyed bijection function that maps a set of input to output of the same length that is computationally indistinguishable from a truly random permutation. The implementation of PRP, a keyed family of bujections with efficient inversion is the fundamental definition of a block cipher.


## 2: Indistinguishability

**a.** The basic ability of the idea behind computational indistinguishability is that two probability distributions cannot be differentiated by any efficient polynomial time algorithm. Adversaries are probabilistic polynomial time because security is claimed only against attackers whose resources are bounded. Negligible means smaller than 1/p(n) for every polynomial p, so the advantage is unexploitable even after many repetitions.

**b. PRG.**
- Real experiment: sample a uniform seed s ∈ {0,1}^n and give D the string y = G(s).
- Ideal experiment: give D a uniform string y ∈ {0,1}^ℓ(n), the same length as G's output.
- D receives only this one string (no oracle access and no seed) and outputs a bit.
- G is a secure PRG if for every probalilistic polynomial time distinguisher D,
  | Pr[D(G(s)) = 1] − Pr[D(y) = 1] | ≤ negl(n),
  where s is uniform in {0,1}^n and y is uniform in {0,1}^ℓ(n).

**c. PRF.**
- Real: uniform k; D has adaptive oracle access to F_k(·).
- Ideal: D has adaptive oracle access to f, uniform over all functions with the same domain and range.
- D is probabilistic polynomial time, so it makes polynomially many queries, each possibly depending on earlier answers.
- Secure if for every PPT D: | Pr[D^{F_k(·)}(1^n)=1] − Pr[D^{f(·)}(1^n)=1] | ≤ negl(n).

**d. PRP.**
- Real: uniform k; D has adaptive oracle access to F_k(·).
- Ideal: D has adaptive oracle access to π, uniform over permutations of {0,1}^n (distinct queries get distinct answers, repeats get the same answer).
- Forward oracle only; no inverse oracle.
- Secure if for every PPT D: | Pr[D^{F_k(·)}(1^n)=1] − Pr[D^{π(·)}(1^n)=1] | ≤ negl(n).


## 3. Chosen-plaintext attack security

### a. IND-CPA experiment CPA_{A,Π}(n)

1. k ← Gen(1^n), kept secret.
2. A gets oracle access to Enc_k(·) and queries adaptively.
3. A outputs m0, m1 with |m0| = |m1|.
4. Uniform b ← {0,1}; A receives c* ← Enc_k(m_b).
5. A keeps oracle access to Enc_k(·), including queries on m0, m1.
6. A outputs b'; the experiment outputs 1 iff b' = b.

Π is CPA-secure if for every PPT A: Pr[CPA_{A,Π}(n)=1] ≤ 1/2 + negl(n).

*Equal length:* encryption does not hide length in general. If |m0| ≠ |m1|, A could win from |c*| alone, so the equal-length requirement restricts the game to leakage of content.

*Oracle on m0, m1:* it models an attacker who can make honest parties encrypt chosen messages, and it forces security even when other encryptions of the same messages are visible. Consequently, every stateless deterministic scheme is insecure (A queries m0 and compares with c*), so CPA-secure encryption must be randomized.


### b. Attack on Enc_k(m) = F_k(m)

Adversary A:
1. Choose distinct m0 = 0^n, m1 = 1^n.
2. Query the oracle on m0 and receive c0 = F_k(m0).
3. Output (m0, m1) and receive c* = F_k(m_b).
4. Decision rule: output b' = 0 if c* = c0, else b' = 1.

*Success probability:* F_k is injective, so F_k(m0) ≠ F_k(m1). If b = 0, c* = c0 and A outputs 0. If b = 1, c* ≠ c0 and A outputs 1. So A succeeds with probability exactly 1 (advantage 1/2).

*Why PRP security does not imply CPA security:* the same attack succeeds with probability 1 against a truly random permutation, since a random permutation is also deterministic and injective. So A does not distinguish F_k from a random permutation and does not contradict PRP security. The flaw is the scheme: deterministic encryption always leaks plaintext equality, which PRP security does not rule out.


### c. Enc_k(m) = (r, H_k(r) ⊕ m)

*Decryption:* Dec_k(r, c) = H_k(r) ⊕ c. Correctness: H_k(r) ⊕ H_k(r) ⊕ m = m.

*Why (b) fails:* each encryption uses a fresh uniform r. The oracle's answer for m0 is (r', H_k(r') ⊕ m0) and the challenge is (r*, H_k(r*) ⊕ m_b), with r' ≠ r* except with probability 2^{-n}. Equal messages give different ciphertexts, so comparing to the oracle's answer reveals nothing.

*Why revealing r is fine:* r is chosen independently of k and m, so it carries no information about m. Only H_k(r) depends on k, and if r is fresh (never queried to H_k before), PRF security makes H_k(r) look uniform and independent of A's view. Then H_k(r) ⊕ m acts as a one-time pad.

*Randomizer reuse:* suppose A holds an encryption (r, c0) of 0^n, so c0 = H_k(r), and the challenge is (r, c*) with the same r. Then

    c* ⊕ c0 = H_k(r) ⊕ m_b ⊕ H_k(r) = m_b,

so A recovers m_b, compares it to m0, m1, and wins with probability 1 (two-time pad).

*Reuse bound:* let r* be the challenge randomizer and r_1, …, r_q the randomizers of the q(n) oracle queries. Each r_i is uniform and independent of r*, so Pr[r_i = r*] = 2^{-n}. By the union bound,


For polynomial q(n) this is negligible, since 2^n grows faster than any polynomial.

*Support for CPA security (sketch):*
1. Replace H_k by a truly random function f. By PRF security, A's success changes by at most negl(n); otherwise A yields a PRF distinguisher.
2. In the ideal world, if Bad does not occur, f(r*) is fresh and uniform and independent of all oracle answers, so c* is uniform and independent of b, and A guesses correctly with probability exactly 1/2.
3. Therefore

       Pr[A succeeds] ≤ 1/2 + q(n)/2^n + negl(n) = 1/2 + negl(n).

So the scheme is CPA-secure, assuming H is a secure PRF and r is fresh and uniform in each encryption.