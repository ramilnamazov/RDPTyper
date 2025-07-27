import tkinter as tk
from tkinter import ttk, messagebox
import pyautogui
import time
import threading
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import secrets
import gc
import atexit
import signal
import sys
import os

class RDPTyperFocus:
    def __init__(self):
        self.username = None
        self.password = None
        self.cipher_suite = None
        self.salt = secrets.token_bytes(16)
        
        # Typing settings optimized for RDP
        self.char_delay = 0.08  # Slightly slower for RDP
        self.initial_delay = 0.5  # Time to switch back to RDP
        
        # PyAutoGUI settings for RDP
        pyautogui.FAILSAFE = False  # Don't stop at corners
        pyautogui.PAUSE = 0.01  # Minimal pause between actions
        
        # Initialize encryption
        self.init_encryption()
        
        # Register cleanup handlers
        self._register_cleanup_handlers()
        
    def _register_cleanup_handlers(self):
        """Register handlers for secure cleanup on exit"""
        # Normal exit
        atexit.register(self._secure_cleanup)
        
        # Handle Ctrl+C and other signals
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        # Windows-specific signal
        if sys.platform == "win32":
            signal.signal(signal.SIGBREAK, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle system signals for cleanup"""
        self._secure_cleanup()
        sys.exit(0)
    
    def _secure_cleanup(self):
        """Securely overwrite and clear sensitive data"""
        # Overwrite credentials with random data multiple times
        if self.username:
            for _ in range(3):
                self.username = secrets.token_bytes(len(self.username))
        if self.password:
            for _ in range(3):
                self.password = secrets.token_bytes(len(self.password))
        
        # Clear the encryption key
        if self.cipher_suite:
            self.cipher_suite = None
            
        # Overwrite salt
        if self.salt:
            self.salt = secrets.token_bytes(len(self.salt))
        
        # Final cleanup
        self.username = None
        self.password = None
        self.salt = None
        
        # Force garbage collection
        gc.collect()
        
    def init_encryption(self):
        """Initialize encryption with a runtime-generated key"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(secrets.token_bytes(32)))
        self.cipher_suite = Fernet(key)
    
    def encrypt_credential(self, credential):
        """Encrypt a credential"""
        if credential:
            return self.cipher_suite.encrypt(credential.encode())
        return None
    
    def decrypt_credential(self, encrypted):
        """Decrypt a credential"""
        if encrypted:
            return self.cipher_suite.decrypt(encrypted).decode()
        return None
    
    def type_with_delay(self):
        """Give time to switch back to RDP window"""
        # Countdown in status
        for i in range(3, 0, -1):
            self.mini_status.config(text=f"Typing in {i}...")
            self.mini_window.update()
            time.sleep(1)
    
    def type_username(self):
        """Type username with RDP-optimized method"""
        if not self.username:
            messagebox.showwarning("Warning", "No username saved!")
            return
            
        self.type_with_delay()
        self.mini_status.config(text="Typing username...")
        self.mini_window.update()
        
        decrypted = self.decrypt_credential(self.username)
        
        # Use pyautogui for RDP compatibility
        for char in decrypted:
            pyautogui.press(char)
            time.sleep(self.char_delay)
        
        # Securely clear sensitive data
        decrypted = secrets.token_bytes(len(decrypted))
        del decrypted
        gc.collect()
        
        self.mini_status.config(text="✓ Ready")
    
    def type_password(self):
        """Type password with RDP-optimized method"""
        if not self.password:
            messagebox.showwarning("Warning", "No password saved!")
            return
            
        self.type_with_delay()
        self.mini_status.config(text="Typing password...")
        self.mini_window.update()
        
        decrypted = self.decrypt_credential(self.password)
        
        # Use pyautogui for RDP compatibility
        for char in decrypted:
            pyautogui.press(char)
            time.sleep(self.char_delay)
        
        # Securely clear sensitive data
        decrypted = secrets.token_bytes(len(decrypted))
        del decrypted
        gc.collect()
        
        self.mini_status.config(text="✓ Ready")
    
    def type_both(self):
        """Type username, TAB, then password"""
        if not self.username or not self.password:
            messagebox.showwarning("Warning", "Missing credentials!")
            return
            
        self.type_with_delay()
        self.mini_status.config(text="Typing credentials...")
        self.mini_window.update()
        
        # Type username
        decrypted_user = self.decrypt_credential(self.username)
        for char in decrypted_user:
            pyautogui.press(char)
            time.sleep(self.char_delay)
        decrypted_user = secrets.token_bytes(len(decrypted_user))
        del decrypted_user
        
        # Press TAB
        time.sleep(0.2)
        pyautogui.press('tab')
        time.sleep(0.2)
        
        # Type password
        decrypted_pass = self.decrypt_credential(self.password)
        for char in decrypted_pass:
            pyautogui.press(char)
            time.sleep(self.char_delay)
        decrypted_pass = secrets.token_bytes(len(decrypted_pass))
        del decrypted_pass
        
        gc.collect()
        self.mini_status.config(text="✓ Ready")
    
    def create_mini_window(self):
        """Create a small always-on-top window"""
        self.mini_window = tk.Toplevel(self.root)
        self.mini_window.title("RDP Typer")
        self.mini_window.geometry("300x200")
        self.mini_window.attributes('-topmost', True)  # Always on top
        self.mini_window.resizable(False, False)
        
        # Position in top-right corner
        self.mini_window.geometry("+{}+{}".format(
            self.root.winfo_screenwidth() - 320, 20
        ))
        
        # Frame
        frame = ttk.Frame(self.mini_window, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        ttk.Label(frame, text="🔐 RDP Quick Type", 
                 font=('Arial', 12, 'bold')).pack(pady=(0, 10))
        
        # Buttons with RDP-friendly layout
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create large buttons for easy clicking
        self.user_btn = ttk.Button(btn_frame, text="👤 Username (U)", 
                                  command=lambda: threading.Thread(target=self.type_username, daemon=True).start())
        self.user_btn.pack(fill=tk.X, pady=2)
        
        self.pass_btn = ttk.Button(btn_frame, text="🔑 Password (P)", 
                                  command=lambda: threading.Thread(target=self.type_password, daemon=True).start())
        self.pass_btn.pack(fill=tk.X, pady=2)
        
        self.both_btn = ttk.Button(btn_frame, text="⚡ Both (B)", 
                                  command=lambda: threading.Thread(target=self.type_both, daemon=True).start())
        self.both_btn.pack(fill=tk.X, pady=2)
        
        # Status
        self.mini_status = ttk.Label(frame, text="✓ Ready", 
                                    font=('Arial', 9), foreground='green')
        self.mini_status.pack(pady=(10, 0))
        
        # Bind keyboard shortcuts to the mini window
        self.mini_window.bind('u', lambda e: threading.Thread(target=self.type_username, daemon=True).start())
        self.mini_window.bind('U', lambda e: threading.Thread(target=self.type_username, daemon=True).start())
        self.mini_window.bind('p', lambda e: threading.Thread(target=self.type_password, daemon=True).start())
        self.mini_window.bind('P', lambda e: threading.Thread(target=self.type_password, daemon=True).start())
        self.mini_window.bind('b', lambda e: threading.Thread(target=self.type_both, daemon=True).start())
        self.mini_window.bind('B', lambda e: threading.Thread(target=self.type_both, daemon=True).start())
        
        # Handle window close with cleanup
        self.mini_window.protocol("WM_DELETE_WINDOW", self._on_mini_close)
        self.mini_window.withdraw()  # Start hidden
    
    def _on_mini_close(self):
        """Handle mini window close"""
        self.mini_window.withdraw()
    
    def _on_main_close(self):
        """Handle main window close with cleanup"""
        self._secure_cleanup()
        self.root.destroy()
    
    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo("About", "Made by Ramil Namazov\nVersion v1.0")
    
    def create_main_gui(self):
        """Create the main setup window"""
        self.root = tk.Tk()
        self.root.title("RDP Typer Setup")
        self.root.geometry("450x400")
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self._on_main_close)
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        ttk.Label(main_frame, text="🔐 RDP Credential Setup", 
                 font=('Arial', 16, 'bold')).pack(pady=(0, 20))
        
        # Instructions
        inst_frame = ttk.LabelFrame(main_frame, text="📋 Instructions", padding="10")
        inst_frame.pack(fill=tk.X, pady=(0, 20))
        
        instructions = """1. Enter your credentials below
2. Click 'Save & Show Mini Window'
3. Position the mini window where convenient
4. Click buttons or press U/P/B in mini window
5. You have 3 seconds to click back in RDP!"""
        
        ttk.Label(inst_frame, text=instructions, justify=tk.LEFT).pack()
        
        # Credentials frame
        cred_frame = ttk.LabelFrame(main_frame, text="🔑 Credentials", padding="10")
        cred_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Username
        ttk.Label(cred_frame, text="Username:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.username_entry = ttk.Entry(cred_frame, width=30)
        self.username_entry.grid(row=0, column=1, pady=5, padx=(10, 0))
        
        # Password
        ttk.Label(cred_frame, text="Password:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.password_entry = ttk.Entry(cred_frame, width=30, show="*")
        self.password_entry.grid(row=1, column=1, pady=5, padx=(10, 0))
        
        # Show password checkbox
        self.show_var = tk.BooleanVar()
        ttk.Checkbutton(cred_frame, text="Show password", variable=self.show_var,
                       command=self.toggle_password).grid(row=2, column=1, sticky=tk.W, padx=(10, 0))
        
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack()
        
        ttk.Button(btn_frame, text="💾 Save & Show Mini Window", 
                  command=self.save_and_show).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(btn_frame, text="🗑️ Clear", 
                  command=self.clear_credentials).pack(side=tk.LEFT, padx=5)
        
        # About button with info icon
        about_btn = ttk.Button(btn_frame, text="ℹ️ About", 
                              command=self.show_about)
        about_btn.pack(side=tk.LEFT, padx=5)
        
        # Create tooltip for about button
        self.create_tooltip(about_btn, "Made by Ramil Namazov\nVersion v1.0")
        
        # Create mini window (hidden initially)
        self.create_mini_window()
    
    def create_tooltip(self, widget, text):
        """Create a tooltip for a widget"""
        def on_enter(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            label = tk.Label(tooltip, text=text, background="#ffffe0", 
                           relief="solid", borderwidth=1, font=("Arial", 9))
            label.pack()
            widget.tooltip = tooltip
        
        def on_leave(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                del widget.tooltip
        
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
    
    def toggle_password(self):
        """Toggle password visibility"""
        if self.show_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")
    
    def save_and_show(self):
        """Save credentials and show mini window"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password!")
            return
        
        # Encrypt and store
        self.username = self.encrypt_credential(username)
        self.password = self.encrypt_credential(password)
        
        # Clear entries
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        
        # Show mini window
        self.mini_window.deiconify()
        self.mini_window.lift()
        
        messagebox.showinfo("Success", 
                          "Credentials saved!\n\n"
                          "Use the mini window to type in RDP.\n"
                          "You can minimize this setup window.")
    
    def clear_credentials(self):
        """Clear all credentials with secure overwrite"""
        # Overwrite before clearing
        if self.username:
            self.username = secrets.token_bytes(len(self.username))
        if self.password:
            self.password = secrets.token_bytes(len(self.password))
            
        self.username = None
        self.password = None
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        gc.collect()
    
    def run(self):
        """Run the application"""
        self.create_main_gui()
        self.root.mainloop()

def main():
    try:
        app = RDPTyperFocus()
        app.run()
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
