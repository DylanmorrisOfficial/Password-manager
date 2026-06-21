# Threat Model

## Purpose

This document describes the security assumptions, assets, threats, and mitigations for the Password Manager application.

---

## System Overview

The Password Manager is a local desktop application that allows users to store credentials in encrypted vault files.

The application provides:

* User registration
* User authentication
* Password generation
* Encrypted vault storage
* Password retrieval and management

---

## Assets to Protect

The following assets are considered sensitive:

### Master Passwords

Used to authenticate users.

### Stored Credentials

Usernames, passwords, and notes stored within vault entries.

### Derived Encryption Keys

Encryption keys derived from the user's master password and used to encrypt and decrypt vault data.

### Vault Files

Encrypted vault files stored on disk.

---

## Security Goals

### Confidentiality

Only authorized users should be able to access stored credentials.

### Integrity

Stored vault data should not be modified without detection.

### Availability

Authorized users should be able to access their vault data when needed.

---

## Threat Actors

### Casual Attacker

An attacker who gains access to vault files but does not know the master password.

### Malicious Local User

A user with access to the same computer attempting to view or modify stored data.

### Physical Attacker

Someone who gains access to the storage device containing vault files.

### Malware

Malicious software running on the user's machine.

---

## Threats and Mitigations

### Threat: Password Database Theft

#### Description

An attacker copies encrypted vault files from disk.

#### Mitigation

* Vault files are encrypted using Fernet authenticated encryption.
* Encryption keys are derived from the user's master password using PBKDF2-HMAC-SHA256.
* Encryption keys are not stored on disk.
* Vault contents are not stored in plaintext.

---

### Threat: Master Password Disclosure

#### Description

An attacker gains access to stored authentication data.

#### Mitigation

* Passwords are hashed using PBKDF2-HMAC-SHA256.
* Each password uses a unique random salt.
* Passwords are never stored in plaintext.

---

### Threat: Brute Force Attacks

#### Description

An attacker attempts to guess a user's master password.

#### Mitigation

* PBKDF2 uses 100,000 iterations.
* Password complexity requirements are enforced.
* Unique salts prevent precomputed rainbow table attacks.

---

### Threat: Weak Generated Passwords

#### Description

Generated passwords are predictable.

#### Mitigation

* Password generation uses Python's cryptographically secure `secrets` module.
* Generated passwords contain uppercase letters, lowercase letters, numbers, and symbols.

---

### Threat: Unauthorized Vault Modification

#### Description

An attacker modifies encrypted vault files.

#### Mitigation

* Fernet provides authenticated encryption and integrity checking.
* Modified ciphertext cannot be successfully decrypted.

---

## Known Limitations

### Offline Password Guessing Risk

If an attacker obtains:

* The encrypted vault file
* Authentication data containing salts and password hashes

they may attempt offline password guessing attacks against weak master passwords.

Security therefore depends heavily on the strength of the user's master password and the computational cost of PBKDF2.

### Trusted Environment Assumption

The application assumes the operating system is trusted.

The application does not protect against:

* Keyloggers
* Privileged malware
* Memory scraping malware
* Fully compromised operating systems

---

## Assumptions

This threat model assumes:

* Users choose reasonably strong master passwords.
* The operating system is trusted.
* Cryptographic libraries are implemented correctly.
* Sensitive files are stored on trusted devices.

---

## Future Improvements

* Increase PBKDF2 iteration count or migrate to Argon2id.
* Implement automatic vault backups.
* Add password expiration and reuse detection.
* Support multi-factor authentication.

---

## Residual Risk

Despite encryption and password hashing, users remain vulnerable if:

* The operating system is compromised.
* Malware captures credentials during entry.
* Weak master passwords are chosen.

Users should maintain good endpoint security and choose strong master passwords.
