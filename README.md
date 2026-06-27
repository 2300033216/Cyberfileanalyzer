# 🛡️ Cyber File Analyzer

A modern **Cybersecurity File Integrity Analyzer** built with **Python** that helps users detect file changes through **SHA-256 hashing**. The application features a clean interface with **real-time status indicators**, an **AI-powered assistant**, and support for both **Dark** and **Light** themes.

---

## ✨ Key Features

### 🟢 Real-Time Scan Status

The application visually indicates the current scan state.

* 🟢 **Green Status**

  * Displayed when the application is opened.
  * Indicates that no scan has been performed yet.
  * System is ready to analyze files.

* 🔴 **Red Status**

  * Displayed after the user scans a folder.
  * Indicates that the scan has been completed.
  * Results and feedback are now available.

---

### 🤖 AI-Powered Feedback Assistant

After every scan, the integrated AI assistant automatically:

* Explains scan results in simple language.
* Detects modified, deleted, and newly created files.
* Provides cybersecurity recommendations.
* Suggests best practices to maintain file integrity.
* Generates user-friendly security feedback.

All AI-generated feedback is automatically saved in:

```text
feedback.txt
```

---

### 🔐 File Integrity Monitoring

The application secures file integrity by:

* Generating SHA-256 hashes
* Creating file snapshots
* Comparing previous and current file states
* Detecting:

  * Modified files
  * Deleted files
  * Newly added files

---

### 🌙 Theme Support

Users can personalize the interface by switching between:

* 🌙 Dark Mode
* ☀️ Light Mode

---

## 📂 Project Structure

```text
Cyberfileanalyzer/
│
├── files.py          # Main application
├── snapshot.json     # Stores file hashes and snapshots
├── feedback.txt      # AI-generated scan feedback
└── README.md
```

---

## 🚀 How It Works

### Step 1 — Open the Application

The application starts with a **Green Status Indicator**, showing that the system is ready.

```
🟢 Ready to Scan
```

---

### Step 2 — Scan Files

The user selects a folder for analysis.

During the scan, the application:

* Reads all files
* Generates SHA-256 hashes
* Compares files with the previous snapshot
* Detects any integrity changes

---

### Step 3 — Scan Completed

Once scanning finishes, the status changes to:

```
🔴 Scan Completed
```

---

### Step 4 — AI Analysis

The AI Assistant analyzes the scan results and provides:

* Security observations
* File integrity summary
* Recommendations
* Suggested actions

The generated report is saved in:

```
feedback.txt
```

---

## 📊 Workflow

```text
           Start Application
                  │
                  ▼
        🟢 Green Status (Ready)
                  │
                  ▼
          Select Folder to Scan
                  │
                  ▼
          Generate SHA-256 Hashes
                  │
                  ▼
      Compare with Previous Snapshot
                  │
                  ▼
      Detect File Integrity Changes
                  │
                  ▼
        🔴 Red Status (Completed)
                  │
                  ▼
        AI Generates User Feedback
                  │
                  ▼
      Save Results to feedback.txt
```

---

## 💻 Technologies Used

* Python
* CustomTkinter
* SHA-256 (hashlib)
* JSON
* AI-powered Feedback System
* File System APIs

---

## 🎯 Future Enhancements

* 📄 Export Scan Reports as PDF
* 📈 Scan History Dashboard
* ⚠️ Threat Severity Levels
* 📧 Email Notifications
* 📁 Multi-folder Monitoring
* ☁️ Cloud Backup
* 🦠 Malware Signature Detection
* 📊 Analytics Dashboard

---

## 👩‍💻 Author

**Shaik Manduru Niloufer**

Cybersecurity Enthusiast | Computer Science Student

---

## ⭐ Support

If you found this project useful, please consider giving it a **⭐ Star** on GitHub.

Your support helps improve the project and motivates future development.
