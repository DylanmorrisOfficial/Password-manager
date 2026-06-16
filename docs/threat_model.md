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

### Encryption Keys

Keys used to encrypt and decrypt vault data.

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

* Vault files are encrypted using Fernet encryption.
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

### Separate Encryption Key Storage

The current implementation stores the vault encryption key separately from the user's master password.

If an attacker obtains:

* The encrypted vault file
* The encryption key file

they may be able to decrypt vault contents without knowing the master password.

Future versions should derive encryption keys directly from the user's master password.

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

* Derive vault encryption keys from master passwords.

---

## Residual Risk

Despite encryption and password hashing, users remain vulnerable if:

* The operating system is compromised.
* Malware captures credentials during entry.
* Weak master passwords are chosen.
* Encryption keys are exposed.

Users should maintain good endpoint security and choose strong master passwords.
