import socket
import ipaddress
import threading
import queue
import csv
import time
from datetime import datetime
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class ScannerEngine:
    def __init__(self, target, ports, result_queue, log_queue, timeout=3.0):
        self.target = target
        self.ports = ports
        self.result_queue = result_queue
        self.log_queue = log_queue
        self.timeout = timeout
        self.is_running = True
        self.completed = 0
        self.lock = threading.Lock()

    def stop(self):
        self.is_running = False

    def expand_target(self):
        try:
            network = ipaddress.ip_network(self.target, strict=False)
            return [str(ip) for ip in network.hosts()]
        except ValueError:
            return [self.target]

    def grab_banner(self, sock, port):
        try:
            sock.settimeout(2.0)
            if port in [80, 443, 8080, 8443, 8000, 8888, 3000, 5000]:
                request = f"GET / HTTP/1.0\r\nHost: {self.target}\r\nUser-Agent: PyScan/1.0\r\nConnection: close\r\n\r\n"
                sock.send(request.encode())
            else:
                sock.send(b"\r\n")

            response = sock.recv(4096).decode('utf-8', errors='ignore').strip()
            if response:
                lines = response.split('\n')
                for line in lines:
                    if 'Server:' in line or 'SSH-' in line or '220 ' in line or 'FTP' in line or 'HTTP/' in line:
                        return line.strip()[:100]
                return lines[0].split('\r')[0][:100]
        except:
            pass
        return "Filtered / No Response"

    def scan_single_port(self, ip, port):
        if not self.is_running:
            return

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(self.timeout)
                result = s.connect_ex((ip, port))

                if result == 0:
                    try:
                        service = socket.getservbyport(port, 'tcp')
                    except OSError:
                        service = "unknown"

                    banner = self.grab_banner(s, port)
                    self.result_queue.put({
                        'ip': ip,
                        'port': port,
                        'state': 'OPEN',
                        'service': service,
                        'banner': banner
                    })
                    self.log_queue.put(f"[OPEN] {ip}:{port} - {service} - {banner}")
                else:
                    self.log_queue.put(f"[CLOSED] {ip}:{port}")
        except socket.timeout:
            self.log_queue.put(f"[TIMEOUT] {ip}:{port}")
        except Exception as e:
            self.log_queue.put(f"[ERROR] {ip}:{port} - {str(e)}")
        finally:
            with self.lock:
                self.completed += 1
                if self.completed % 5 == 0 or self.completed == len(self.ports):
                    self.log_queue.put(f"[PROGRESS] {self.completed}/{len(self.ports)} ports scanned")

    def execute(self):
        ips = self.expand_target()
        total_ports = len(self.ports)

        self.log_queue.put(f"[INIT] Target: {self.target}")
        self.log_queue.put(f"[INIT] IPs: {len(ips)}, Ports: {total_ports}")
        self.log_queue.put(f"[INIT] Timeout: {self.timeout}s")
        self.log_queue.put("[SCAN] Starting parallel scan...")

        threads = []
        for ip in ips:
            for port in self.ports:
                if not self.is_running:
                    break
                t = threading.Thread(target=self.scan_single_port, args=(ip, port), daemon=True)
                threads.append(t)
                t.start()

                # Thread sayısını sınırla (maksimum 50 eş zamanlı)
                if len([th for th in threads if th.is_alive()]) >= 50:
                    time.sleep(0.1)

        for t in threads:
            t.join(timeout=self.timeout + 2)

        self.log_queue.put(
            f"[DONE] Completed. {len([r for r in self.result_queue.queue if isinstance(r, dict)])} open ports found.")
        self.result_queue.put("SCAN_COMPLETE")


class ScannerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Advanced Network Scanner")
        self.geometry("1000x700")
        self.minsize(900, 650)

        self.scan_thread = None
        self.scanner_engine = None
        self.result_queue = queue.Queue()
        self.log_queue = queue.Queue()
        self.scan_results = []

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.build_header()
        self.build_controls()
        self.build_output_area()
        self.build_footer()

        self.after(100, self.process_queues)

    def build_header(self):
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=15)

        title_label = ctk.CTkLabel(
            header_frame,
            text="NET.SCANNER PRO",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(side="left")

        branding_label = ctk.CTkLabel(
            header_frame,
            text="Powered by mucahidbalci  |  mucahidbalci.github.io",
            font=ctk.CTkFont(size=12, weight="normal"),
            text_color="gray"
        )
        branding_label.pack(side="right")

    def build_controls(self):
        control_frame = ctk.CTkFrame(self)
        control_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 10))
        control_frame.grid_rowconfigure(3, weight=1)
        control_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(control_frame, text="Target (IP / CIDR)", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0,
                                                                                                     sticky="w",
                                                                                                     padx=15, pady=10)
        self.target_entry = ctk.CTkEntry(control_frame, placeholder_text="192.168.1.1 or 192.168.1.0/24", width=300)
        self.target_entry.grid(row=0, column=1, sticky="w", padx=15, pady=10)

        ctk.CTkLabel(control_frame, text="Port Profile", font=ctk.CTkFont(weight="bold")).grid(row=1, column=0,
                                                                                               sticky="w", padx=15,
                                                                                               pady=5)

        profile_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
        profile_frame.grid(row=1, column=1, sticky="w", padx=15, pady=5)

        self.port_var = tk.StringVar(value="common")
        ctk.CTkRadioButton(profile_frame, text="Top 20 Common", variable=self.port_var, value="common").pack(
            side="left", padx=5)
        ctk.CTkRadioButton(profile_frame, text="Web Services", variable=self.port_var, value="web").pack(side="left",
                                                                                                         padx=5)
        ctk.CTkRadioButton(profile_frame, text="Full (1-1024)", variable=self.port_var, value="full").pack(side="left",
                                                                                                           padx=5)

        self.custom_port_entry = ctk.CTkEntry(profile_frame, placeholder_text="Custom: 80,443,8080 or 1-100", width=200)
        self.custom_port_entry.pack(side="left", padx=10)

        ctk.CTkLabel(control_frame, text="Timeout (sec)", font=ctk.CTkFont(weight="bold")).grid(row=2, column=0,
                                                                                                sticky="w", padx=15,
                                                                                                pady=5)
        self.timeout_entry = ctk.CTkEntry(control_frame, placeholder_text="3.0", width=100)
        self.timeout_entry.insert(0, "3.0")
        self.timeout_entry.grid(row=2, column=1, sticky="w", padx=15, pady=5)

        action_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
        action_frame.grid(row=0, column=2, rowspan=3, padx=15, pady=10, sticky="e")

        self.start_btn = ctk.CTkButton(action_frame, text="START SCAN", command=self.start_scan, fg_color="#2ea043",
                                       hover_color="#238636")
        self.start_btn.pack(side="left", padx=5)

        self.stop_btn = ctk.CTkButton(action_frame, text="STOP", command=self.stop_scan, state="disabled",
                                      fg_color="#da3633", hover_color="#b62324")
        self.stop_btn.pack(side="left", padx=5)

        self.export_btn = ctk.CTkButton(action_frame, text="EXPORT CSV", command=self.export_results, state="disabled",
                                        fg_color="#1f6feb", hover_color="#1158c7")
        self.export_btn.pack(side="left", padx=5)

        self.log_text = tk.Text(control_frame, height=8, bg="#0d1117", fg="#8b949e", font=("Consolas", 10),
                                relief="flat", state="disabled")
        self.log_text.grid(row=3, column=0, columnspan=3, sticky="nsew", padx=15, pady=10)

    def build_output_area(self):
        output_frame = ctk.CTkFrame(self)
        output_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 20))
        output_frame.grid_rowconfigure(0, weight=1)
        output_frame.grid_columnconfigure(0, weight=1)

        columns = ("ip", "port", "state", "service", "banner")
        self.tree = ttk.Treeview(output_frame, columns=columns, show="headings", style="Custom.Treeview")

        self.tree.heading("ip", text="IP Address")
        self.tree.heading("port", text="Port")
        self.tree.heading("state", text="State")
        self.tree.heading("service", text="Service")
        self.tree.heading("banner", text="Banner / Version")

        self.tree.column("ip", width=150)
        self.tree.column("port", width=80, anchor="center")
        self.tree.column("state", width=80, anchor="center")
        self.tree.column("service", width=120)
        self.tree.column("banner", width=400)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Custom.Treeview", background="#161b22", foreground="#c9d1d9", fieldbackground="#161b22",
                        borderwidth=0)
        style.configure("Custom.Treeview.Heading", background="#21262d", foreground="#c9d1d9", relief="flat")
        style.map("Custom.Treeview", background=[("selected", "#1f6feb")])

        scrollbar = ttk.Scrollbar(output_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

    def build_footer(self):
        footer_frame = ctk.CTkFrame(self, fg_color="transparent", height=30)
        footer_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=5)

        self.status_var = tk.StringVar(value="Ready")
        status_label = ctk.CTkLabel(footer_frame, textvariable=self.status_var, font=ctk.CTkFont(size=11),
                                    text_color="gray")
        status_label.pack(side="left")

    def parse_ports(self):
        profile = self.port_var.get()
        custom = self.custom_port_entry.get().strip()

        if custom:
            try:
                if '-' in custom:
                    start, end = map(int, custom.split('-'))
                    return list(range(start, end + 1))
                return [int(p.strip()) for p in custom.split(',')]
            except ValueError:
                return []

        if profile == "common":
            return [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080, 8443]
        elif profile == "web":
            return [80, 443, 8000, 8080, 8443, 8888, 3000, 5000]
        elif profile == "full":
            return list(range(1, 1025))
        return []

    def start_scan(self):
        target = self.target_entry.get().strip()
        if not target:
            messagebox.showwarning("Input Error", "Target IP or CIDR is required.")
            return

        ports = self.parse_ports()
        if not ports:
            messagebox.showwarning("Input Error", "Invalid port configuration.")
            return

        try:
            timeout = float(self.timeout_entry.get().strip())
            if timeout < 0.5 or timeout > 10.0:
                raise ValueError
        except ValueError:
            timeout = 3.0

        self.scan_results = []
        self.tree.delete(*self.tree.get_children())
        self.log_text.configure(state="normal")
        self.log_text.delete(1.0, tk.END)
        self.log_text.configure(state="disabled")

        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.export_btn.configure(state="disabled")
        self.status_var.set("Scanning in progress...")

        self.scanner_engine = ScannerEngine(target, ports, self.result_queue, self.log_queue, timeout)
        self.scan_thread = threading.Thread(target=self.scanner_engine.execute, daemon=True)
        self.scan_thread.start()

    def stop_scan(self):
        if self.scanner_engine:
            self.scanner_engine.stop()
            self.status_var.set("Scan aborted by user.")
            self.reset_controls()

    def reset_controls(self):
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        if self.scan_results:
            self.export_btn.configure(state="normal")

    def process_queues(self):
        try:
            while True:
                log_msg = self.log_queue.get_nowait()
                self.log_text.configure(state="normal")
                self.log_text.insert(tk.END, f"{log_msg}\n")
                self.log_text.see(tk.END)
                self.log_text.configure(state="disabled")
        except queue.Empty:
            pass

        try:
            while True:
                item = self.result_queue.get_nowait()
                if item == "SCAN_COMPLETE":
                    self.status_var.set(f"Scan completed. {len(self.scan_results)} open ports found.")
                    self.reset_controls()
                else:
                    self.scan_results.append(item)
                    self.tree.insert("", "end", values=(
                        item['ip'],
                        item['port'],
                        item['state'],
                        item['service'],
                        item['banner']
                    ))
        except queue.Empty:
            pass

        self.after(100, self.process_queues)

    def export_results(self):
        if not self.scan_results:
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            initialfile=f"scan_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )

        if file_path:
            try:
                with open(file_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=["ip", "port", "state", "service", "banner"])
                    writer.writeheader()
                    writer.writerows(self.scan_results)
                messagebox.showinfo("Success", "Results exported successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {str(e)}")


if __name__ == "__main__":
    app = ScannerApp()
    app.mainloop()
