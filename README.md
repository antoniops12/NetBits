# 🧪 NetBits: Python Networking Tools

Welcome to **NetBits**, a growing collection of lightweight, scriptable tools for network engineers, security analysts, and packet wizards. Whether you're crafting custom Ethernet frames, dissecting packets, or automating CLI flows, these scripts are built to give you power with clarity—and just the right touch of Pythonic flair.

---

## ⚙️ What You’ll Find Here

Each tool is designed to be:
- **Modular** – Plug into other workflows or use standalone
- **Readable** – Clear structure, minimal dependencies, generously commented
- **Practical** – Focused on real-world tasks and learning-friendly

Think of this repo as your toolkit for exploring and engineering networks—one Python script at a time.

---

## ✨ Example Scripts

| Script | Description |
|--------|-------------|
| `eth_frame_builder.py` | GUI tool for crafting raw Ethernet frames from HEX and exporting to `.pcap` |
| *(more coming soon)* | Wireshark dissector helpers, packet fuzzers, packet replayers, etc. |

---

## 📦 Requirements

Each script includes its own dependencies section, but commonly used packages include:

- [`scapy`](https://scapy.net/) – packet crafting and manipulation
- `tkinter` – native GUI support (bundled with most Python installations)

Install requirements using:
```bash
pip install -r requirements.txt
