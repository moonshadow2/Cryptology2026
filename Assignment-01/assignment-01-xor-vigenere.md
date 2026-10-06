# Assignment 1: Repeating-Key XOR

> **Points:** 100 (+5 optional bonus)
>
> **Work mode:** Individual

## 1. Purpose and Learning Objectives

In this assignment, you will implement and analyze a byte-oriented analogue of the Vigenère cipher. Classical Vigenère encryption adds letters modulo 26; this construction XORs each plaintext byte with a byte from a repeating key. We will call it **repeating-key XOR**.

By completing the assignment, you should be able to:

1. distinguish text, byte strings, and hexadecimal representations;
2. translate a mathematical specification into a correct program;
3. test the functional correctness and boundary behavior of a private-key encryption scheme; and
4. explain, using explicit attack equations, why reuse of a short key stream compromises confidentiality and why encryption alone does not provide integrity.

This construction is intentionally insecure. It is suitable for learning, not for protecting real data.

You may use your language's standard library. Apart from accessing the operating system's secure random-number generator, you may not delegate the cipher operation to a cryptographic library: implement the byte-wise XOR loop yourself.

## 2. Formal Specification

Let $\mathbb{B}=\{0,1,\ldots,255\}$ denote the set of byte values. The message space is $\mathbb{B}^*$, including the empty string, and the key space is $\mathbb{B}^+$, excluding the empty string.

For a message $m=m_0m_1\ldots m_{n-1}$ and key $k=k_0k_1\ldots k_{\ell-1}$, encryption returns a ciphertext $c=c_0c_1\ldots c_{n-1}$ of the same length, where

$$
c_i=m_i\oplus k_{i\bmod \ell}
\qquad\text{for }0\leq i<n.
$$

Decryption is defined by

$$
m_i=c_i\oplus k_{i\bmod \ell}
\qquad\text{for }0\leq i<n.
$$

Correctness follows from the identities $x\oplus x=0$ and $x\oplus 0=x$:

$$
\bigl(m_i\oplus k_{i\bmod \ell}\bigr)\oplus k_{i\bmod \ell}=m_i.
$$

### 2.1 Key generation

On input a positive integer $\ell$, $\mathsf{Gen}(\ell)$ must obtain exactly $\ell$ bytes from the operating system's cryptographically secure random-number generator. Its command-line representation is the lowercase hexadecimal encoding of those bytes.

Do not use a general-purpose pseudorandom-number generator such as Python's `random`, C's `rand`, or Java's `java.util.Random`. Appropriate standard-library interfaces include Python's `secrets.token_bytes`, Go's `crypto/rand`, and Java's `SecureRandom`.

### 2.2 Representations

The core cipher operates on byte strings, not characters.

- The `encrypt` interface converts plaintext from Unicode text to bytes using UTF-8.
- Keys and ciphertexts cross the command-line interface as hexadecimal; all program output must use canonical lowercase.
- The `decrypt` interface converts recovered bytes to Unicode text using strict UTF-8 decoding.
- Hexadecimal is only an external representation. Do not XOR the character codes of hexadecimal digits.

For example, the text `A` is the one-byte string `41` in hexadecimal, while the literal text `41` is the two-byte string `3431`.

## 3. Program Requirements

Submit one program implementing the following interface:

```text
xor_vigenere keygen  --length <positive integer>
xor_vigenere encrypt --key <hex> --text <UTF-8 string>
xor_vigenere decrypt --key <hex> --ciphertext <hex>
```

The executable may be a compiled binary, a script, or a documented language-specific invocation. If your command differs from the interface above, the `README.md` must give exact equivalent commands.

### 3.1 Required behavior

Your program must satisfy all of the following requirements.

1. `keygen` prints exactly $2\ell$ lowercase hexadecimal characters followed by the conventional output newline.
2. `encrypt` parses the key, UTF-8 encodes the text, encrypts all message bytes, and prints lowercase hexadecimal ciphertext.
3. `decrypt` parses the key and ciphertext, decrypts all ciphertext bytes, strictly decodes the result as UTF-8, and prints the recovered text.
4. Encryption and decryption accept an empty message or ciphertext.
5. The byte-oriented core function accepts arbitrary byte strings, including bytes that are not valid UTF-8.
6. No operation silently changes its input. In particular, encryption must preserve spaces and must not append a newline to the plaintext.

Keep cipher logic separate from argument parsing and display logic. At minimum, expose a core function equivalent to

```text
xor_repeating(data: bytes, key: bytes) -> bytes
```

Because XOR is self-inverse, the same core function may be used for encryption and decryption.

### 3.2 Input validation and failures

Reject each of the following inputs:

- an empty key;
- an odd-length hexadecimal key or ciphertext;
- a key or ciphertext containing a character outside `0`–`9`, `a`–`f`, and `A`–`F`;
- a key or ciphertext with leading or trailing whitespace;
- a zero, negative, non-integer, or missing key length; and
- decrypted bytes that are not valid UTF-8.

For an expected input error, print a concise diagnostic to standard error, return a nonzero exit status, and do not print a language stack trace. Do not print a partial result to standard output.

## 4. Required Tests

Submit an automated test suite. A correct implementation with weak or missing tests does not receive full credit. The suite must include:

1. all three known-answer tests in Table 1;
2. round-trip tests establishing $\mathsf{Dec}_k(\mathsf{Enc}_k(m))=m$;
3. the empty message;
4. a message longer than the key, so that the key repeats;
5. a key longer than the message;
6. a UTF-8 message containing at least one multibyte character;
7. arbitrary non-text bytes passed directly to the byte-oriented core function;
8. one rejection test for every invalid-input class in Section 3.2; and
9. a key-generation test checking format and length.

**Table 1. Known-answer tests.** Every table entry is a byte string represented in hexadecimal.

| Plaintext | Key | Expected ciphertext |
|---|---|---|
| `41747461636b206174206461776e21` | `494345` | `08373128202e6922316927243e2d64` |
| `68656c6c6f` | `6b6579` | `030015070a` |
| `00010203feff` | `a55a` | `a55ba7595ba5` |

All tests other than the key-generation test must be deterministic. The key-generation test must check observable properties, such as length and valid lowercase hexadecimal, rather than expect a fixed random value. A statistical randomness test is neither required nor appropriate here.

## 5. Security Analysis

Submit `analysis.md` containing concise, rigorous answers to the following questions. Target 500–750 words in total. State any assumptions you make and show the intermediate equations needed to support each conclusion.

1. **Correctness.** Prove that $\mathsf{Dec}_k(\mathsf{Enc}_k(m))=m$ for every $m\in\mathbb{B}^*$ and every $k\in\mathbb{B}^+$. Your proof must address messages of arbitrary length, including the empty message.
2. **Known plaintext.** Suppose an attacker knows $m_i$ and the corresponding $c_i$. Derive the key byte the attacker learns. Identify every other message position encrypted with that same key byte.
3. **Key reuse.** Suppose equal-length messages $m$ and $m'$ are encrypted under the same repeating key, both beginning at key position zero, producing $c$ and $c'$. Derive $c_i\oplus c_i'$ and explain precisely what the cancellation reveals and what it does not reveal immediately.
4. **One-time pad comparison.** State the key-distribution, uniformity, length, and single-use conditions required by a one-time pad. Identify which conditions repeating-key XOR violates when $\ell<n$ or when a key is reused across messages.
5. **Security limits.** Consider two cases separately: (a) a short key that repeats within a message, and (b) a uniformly random key at least as long as the message that is never reused. Explain the confidentiality obtained in each case. Then explain why even case (b) does not provide ciphertext integrity or authenticity and why secure key distribution remains necessary.

You may consult course materials and properly cited external sources, but the analysis must be written in your own words. Use one consistent citation style. No citation is needed for algebra that you derive yourself.

## 6. Submission Package

Submit a single archive or repository directory with the following structure:

```text
assignment-01/
├── README.md
├── analysis.md
├── <source files>
└── <test files>
```

The `README.md` must provide:

- your name;
- the programming language and version;
- exact commands for building, running, and testing the submission from a clean environment;
- any assumptions or known limitations; and
- a disclosure of permitted assistance, including any generative-AI tools used, what they contributed, and how you verified their output.

Do not submit generated build artifacts, virtual environments, dependency caches, secret keys, or unrelated files. The grader must be able to reproduce your results using only the files and commands you document.

## 7. Grading Rubric

| Criterion | Points |
|---|---:|
| Correct byte-wise repeating-key XOR implementation | 25 |
| Correct key-generation, encryption, and decryption interfaces | 15 |
| Correct UTF-8, hexadecimal, and arbitrary-byte handling | 10 |
| Complete validation and controlled error behavior | 10 |
| Automated tests and required-case coverage | 20 |
| Security analysis and mathematical reasoning | 15 |
| Code organization, documentation, and reproducibility | 5 |
| **Total** | **100** |

Submissions that cannot be executed using their documented commands may lose credit in every affected category. Tests that merely restate the implementation, without checking independently specified outputs or properties, receive limited credit.

## 8. Academic Integrity and Safety

Follow the course academic-integrity policy. You may discuss general course concepts with classmates, but unless the instructor explicitly authorizes collaboration, all submitted code, tests, and prose must be your own. Cite any code or ideas adapted from external sources and disclose tool assistance as required in Section 6.

Never use this cipher to protect credentials, personal information, files, or network traffic. Real systems should use a well-reviewed authenticated-encryption construction from a reputable cryptographic library.

## 9. Optional Extension: Ciphertext Malleability (+5 points)

Write a program or automated test showing how an attacker can change one chosen plaintext byte by modifying only the corresponding ciphertext byte, without learning the key. If the original byte is $m_i$ and the attacker wants it to decrypt as $\widehat{m}_i$, derive and apply

$$
c_i'=c_i\oplus m_i\oplus\widehat{m}_i.
$$

State what the attacker must know or correctly guess, demonstrate the modified decryption, and explain in at most 200 words why the attack succeeds. Bonus work does not replace any required component.
