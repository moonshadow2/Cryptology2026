# Von Neumann Extractor — Written Assignment
**By:** Savar Shrestha

---

## Problem 1 — Mechanics

Input 1: 0010110110001011101 (19 bits; trailing 1 discarded)

| Pair | Bits | Output |
|------|------|--------|
| 0 | 00 | rejected |
| 1 | 10 | 1 |
| 2 | 11 | rejected |
| 3 | 01 | 0 |
| 4 | 10 | 1 |
| 5 | 00 | rejected |
| 6 | 10 | 1 |
| 7 | 11 | rejected |
| 8 | 10 | 1 |

Output: 10111

Input 2: 1010101010 (10 bits, even)

Every pair is (1,0) → accepted, giving 1. Output: 11111

**Is the output balanced?** 

No, all five bits are 1, even though the input has equal zeros and ones. This is not a flaw and the extractor guarantees uniformity in the distribution of Z over a random source, not for a single fixed string.

---

## Problem 2 — Correctness

### Part (a)

Since $X_{2i}$ and $X_{2i+1}$ are independent with bias $p$:

$$\Pr[(X_{2i}, X_{2i+1}) = (0,1)] = (1-p)p = p(1-p)$$
$$\Pr[(X_{2i}, X_{2i+1}) = (1,0)] = p(1-p)$$

The two mixed pairs are equally likely. The output bit is 1 if the pair is 10, so:

$$\Pr[\text{out} = 1 \mid \text{accepted}] = \frac{p(1-p)}{p(1-p)+p(1-p)} = \frac{1}{2}$$

for every $p \in (0,1)$.

### Part (b)

Fix any pattern $(a_0,\ldots,a_{N-1})$ with k accepted pairs. For each accepted pair i, part (a) gives $\Pr[B_i = 0 \mid A_i=1] = \Pr[B_i=1 \mid A_i=1] = \tfrac{1}{2}$.
The bits of distinct pairs are disjoint and i.i.d., so pairs $i \neq j$ are independent even after conditioning on their acceptance indicators. So, the k given bits are mutually independent and uniform given the pattern.
For any $z \in \{0,1\}^k$, the conditional probability $\Pr[Z=z \mid \text{pattern}] = 2^{-k}$ is the same for every pattern with exactly $k$ accepted pairs. Averaging over all such patterns:
$$\Pr[Z = z \mid L = k] = \sum_{\text{patterns}} \Pr[Z=z \mid \text{pattern}]\,\Pr[\text{pattern}\mid L=k] = 2^{-k} \qquad \blacksquare$$

### Part (c)

**Why condition on L=k?**
Without conditioning, Z is a variable length string. The strings 0 and 00 live in different output spaces; comparing their probabilities directly is meaningless. Fixing L=k restricts to a common space $\{0,1\}^k$ where uniformity is well defined.

**Numerical example ($p = \tfrac{1}{2}$, $N=2$).** 
Each pair is accepted with probability $2\cdot\tfrac{1}{2}\cdot\tfrac{1}{2} = \tfrac{1}{2}$, so:

$$\Pr[L=0]=\tfrac{1}{4},\quad \Pr[L=1]=\tfrac{1}{2},\quad \Pr[L=2]=\tfrac{1}{4}$$

$$\Pr[Z = \mathtt{0}] = \Pr[L=1]\cdot\tfrac{1}{2} = \frac{1}{2}\cdot\frac{1}{2} = \boxed{\frac{1}{4}}$$

$$\Pr[Z = \mathtt{00}] = \Pr[L=2]\cdot\tfrac{1}{4} = \frac{1}{4}\cdot\frac{1}{4} = \boxed{\frac{1}{16}}$$

These differ ($\tfrac{1}{4} \neq \tfrac{1}{16}$) which confirms that the condition on L is essential.

---

## Problem 3 — Unequal Biases Within a Pair

Let $\Pr[X_{2i}=1]=p$ and $\Pr[X_{2i+1}=1]=q$, with both bits still independent.

$$\Pr[(0,1)] = (1-p)q, \qquad \Pr[(1,0)] = p(1-q)$$

$$\Pr[\text{out}=1 \mid \text{accepted}] = \frac{p(1-q)}{(1-p)q + p(1-q)}$$

**When is this $\tfrac{1}{2}$?** 
Setting the numerator equal to half the denominator:

$$2p(1-q) = (1-p)q + p(1-q) \implies p(1-q) = (1-p)q \implies p = q$$

So the output is unbiased if and only if $p = q$.

**At $p=\tfrac{1}{2},\; q=\tfrac{1}{4}$:**

$$\frac{\tfrac{1}{2}\cdot\tfrac{3}{4}}{\tfrac{1}{2}\cdot\tfrac{1}{4}+\tfrac{1}{2}\cdot\tfrac{3}{4}} = \frac{3/8}{1/8+3/8} = \frac{3/8}{1/2} = \frac{3}{4}$$

Every given bit is 1 with probability $\frac{3}{4}$ — heavily biased.

**A $(p,q)$ making every given bit constant.** 
Take $p=1,\;q=0$: then $\Pr[(0,1)]=0$ and $\Pr[(1,0)]=1$, so every accepted pair is 10 and every output bit is 1.

What matters is the symmetry $\Pr[(0,1)]=\Pr[(1,0)]$ within each pair, i.e., $p=q$ within that pair.

---

## Problem 4 — Unbiased Output Can Still Be Dependent

Let $X_0$ be a fair coin; each subsequent bit copies its predecessor with probability $\tfrac{3}{4}$.

### Part (a): Marginal uniformity

**Claim:** 
$\Pr[X_i=1]=\tfrac{1}{2}$ for all $i$.

Base: $\Pr[X_0=1]=\tfrac{1}{2}$. 
Step: assuming $\Pr[X_i=1]=\tfrac{1}{2}$,

$$\Pr[X_{i+1}=1] = \frac{3}{4}\cdot\frac{1}{2} + \frac{1}{4}\cdot\frac{1}{2} = \frac{1}{2}$$

**Pair probabilities.** 
$\Pr[(X_{2i},X_{2i+1})=(0,1)] = \tfrac{1}{2}\cdot\tfrac{1}{4} = \tfrac{1}{8}$, and same for $(1,0)$. So $\Pr[\text{out}=1\mid\text{accepted}]=\tfrac{1}{2}$: every output bit is unbiased.

### Part (b): Dependent outputs

Condition on two consecutive pairs both being accepted. The four valid 4 bit strings and their probabilities (using $\Pr[x_0,x_1,x_2,x_3]=\tfrac{1}{2}\cdot P_{x_0x_1}\cdot P_{x_1x_2}\cdot P_{x_2x_3}$):

| String | Probability | $B_1$ | $B_2$ | Agree? |
|--------|------------|-------|-------|--------|
| 0101 | $\tfrac{1}{2}(\tfrac{1}{4})^3 = \tfrac{1}{128}$ | 0 | 0 | ✓ |
| 0110 | $\tfrac{1}{2}\cdot\tfrac{1}{4}\cdot\tfrac{3}{4}\cdot\tfrac{1}{4} = \tfrac{3}{128}$ | 0 | 1 | ✗ |
| 1001 | $\tfrac{3}{128}$ | 1 | 0 | ✗ |
| 1010 | $\tfrac{1}{128}$ | 1 | 1 | ✓ |

Total: $\tfrac{8}{128}=\tfrac{1}{16}$. Probability of agreement:

$$\Pr[B_1=B_2 \mid \text{both accepted}] = \frac{1/128+1/128}{8/128} = \frac{2}{8} = \frac{1}{4}$$

Under independence this would be $\tfrac{1}{2}$. The output bits agree with probability $\tfrac{1}{4}$, which is far from independent.

### Part (c): What fails and what survives

**Fails:**
Mutual independence of given bits. That step required bits of distinct pairs to be independent which is true for i.i.d. sources but not here, since $X_1$ and $X_2$ are correlated by the Markov chain.

**Survives:** 
Marginal uniformity of each output bit, as shown above.

**Lesson:** 
Checking for bias alone cannot confirm an extractor. An output can pass every single bit frequency test while still being far from uniform, because bias is a marginal property and uniformity is joint. A complete test must also verify independence across output bits.

---

## Problem 5 — Yield

**Acceptance probability.**
A pair is accepted if it is 01 or 10:

$$\Pr[\text{accepted}] = 2p(1-p)$$

Each accepted pair gives 1 bit from 2 input bits, so:

$$\text{yield} = \frac{2p(1-p)\cdot 1}{2} = p(1-p) \text{ bits per input bit}$$

**Comparison with entropy:**

| $p$ | VN yield $p(1-p)$ | $H(p)$ | Fraction of entropy extracted |
|-----|------------------|--------|-------------------------------|
| 0.50 | 0.2500 | 1.0000 | 25.0% |
| 0.75 | 0.1875 | 0.8113 | 23.1% |
| 0.99 | 0.0099 | 0.0808 | 12.3% |

The Von Neuman yield is always well below $H(p)$, and the gap widens as $p$ approaches 0 or 1.

**Why the gap?** 
Rejected pairs (00 and 11) carry information that Von Neuman discards. A 00 pair is evidence that $p$ is small, and a 11 pair is evidence that $p$ is large. The pattern of rejections is correlated with the source bias and contains recoverable entropy.

---

## Problem 6 — Scope of the Guarantee

**Claim.** 
For any deterministic $f:\{0,1\}^n\to\{0,1\}$, there exists a source $X$ with $H_\infty(X)\ge n-1$ on which $f(X)$ is constant.

**Proof.** 
Let $S_b = f^{-1}(b)$. Since $|S_0|+|S_1|=2^n$, at least one set has size $\ge 2^{n-1}$; call it $S_b$. Let $X$ be uniform on $S_b$. Then:

1. $f(X)=b$ with probability 1 (constant output).
2. $H_\infty(X) = \log_2|S_b| \ge \log_2 2^{n-1} = n-1$.

So $f$ fails to extract randomness from $X$, for every choice of $f$. No deterministic extractor is universal at min-entropy $n-1$. $\blacksquare$

**Reconciliation with Problem 2.** 
Von Neuman is correct only for a specific source model, not for all high-entropy sources. Problem 6 says no deterministic function can be universal and Von NeumanN is no exception.
