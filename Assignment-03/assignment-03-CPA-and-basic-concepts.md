# Assignment 3: Pseudorandomness and CPA Security

> **Points:** 100
>
> **Work mode:** Individual

## 1. Purpose and Learning Objectives

This assignment examines pseudorandom generators (PRGs), pseudorandom functions (PRFs), pseudorandom permutations (PRPs), and indistinguishability under chosen-plaintext attack (IND-CPA).

By completing the assignment, you should be able to:

1. distinguish the definitions and security experiments for PRGs, PRFs, and PRPs
2. describe the IND-CPA experiment and its security condition
3. construct a chosen-plaintext attack against deterministic encryption
4. explain how randomized PRF-based encryption achieves CPA security and how randomizer reuse can expose plaintext

## 2. Problems

Answer each question in order. Explain and justify each answer.

**1. Key concepts (15 points, 5 points each).**

Explain the structure and functionality of each concept in your own words: its inputs and outputs, whether it is keyed, and its defining properties. Include output stretch for a PRG, a keyed family of functions for a PRF, and a keyed family of bijections with efficient inversion for a PRP. Discuss security experiments in Problem 2.

a. PRG (pseudorandom generator)

b. PRF (pseudorandom function)

c. PRP (pseudorandom permutation)

**2. Indistinguishability (20 points, 5 points each).**

a. Explain the basic idea behind computational indistinguishability in cryptography, including the role of probabilistic polynomial-time adversaries and negligible distinguishing advantage.

b. Explain how indistinguishability defines PRG security. Describe the real and ideal experiments, what the adversary receives, and the security condition. The ideal experiment supplies a uniform string of the same length as the generator's output.

c. Explain how indistinguishability defines PRF security. Describe the real and ideal experiments, the adversary's adaptive oracle access, and the security condition. The ideal oracle implements a uniformly random function with the same domain and range, giving consistent answers to repeated queries.

d. Explain how indistinguishability defines PRP security. Describe the real and ideal experiments, the adversary's adaptive oracle access, and the security condition. The ideal oracle implements a uniformly random permutation on the same domain. Use ordinary PRP security: the adversary has forward-oracle access only.

**3. Chosen-plaintext attack security (65 points).**

Consider a stateless private-key encryption scheme $\Pi = (\mathsf{Gen}, \mathsf{Enc}, \mathsf{Dec})$. Let $n$ be the security parameter, with key generation written as $k \leftarrow \mathsf{Gen}(1^n)$. The adversary is a probabilistic polynomial-time algorithm. In parts (b) and (c), the key space is $\{0,1\}^n$, and key generation samples a uniform key once and reuses it across encryptions. Justify each answer and state any assumptions you use.

a. **The security experiment (15 points).** Describe the IND-CPA experiment, including key generation, encryption-oracle access before and after the challenge, the choice of two equal-length challenge messages, and the adversary's final guess. State the CPA-security condition using the adversary's probability of guessing correctly. Explain why the challenge messages must have equal length and why the adversary may request encryptions of those messages.

b. **An explicit attack (25 points).** Let $F_k : \{0,1\}^n \to \{0,1\}^n$ be a secure pseudorandom permutation. Consider the encryption scheme $\mathsf{Enc}_k(m) = F_k(m)$, with decryption using $F_k^{-1}$. Construct a CPA adversary that distinguishes encryptions of two *distinct* messages with certainty. Specify its oracle query, challenge messages, and decision rule. Compute its success probability and explain why PRP security does not imply CPA security for this construction.

c. **Randomization and its limits (25 points).** Let $H_k : \{0,1\}^n \to \{0,1\}^n$ be a secure pseudorandom function. Consider $\mathsf{Enc}_k(m) = (r, H_k(r) \oplus m)$ for $m \in \{0,1\}^n$, where each encryption independently samples uniform $r \in \{0,1\}^n$ and the key $k$ is sampled uniformly once and reused across encryptions.

Give the decryption algorithm and explain why the attack in part (b) no longer succeeds with certainty. Explain why revealing $r$ is compatible with CPA security. Suppose an encryption of the known message $0^n$ and the challenge ciphertext use the same $r$. Show how the adversary recovers the challenge plaintext. For at most $q(n)$ encryption-oracle queries in total, before and after the challenge, bound the probability that any queried encryption uses the challenge randomizer. Explain why this bound is negligible when $q(n)$ is polynomial in $n$, and how this bound and PRF security support the CPA-security claim. **You do not need to provide a full reduction proof.**

## 3. Submission Package

One PDF or Markdown (`.md`) file with your name and your answers in order.
