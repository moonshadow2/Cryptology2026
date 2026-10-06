# Assignment 2: Correctness of the von Neumann Extractor

> **Points:** 100
>
> **Work mode:** Individual

## 1. Purpose and Learning Objectives

Physical entropy sources produce biased, correlated bits, which must be smoothed before use as key material. This written assignment concerns the oldest such procedure, published by von Neumann in 1951. Lecture 4 covers min-entropy and smoothing.

By completing the assignment, you should be able to:

1. prove the procedure is exactly uniform for any bias
2. derive the output when each hypothesis fails
3. compare its yield against the source's entropy
4. explain why no deterministic extractor is universal

## 2. The Construction

The von Neumann extractor $\mathsf{VN}$ partitions a bit stream $x = x_0x_1\ldots x_{n-1}$ into non-overlapping pairs $(x_0,x_1), (x_2,x_3), \ldots$ and maps each separately: $01 \mapsto 0$, $10 \mapsto 1$, and $00, 11 \mapsto \varepsilon$ (nothing). Concatenate in order, discarding $x_{n-1}$ if $n$ is odd. The pairing is fixed, so a rejected pair does not re-align those after it, and an accepted pair emits its first bit $x_{2i}$.

An i.i.d. source with bias $p \in (0,1)$ emits independent $X_i$ with $\Pr[X_i = 1] = p$. For $N$ pairs of input, let $Z = \mathsf{VN}(X_0 \ldots X_{2N-1})$ and $L = |Z| \le N$.

Problem 2 needs only two properties: distinct pairs are independent, and a pair's two bits are independent with equal bias. Problem 3 drops the second, Problem 4 the first.

## 3. Problems

Justify every step and state any assumption you use. A correct result without its derivation earns limited credit.

**1. Mechanics (10 points).** Apply the extractor by hand to `0010110110001011101` and `1010101010`, giving the pairs and output. The second input has as many zeros as ones. Is its output balanced?

**2. Correctness (30 points).** Let the source be i.i.d. with bias $p$.

   a. Compute $\Pr[(X_{2i},X_{2i+1}) = (0,1)]$ and $\Pr[(X_{2i},X_{2i+1}) = (1,0)]$, and deduce $\Pr[\text{output bit} = 1 \mid \text{accepted}] = \tfrac12$ for every $p$.
   b. For each input pair $i$, let $A_i$ indicate whether it is accepted: $A_i = 1$ if the pair is $01$ or $10$, and $A_i = 0$ if it is $00$ or $11$. The acceptance pattern $(A_0,\ldots,A_{N-1})$ records the status of every input pair; only pairs with $A_i = 1$ emit a bit. Conditioned on any fixed acceptance pattern, show the emitted bits are independent and uniform. Then average over patterns with $k$ accepted pairs to get $\Pr[Z = z \mid L = k] = 2^{-k}$ for all $k \le N$ and all $z \in \{0,1\}^k$.
   c. Why must this be conditioned on $L = k$? For $p = \tfrac12$ and $N = 2$, compute the probabilities of the one-bit output $0$ and the two-bit output $00$.

**3. Unequal biases within a pair (15 points).** Let the bits be independent with $\Pr[X_i=1] = p$ for even $i$ and $q$ for odd $i$, where $p(1-q)+(1-p)q > 0$. Derive $\Pr[\text{output bit} = 1 \mid \text{accepted}]$, show it is $\tfrac12$ iff $p = q$, and evaluate it at $p = \tfrac12$, $q = \tfrac14$. Give a $(p,q)$ making every emitted bit equal. *Equal bias within each pair suffices even if it varies between pairs.*

**4. Unbiased output can still be dependent (25 points).** Let $X_0$ be a fair coin flip, and let each later bit repeat its predecessor with probability $\tfrac34$, independently. Dependence can break the guarantee, though not every dependent source fails.

   a. Show by induction that $\Pr[X_i = 1] = \tfrac12$, and that $\Pr[\text{pair} = 01] = \Pr[\text{pair} = 10] = \tfrac18$: the source and every output bit are unbiased.
   b. Condition on two adjacent pairs both being accepted. Enumerate the four 4-bit strings and show the emitted bits agree with probability $\tfrac14$, not $\tfrac12$.
   c. Which conclusion of Problem 2 fails, and which survives? What does this say about testing an extractor for bias alone?

**5. Yield (10 points).** Show a pair is accepted with probability $2p(1-p)$, so the yield is $p(1-p)$ bits per input bit. Compare it against $H(p) = -p\log_2 p - (1-p)\log_2(1-p)$, the ceiling on any extractor's yield, at $p = 0.50, 0.75, 0.99$, where $H(p) = 1.0000, 0.8113, 0.0808$. Account for the gap, and say what a rejected $00$ pair reveals about $p$.

**6. Scope of the guarantee (10 points).** Let $f : \{0,1\}^n \to \{0,1\}$ be deterministic, and let $H_\infty(X) = -\log_2 \max_x \Pr[X = x]$. Show some $X$ with $H_\infty(X) \ge n-1$ makes $f(X)$ constant, so no deterministic $f$ extracts a nearly uniform bit from every source of min-entropy $n-1$. Reconcile this with Problem 2, and say what a seeded extractor (one given a short uniform seed) adds.

## 4. Submission Package

One PDF or `analysis.md` with your name and your answers in order. Written work only, no code.
