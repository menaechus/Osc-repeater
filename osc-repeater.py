from pythonosc import dispatcher, osc_server, udp_client
# from pythonosc.dispatcher import Dispatcher
import netifaces as ni
import threading
import tkinter as tk
from tkinter import messagebox
import json

# Get the IP addresses of the machine
def get_ips():
    ips = []
    for interface in ni.interfaces():
        try:
            ip = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
            ips.append(ip)
        except KeyError:
            pass
    # ips.append('0.0.0.0')  # for broadcast
    return ips

# Set the maximum number of lines
MAX_LINES = 1000

def forward_osc(addr, *args):
    client.send_message(addr, args)
    # print(f"Forwarded message: {addr} {args}")
last_address = None

def on_message(address, *args):
    global last_address
    # print(f"Received message: {address} {args[0]}")
    if terminal_text is not None:
        if address == last_address:
            # Delete the last line
            terminal_text.delete("end-2l", "end-1c")
        # Insert the new message
        terminal_text.insert(tk.END, f"{address} {args[0]}\n")
    last_address = address

# Create a dispatcher and register the forward_osc function to it
dispatcher = dispatcher.Dispatcher()
dispatcher.map("*", on_message)
dispatcher.set_default_handler(forward_osc)

# Create an OSC server and client
server = None
client = udp_client.SimpleUDPClient('0.0.0.0', 8001)

# Create a new thread for the server
server_thread = None

# Start and stop the server
def start_server():
    global server, server_thread
    if server_thread and server_thread.is_alive():
        messagebox.showerror("Error", "Server is already running!")
        return
    try:
        input_port = int(input_port_entry.get())
        output_port = int(output_port_entry.get())
        server = osc_server.ThreadingOSCUDPServer(('0.0.0.0', input_port), dispatcher)
        client._port = output_port
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.start()
        print(f"Server started. Listening on port {input_port}. Forwarding to port {output_port}.")
    except ValueError:
        messagebox.showerror("Error", "Invalid port number!")

# Create a new window for the terminal
terminal_window = None
terminal_text = None

def toggle_terminal():
    global terminal_window, terminal_text
    if terminal_window is None or not tk.Toplevel.winfo_exists(terminal_window):
        # Create a new window and a text widget
        terminal_window = tk.Toplevel(root)
        terminal_window.title("Terminal")
        terminal_text = tk.Text(terminal_window)
        terminal_text.pack(expand=True, fill='both')  # Make the Text widget fill the window
    else:
        # Destroy the window if it already exists
        terminal_window.destroy()
        terminal_window = None
        terminal_text = None

def stop_server():
    global server, server_thread
    if server_thread and server_thread.is_alive():
        server.shutdown()
        server.server_close()
        server_thread = None
        print("Server stopped.")

# Save and load the ports and address to/from a JSON file
def save_to_json():
    data = {
        "input_port": input_port_entry.get(),
        "output_port": output_port_entry.get(),
        "address": client._address
    }
    with open("config.json", "w") as f:
        json.dump(data, f)

def load_from_json():
    try:
        with open("config.json", "r") as f:
            data = json.load(f)
        input_port_entry.delete(0, tk.END)  # Delete existing text
        input_port_entry.insert(0, data["input_port"])  # Insert loaded value
        output_port_entry.delete(0, tk.END)  # Delete existing text
        output_port_entry.insert(0, data["output_port"])  # Insert loaded value
        client._address = data["address"]
    except FileNotFoundError:
        messagebox.showerror("Error", "No config file found!")

# Create the main window
root = tk.Tk()
root.title("OSC Repeater")
root.resizable(False, False)  # Prevent the window from being resized


def select_ip():
    selection = listbox.curselection()
    if not selection:
        messagebox.showerror("Error", "No IP selected!")
        return
    client._address = listbox.get(selection[0])
    print(f"Selected IP: {client._address}")

listbox = tk.Listbox(root)
for ip in get_ips():
    listbox.insert(tk.END, ip)
listbox.pack(padx=10, pady=5)

select_button = tk.Button(root, text="Select IP", command=select_ip, padx=10, pady=5)
select_button.pack(padx=10, pady=5)

input_port_label = tk.Label(root, text="Input Port:")
input_port_label.pack(padx=10, pady=5)

input_port_entry = tk.Entry(root)
input_port_entry.insert(0, '7000')  # Set default input port
input_port_entry.pack(padx=10, pady=5)

output_port_label = tk.Label(root, text="Output Port:")
output_port_label.pack(padx=10, pady=5)

output_port_entry = tk.Entry(root)
output_port_entry.insert(0, '7001')  # Set default output port
output_port_entry.pack(padx=10, pady=5)

start_button = tk.Button(root, text="Start Server", command=start_server, padx=10, pady=5)
start_button.pack(padx=10, pady=5)

stop_button = tk.Button(root, text="Stop Server", command=stop_server, padx=10, pady=5)
stop_button.pack(padx=10, pady=5)

save_button = tk.Button(root, text="Save Config", command=save_to_json, padx=10, pady=5)
save_button.pack(padx=10, pady=5)

load_button = tk.Button(root, text="Load Config", command=load_from_json, padx=10, pady=5)
load_button.pack(padx=10, pady=5)

# Create a button to toggle the terminal window
toggle_button = tk.Button(root, text="Toggle Terminal", command=toggle_terminal, padx=10, pady=5)
toggle_button.pack(padx=10, pady=5)

load_from_json()

def on_close():
    stop_server()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)

root.mainloop()

