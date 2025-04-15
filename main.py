import tkinter as tk
from tkinter import messagebox, scrolledtext
import smtplib
from email.mime.text import MIMEText
import time
import threading

gateway_map = {
    'att': '@txt.att.net',
    'verizon': '@vtext.com',
    'tmobile': '@tmomail.net',
    'sprint': '@messaging.sprintpcs.com',
}

def clean_ascii(text):
    return text.encode('ascii', errors='ignore').decode()

def send_sms(phone, provider, display_name, email, password, count, delay, output_box):
    phone = clean_ascii(phone.strip())
    provider = clean_ascii(provider.strip().lower())
    display_name = clean_ascii(display_name.strip())
    email = clean_ascii(email.strip())
    password = clean_ascii(password.strip())

    if provider not in gateway_map:
        output_box.insert(tk.END, f"[!] Unsupported provider '{provider}'. Supported: att, verizon, tmobile, sprint.\n")
        return

    sms_gateway = f"{phone}{gateway_map[provider]}"
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(email, password)

            for i in range(count):
                message_body = "Whats up. Since you love to prank call me I think its only fair I spam text you. Enjoy :)"
                msg = MIMEText(message_body, _charset='utf-8')
                msg['From'] = f"{display_name} <{email}>"
                msg['To'] = sms_gateway
                msg['Subject'] = "Get Trolled"

                server.sendmail(email, sms_gateway, msg.as_string())
                output_box.insert(tk.END, f"[+] Sent message {i+1}/{count}. Waiting {delay}s...\n")
                output_box.see(tk.END)
                time.sleep(delay)

        output_box.insert(tk.END, "[✓] All messages sent.\n")

    except Exception as e:
        output_box.insert(tk.END, f"[!] Failed to send messages: {e}\n")
        output_box.see(tk.END)

def start_sms_thread(phone, provider, display_name, email, password, count, delay, output_box):
    try:
        count = int(count)
        delay = int(delay)
        if count <= 0 or delay < 0:
            raise ValueError
    except ValueError:
        output_box.insert(tk.END, "[!] Count must be > 0 and delay must be >= 0.\n")
        return

    threading.Thread(
        target=send_sms,
        args=(phone, provider, display_name, email, password, count, delay, output_box),
        daemon=True
    ).start()

def open_sms_window():
    sms_win = tk.Toplevel(bg='black')
    sms_win.title("Python SMS Sender")
    sms_win.geometry("600x650")

    entries = {}

    def add_labeled_entry(label_text, key, show=None):
        tk.Label(sms_win, text=label_text, fg='white', bg='black', font=('Arial', 10)).pack()
        entry = tk.Entry(sms_win, width=40, show=show, bg='white', fg='black')
        entry.pack(pady=3)
        entries[key] = entry

    add_labeled_entry("Phone Number:", "phone")
    add_labeled_entry("Carrier (att, verizon, tmobile, sprint):", "provider")
    add_labeled_entry("Display Name:", "name")
    add_labeled_entry("Your Email (Gmail):", "email")
    add_labeled_entry("App Password:", "password", show="*")
    add_labeled_entry("How many times to send?", "count")
    add_labeled_entry("Delay between messages (seconds):", "delay")

    terminal_output = scrolledtext.ScrolledText(sms_win, height=15, width=70, bg='black', fg='red', insertbackground='white')
    terminal_output.pack(pady=10)

    tk.Button(
        sms_win,
        text="Send SMS",
        bg='red', fg='white',
        command=lambda: start_sms_thread(
            entries["phone"].get(),
            entries["provider"].get(),
            entries["name"].get(),
            entries["email"].get(),
            entries["password"].get(),
            entries["count"].get(),
            entries["delay"].get(),
            terminal_output
        )
    ).pack(pady=10)

def open_ip_tracking():
    messagebox.showinfo("IP Tracking", "IP tracking feature not implemented yet.")

def show_credits():
    credits_text = (
        "                      == Credits ==\n"
        "Main Developer: mac_cheesecoder (Discord)\n"
        "Contributor: zegamerttv (Discord)\n\n"
        "GitHub - https://github.com/mac-cheesecoder"
    )
    messagebox.showinfo("Credits", credits_text)

def main():
    root = tk.Tk()
    root.title("Blacklisted Command Panel")
    root.geometry("500x550")
    root.configure(bg='black')
    root.resizable(False, False)

    tk.Label(root, text="Blacklisted 🚫", font=("Helvetica", 24, "bold"), fg='red', bg='black').pack(pady=20)

    def styled_button(text, command):
        return tk.Button(
            root, text=text, command=command,
            width=30, bg='red', fg='white', font=('Arial', 12), relief='raised', bd=3
        )

    styled_button("1. IP Tracking", open_ip_tracking).pack(pady=10)
    styled_button("2. Python SMS", open_sms_window).pack(pady=10)
    styled_button("3. Credits", show_credits).pack(pady=10)

    def confirm_exit():
        answer = messagebox.askyesno(
            "Confirm Exit",
            "Are you sure you want to close the Blacklisted Command Panel?\nAll running scripts will be disabled."
        )
        if answer:
            root.destroy()

    styled_button("4. Exit", confirm_exit).pack(pady=30)

    root.mainloop()

if __name__ == "__main__":
    main()
