# PCAP Replay Tool v1.0 - Ernesto Antonio Peña Serrato: eantoniops12@gmail.com

A simple GUI application to replay `.pcap` files over selected network interfaces on Windows using Python and Scapy.

Built using Python, Scapy, and Tkinter.

---

## ✅ Features

- Select and load a `.pcap` file using a file dialog
- Automatically detects available Windows network interfaces
- Sends all packets from the `.pcap` over the selected interface
- Built-in GUI with no need to touch the command line
- Exportable as a standalone `.exe` for Windows

---

## 🖥️ Requirements

This tool is currently built for **Windows 10 or 11**, with administrative privileges.

### 🔧 System Requirements

| Component              | Required | Notes                                                                 |
|------------------------|----------|-----------------------------------------------------------------------|
| Python 3.10+           | ✅       | [Download Python](https://www.python.org/downloads/windows/)         |
| Npcap (with WinPcap API compatibility) | ✅ | [Npcap installer](https://npcap.com/#download)                       |
| Admin privileges       | ✅       | Required to send raw packets with Scapy                              |

### 📦 Python Dependencies

Install using pip:

```bash
pip install scapy
pip install pyinstaller  # optional, for building .exe
