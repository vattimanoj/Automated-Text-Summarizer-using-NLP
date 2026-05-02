# Automated Text Summarizer - Project Test Cases

This document outlines the high-level test cases for the Automated Text Summarizer application, focusing on user flows, inputs, and expected outputs.

---

## 1. User Registration Flow
Tests the logic for creating a new user account.

| Test Case ID | Description | Input | Expected Output | Screen Flow |
| :--- | :--- | :--- | :--- | :--- |
| REG-01 | Successful Registration | Valid Name, Email, Password, Profile Photo | Account created successfully; Auto-login to Dashboard | Registration Page → Dashboard |
| REG-02 | Duplicate Email | Email that already exists in DB | Error message: "Email already registered" | Stay on Registration Page |
| REG-03 | Missing Required Fields | Empty name or email | Form validation error: "Please fill all fields" | Stay on Registration Page |
| REG-04 | Password Complexity | Short password (e.g., < 6 chars) | Validation error: "Password must be at least 6 characters" | Stay on Registration Page |

---

## 2. User Login Flow
Tests user authentication and session management.

| Test Case ID | Description | Input | Expected Output | Screen Flow |
| :--- | :--- | :--- | :--- | :--- |
| LGN-01 | Successful Login | Correct Email and Password | Dashboard loads with user's stats and history | Login Page → Dashboard |
| LGN-02 | Invalid Credentials | Incorrect email or password | Error message: "Invalid credentials" | Stay on Login Page |
| LGN-03 | Unregistered User | Email not in DB | Error message: "User not found" | Stay on Login Page |
| LGN-04 | Logout Flow | Click Logout Button | Session cleared; Redirect to Login | Dashboard → Login Page |

---

## 3. Summarization Flow (Main Feature)
Tests the core functionality of generating summaries.

| Test Case ID | Description | Input | Expected Output | Screen Flow |
| :--- | :--- | :--- | :--- | :--- |
| SUM-01 | Generate Summary (Text) | Paste valid long text and click "Summarize" | AI-generated summary displayed in chat; Stats update | Dashboard (Chat) |
| SUM-02 | Document Upload | Select .pdf or .txt file | Text extracted and summary generated | Dashboard (Upload) |
| SUM-03 | Empty Input | Click Summarize with no text | Error: "Please provide text or a document" | Stay on Dashboard |
| SUM-04 | Long Text Handling | Extensively long research paper | Summary generated with abstractive logic | Dashboard (Chat) |

---

## 4. History and Sidebar Navigation
Tests interaction with previously generated summaries.

| Test Case ID | Description | Input | Expected Output | Screen Flow |
| :--- | :--- | :--- | :--- | :--- |
| HST-01 | View History Item | Click on a past summary in sidebar | Previous input and summary loaded in chat area | Dashboard Screen Update |
| HST-02 | Delete History | Click delete icon on history item | Item removed from list; Stats (document count) update | Dashboard Sidebar |
| HST-03 | New Chat | Click "New Summary" button | Chat area cleared for new input | Reset Dashboard View |
| HST-04 | Stats Refresh | Complete a summary | User statistics cards update in real-time | Sidebar Stats Update |

---

## 5. Profile Management
Tests user profile information viewing and updates.

| Test Case ID | Description | Input | Expected Output | Screen Flow |
| :--- | :--- | :--- | :--- | :--- |
| PRF-01 | View Profile | Click on Profile name/icon | Modal/Page opens with user details & photo | Dashboard → Profile Modal |
| PRF-02 | Update Profile | Change name or upload new photo | User details updated in DB and Header | Profile Modal Update |

---

> [!NOTE]
> These test cases are designed for flow verification and do not include the underlying ML model unit tests or API endpoint testing.
