# Task 3 — Strengthening User Authentication & Data Security

**Internee.pk Cybersecurity Internship — Task 3 of 3**
**Author:** Soban Shehzad, University of Education, Lahore

## 📌 Overview

This task implements and verifies three complementary security controls to protect user accounts and sensitive data:

| Control | Purpose |
|---|---|
| **2FA (Google Authenticator / TOTP)** | Controls *who* can authenticate |
| **OAuth 2.0** | Controls *what* an application is allowed to access |
| **AES-256 Encryption** | Protects the *data itself*, even if stolen |

Test data for the encryption demo was generated using [Mockaroo](https://www.mockaroo.com/), avoiding the need to use real records from Internee.pk's staging database.

## 🎯 Objective

Strengthen user authentication and data security to protect sensitive information, per the task brief:
- Implement 2FA using Google Authenticator
- Use OAuth 2.0 for secure, seamless sign-in
- Encrypt sensitive data with AES-256

## 🔑 1. Two-Factor Authentication (2FA)

- Generated a TOTP secret + QR code (RFC 6238 compliant).
- Scanned the QR code into Google Authenticator; confirmed live 6-digit codes matched between the app and the generator.
- Built a small Python script (`folder_lock_2fa.py`) that independently recomputes the expected TOTP code from the shared secret and current time, and gates access to a real project folder based on a live code entered by the user.
- Verified both outcomes: correct code → folder opens; incorrect code → access denied.

**Note:** This demonstrates the 2FA *verification logic* (the same check a server performs before granting access). It does not encrypt the folder or change OS-level permissions — that is handled separately by AES-256 (see below).

## 🔑 2. OAuth 2.0 Secure Sign-In

Full Authorization Code flow carried out using Google's OAuth 2.0 Playground against a real Google account:

1. **Authorization request** — requested `userinfo.email` and `userinfo.profile` scopes; user consented via Google's real sign-in/consent screen; received a one-time authorization code.
2. **Token exchange** — exchanged the authorization code for a real `access_token`, `refresh_token`, and `id_token`.
3. **Authenticated API request** — used the access token (no password) to call Google's `userinfo` endpoint and successfully retrieved the authenticated user's profile data (`200 OK`).

## 🔑 3. AES-256 Encryption

- Generated a fake sensitive user dataset (`MOCK_DATA.csv`) using Mockaroo.
- Encrypted it into a `.7z` archive using 7-Zip with AES-256 encryption and a password.
- Verified access control in both directions:
  - ❌ Incorrect password → decryption fails with a checksum/data error.
  - ✅ Correct password → archive opens cleanly, original CSV is accessible.

## 🛠️ Tools Used

- Google Authenticator (mobile app)
- RFC 6238-compliant online TOTP generator
- Python 3.14 (standard library only — `hmac`, `hashlib`, `struct`, `time`, `base64`)
- Google OAuth 2.0 Playground
- Mockaroo (fake data generation)
- 7-Zip (AES-256 encryption)

## 📸 Evidence

Screenshots for each stage (TOTP setup, script success, OAuth authorization/token exchange/profile fetch, AES-256 encryption dialog, denied/success access) are included in the full task report: `Task3_Security_Implementation_Report.docx`.

## ✅ Status

All three components implemented and independently tested with reproducible, real-world evidence.
