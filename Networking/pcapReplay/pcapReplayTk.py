import tkinter as tk
from tkinter import filedialog, messagebox
from scapy.all import rdpcap, sendp
from scapy.arch.windows import get_windows_if_list

loaded_packets = None
selected_file = None
iface_map = {}  # Friendly name → Scapy interface (NPF device)


def load_interfaces():
    interfaces = get_windows_if_list()
    friendly_names = []
    for iface in interfaces:
        name = iface.get("name")
        description = iface.get("description")
        guid = iface.get("guid")
        full_npf_name = f"\\Device\\NPF_{guid}"
        label = f"{name} - {description}"
        iface_map[label] = full_npf_name
        friendly_names.append(label)
    return friendly_names


def select_file():
    global loaded_packets, selected_file
    file_path = filedialog.askopenfilename(
        title="Select a PCAP File", filetypes=[("PCAP files", "*.pcap")]
    )
    if file_path:
        try:
            loaded_packets = rdpcap(file_path)
            selected_file = file_path
            file_label.config(text=f"Selected: {file_path}")
            messagebox.showinfo("Success", f"Loaded {len(loaded_packets)} packet(s).")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load PCAP:\n{e}")
            loaded_packets = None
            selected_file = None
            file_label.config(text="No file selected")


def send_packet():
    if loaded_packets is None:
        messagebox.showwarning("No Packets", "Please select a PCAP file first.")
        return

    selected_label = iface_var.get()
    npf_iface = iface_map.get(selected_label)

    if not npf_iface:
        messagebox.showerror("Interface Error", f"Interface '{selected_label}' not found.")
        return

    try:
        sendp(loaded_packets, iface=npf_iface, verbose=True)
        messagebox.showinfo("Sent", f"Sent {len(loaded_packets)} packet(s) on '{selected_label}'")
    except Exception as e:
        messagebox.showerror("Send Error", f"Failed to send packets:\n{e}")


# --- GUI Setup ---
root = tk.Tk()
root.title("PCAP Packet Sender")

main_frame = tk.Frame(root, padx=10, pady=10)
main_frame.pack()

file_label = tk.Label(main_frame, text="No file selected", fg="gray")
file_label.pack(pady=(0, 10), anchor="w")

select_button = tk.Button(main_frame, text="Select PCAP File", command=select_file)
select_button.pack(fill="x", pady=(0, 10))

iface_label = tk.Label(main_frame, text="Select Interface:")
iface_label.pack(anchor="w")

iface_var = tk.StringVar()
available_interfaces = load_interfaces()
iface_dropdown = tk.OptionMenu(main_frame, iface_var, *available_interfaces)
iface_dropdown.pack(fill="x", pady=(0, 10))

send_button = tk.Button(main_frame, text="Send Packet", command=send_packet)
send_button.pack(fill="x")

root.mainloop()
