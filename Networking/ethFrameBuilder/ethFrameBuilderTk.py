import tkinter as tk
from tkinter import messagebox, filedialog
from scapy.all import Ether, wrpcap
import binascii

def build_frame():
    hex_input = text_box.get("1.0", tk.END).strip().replace("\n", "").replace(" ", "")
    if not hex_input:
        messagebox.showwarning("Input Missing", "Please enter a HEX stream.")
        return

    try:
        frame_bytes = binascii.unhexlify(hex_input)
        eth_pkt = Ether(frame_bytes)

        # Save As dialog
        file_path = filedialog.asksaveasfilename(
            title="Save PCAP file",
            defaultextension=".pcap",
            filetypes=[("PCAP files", "*.pcap")]
        )

        if file_path:  # if user didn't cancel
            wrpcap(file_path, eth_pkt)
            messagebox.showinfo("Success", f"PCAP saved to:\n{file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{str(e)}")

# Create the GUI
root = tk.Tk()
root.title("ETH Frame Builder")

tk.Label(root, text="Enter HEX stream:").pack(anchor="w", padx=10, pady=(10,0))
text_box = tk.Text(root, height=10, width=80)
text_box.pack(padx=10, pady=5)

build_button = tk.Button(root, text="Build & Save", command=build_frame)
build_button.pack(pady=10)

root.mainloop()
