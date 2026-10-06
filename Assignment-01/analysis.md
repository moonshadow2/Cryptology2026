# Security Analysis: Repeating-Key XOR (Simplified)

**Notation.** Plaintext $m = m_0 \ldots m_{n-1}$, key $k = k_0 \ldots k_{\ell-1}$.
Encryption: $c_i = m_i \oplus k_{i \bmod \ell}$ ($\oplus$ = XOR).

## 1. Correctness

Decryption undoes encryption because XOR-ing the same value twice cancels out:

$$\widehat{m}_i = c_i \oplus k_{i\bmod\ell} = (m_i \oplus k_{i\bmod\ell}) \oplus k_{i\bmod\ell} = m_i.$$

This works one byte at a time, so it doesn't matter how long the message is or how it compares to the key length. It even works for the empty message: with zero bytes, there's nothing to check, so the claim holds
trivially.

## 2. Known Plaintext

If an attacker sees one plaintext/ciphertext pair $(m_i, c_i)$, they can
solve for the key byte used at that position:

$$k_{i \bmod \ell} = m_i \oplus c_i.$$

That's one key byte recovered. Because the key repeats every $\ell$ bytes, this same key byte was also used at every position $i'$ where $i' \bmod \ell = i \bmod \ell$ (i.e., $i, i+\ell, i+2\ell, \ldots$). At all
of those positions, the attacker can now read the plaintext or plant a fake ciphertext byte of their choosing.

## 3. Key Reuse

Suppose two equal-length messages $m$ and $m'$ are encrypted with the same key, both starting at key byte 0. XOR-ing the two ciphertexts together cancels the key completely:

$$c_i \oplus c_i' = (m_i \oplus k_{i\bmod\ell}) \oplus (m_i' \oplus k_{i\bmod\ell}) = m_i \oplus m_i'.$$

So the attacker learns $m_i \oplus m_i'$ — the two plaintexts' difference without ever seeing the key. This is dangerous: with real language,techniques like guessing a likely word ("crib") in one message and checking what it implies about the other, or basic letter frequency analysis, often untangle $m$ and $m'$ from there. But the XOR value by itself doesn't hand over $m_i$, $m_i'$, or any key byte directly. A single XOR difference is consistent with many possible byte pairs.

## 4. Comparison to a One Time Pad

A true one-time pad needs four things: (1) a key **at least as long** as the message, (2) a key that's **truly random** (every byte independent and uniform), (3) **used only once**, ever, and (4) delivered to the
recipient over a channel the attacker can't observe. Repeating-key XOR breaks rule (1) whenever the key is shorter than the message — the key ends up reused within a single message, which is just the Section 3 key-reuse problem happening internally, over and over. It breaks rule (3) directly if the same key is reused across separate messages. Rule (2) is only satisfied if key generation uses a proper cryptographic random source (as this assignment requires); a weak
random-number generator would violate it too.

## 5. What Security (If Any) Does This Give?

**(a) Short key that repeats.** Confidentiality is weak. Because the key repeats every $\ell$ bytes, ciphertext bytes $\ell$ apart satisfy $c_i \oplus c_{i+\ell} = m_i \oplus m_{i+\ell}$ — the same cancellation trick as Section 3, just against itself. This lets an attacker guess the key length $\ell$ (for instance by looking for repeated patterns) and
then crack each of the $\ell$ interleaved streams separately using ordinary letter-frequency analysis. For real text, this usually breaks the cipher completely.

**(b) Long, truly random key, used once.** This is a proper one-time pad, and it gives **perfect secrecy**: every possible plaintext is equally consistent with the ciphertext, so the ciphertext reveals nothing
about the message at all, no matter how much computing power the attacker has.

But even this best case gives **no protection against tampering**. XOR ciphertext is trivially editable: if an attacker knows or guesses a plaintext byte $m_i$, they can force it to decrypt to any byte they want,
$\widehat{m}_i$, by changing only the ciphertext:

$$c_i' = c_i \oplus m_i \oplus \widehat{m}_i.$$

Nothing in decryption checks whether the ciphertext was tampered with — every ciphertext of the right length decodes to *some* message, valid-looking or not. Confidentiality and tamper-protection are separate properties,
and this scheme only ever tries to provide the first.

Secure key delivery is also still required in case (b): the whole guarantee depends on the attacker never seeing the key, and since the key must be as long as the message, you need a channel that can securely carry *at least* as much data as you're trying to protect — which is exactly why one-time pads aren't practical for everyday use. Real-world systems instead use a short key with a modern authenticated-encryption algorithm (like AES-GCM or ChaCha20-Poly1305), which gives both secrecy and tamper-detection from a small, manageable key.