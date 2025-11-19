import tkinter as tk
from tkinter import filedialog, messagebox
import os
import hashlib


# ============================================================
# ------------------------- UTIL ------------------------------
# ============================================================

def derive_key_from_password(password: str, key_len: int) -> bytes:
    salt = b"xor_cipher_fixed_salt"
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        50000,
        dklen=key_len,
    )


def xor_stream_bytes(data: bytes, key: bytes) -> bytes:
    out = bytearray()
    kl = len(key)
    for i, b in enumerate(data):
        out.append(b ^ key[i % kl])
    return bytes(out)


def xor_file_stream(input_path, output_path, key, block_size=4096):
    with open(input_path, "rb") as fin, open(output_path, "wb") as fout:
        while chunk := fin.read(block_size):
            fout.write(xor_stream_bytes(chunk, key))


# ============================================================
# ------------------------- LANGUAGE -------------------------
# ============================================================

LANG = "UA"

TEXTS = {
    "UA": {
        "title": "Метод гамування",
        "gen_key": "Генерувати випадковий ключ",
        "pass_key": "Створити ключ з паролю",
        "key_len": "Довжина ключа (байт):",
        "pass": "Пароль → ключ:",
        "no_key": "Немає key.dat!",
        "key_ok": "Ключ згенеровано",
        "key_pwd_ok": "Ключ створено з паролю",
        "text_enc": "Шифрувати текст → after.dat",
        "text_dec": "Розшифрувати текст → decoded.dat",
        "enter_text": "Введіть текст:",
        "decoded_text": "Розшифрований текст:",
        "file_enc": "Шифрувати файл",
        "file_dec": "Розшифрувати файл",
        "choose_in": "Обрати вхідний файл",
        "choose_out": "Обрати вихідний файл",
        "file_err": "Оберіть файли!",
        "enc_ok": "Зашифровано",
        "dec_ok": "Розшифровано",
        "err_len": "Введіть коректну довжину ключа!",
        "err_pass": "Введіть пароль!",
    },
    "EN": {
        "title": "Stream Cipher (XOR)",
        "gen_key": "Generate random key",
        "pass_key": "Create key from password",
        "key_len": "Key length (bytes):",
        "pass": "Password → key:",
        "no_key": "key.dat not found!",
        "key_ok": "Key generated",
        "key_pwd_ok": "Key created from password",
        "text_enc": "Encrypt text → after.dat",
        "text_dec": "Decrypt text → decoded.dat",
        "enter_text": "Enter text:",
        "decoded_text": "Decrypted text:",
        "file_enc": "Encrypt file",
        "file_dec": "Decrypt file",
        "choose_in": "Choose input file",
        "choose_out": "Choose output file",
        "file_err": "Select files!",
        "enc_ok": "Encrypted",
        "dec_ok": "Decrypted",
        "err_len": "Enter valid key length!",
        "err_pass": "Enter password!",
    }
}


def T(key):
    return TEXTS[LANG][key]


def update_language():
    root.title(T("title"))
    lbl_key_len.config(text=T("key_len"))
    btn_gen_key.config(text=T("gen_key"))
    lbl_pass.config(text=T("pass"))
    btn_pass_key.config(text=T("pass_key"))
    lbl_enter_text.config(text=T("enter_text"))
    btn_encrypt_text.config(text=T("text_enc"))
    btn_decrypt_text.config(text=T("text_dec"))
    lbl_decoded_text.config(text=T("decoded_text"))
    btn_file_in.config(text=T("choose_in"))
    btn_file_out.config(text=T("choose_out"))
    btn_encrypt_file.config(text=T("file_enc"))
    btn_decrypt_file.config(text=T("file_dec"))
    lang_button.config(text="EN" if LANG == "UA" else "UA")


def toggle_language():
    global LANG
    LANG = "EN" if LANG == "UA" else "UA"
    update_language()


# ============================================================
# ------------------------- GUI LOGIC ------------------------
# ============================================================

def generate_key():
    try:
        length = int(key_len_entry.get())
        if length <= 0:
            raise ValueError
    except:
        messagebox.showerror("Error", T("err_len"))
        return

    key = os.urandom(length)
    with open("key.dat", "wb") as f:
        f.write(key)

    messagebox.showinfo("OK", f"{T('key_ok')} ({length} bytes)")


def generate_key_from_password():
    try:
        length = int(key_len_entry.get())
    except:
        messagebox.showerror("Error", T("err_len"))
        return

    pwd = pass_entry.get()
    if not pwd:
        messagebox.showerror("Error", T("err_pass"))
        return

    key = derive_key_from_password(pwd, length)
    with open("key.dat", "wb") as f:
        f.write(key)

    messagebox.showinfo("OK", T("key_pwd_ok"))


def encrypt_text():
    try:
        key = open("key.dat", "rb").read()
    except:
        messagebox.showerror("Error", T("no_key"))
        return

    txt = text_input.get("1.0", tk.END).rstrip("\n")
    enc = xor_stream_bytes(txt.encode("utf-8"), key)
    open("after.dat", "wb").write(enc)
    messagebox.showinfo("OK", T("enc_ok"))


def decrypt_text():
    try:
        key = open("key.dat", "rb").read()
        data = open("after.dat", "rb").read()
    except:
        messagebox.showerror("Error", T("no_key"))
        return

    dec = xor_stream_bytes(data, key)
    try:
        decoded_txt = dec.decode("utf-8")
    except:
        decoded_txt = "[UTF-8 decode error]"

    text_output.delete("1.0", tk.END)
    text_output.insert(tk.END, decoded_txt)
    open("decoded.dat", "wb").write(dec)
    messagebox.showinfo("OK", T("dec_ok"))


def choose_input():
    p = filedialog.askopenfilename()
    if p:
        file_in_var.set(p)


def choose_output():
    p = filedialog.asksaveasfilename()
    if p:
        file_out_var.set(p)


def encrypt_file():
    try:
        key = open("key.dat", "rb").read()
    except:
        messagebox.showerror("Error", T("no_key"))
        return

    if not file_in_var.get() or not file_out_var.get():
        messagebox.showerror("Error", T("file_err"))
        return

    xor_file_stream(file_in_var.get(), file_out_var.get(), key)
    messagebox.showinfo("OK", T("enc_ok"))


def decrypt_file():
    try:
        key = open("key.dat", "rb").read()
    except:
        messagebox.showerror("Error", T("no_key"))
        return

    if not file_in_var.get() or not file_out_var.get():
        messagebox.showerror("Error", T("file_err"))
        return

    xor_file_stream(file_in_var.get(), file_out_var.get(), key)
    messagebox.showinfo("OK", T("dec_ok"))


# ============================================================
# ------------------------- GUI ------------------------------
# ============================================================

root = tk.Tk()
root.title("Метод гамування")
root.geometry("800x700")

lang_button = tk.Button(root, text="EN", command=toggle_language, width=5)
lang_button.pack(anchor="ne", pady=5, padx=5)

frame_key = tk.Frame(root)
frame_key.pack()
lbl_key_len = tk.Label(frame_key, text=T("key_len"))
lbl_key_len.grid(row=0, column=0)
key_len_entry = tk.Entry(frame_key, width=10)
key_len_entry.grid(row=0, column=1)
key_len_entry.insert(0, "32")

btn_gen_key = tk.Button(frame_key, text=T("gen_key"), command=generate_key)
btn_gen_key.grid(row=0, column=2, padx=5)

lbl_pass = tk.Label(frame_key, text=T("pass"))
lbl_pass.grid(row=1, column=0)
pass_entry = tk.Entry(frame_key, width=20, show="*")
pass_entry.grid(row=1, column=1)
btn_pass_key = tk.Button(frame_key, text=T("pass_key"), command=generate_key_from_password)
btn_pass_key.grid(row=1, column=2, padx=5)

lbl_enter_text = tk.Label(root, text=T("enter_text"))
lbl_enter_text.pack()
text_input = tk.Text(root, height=6, width=80)
text_input.pack()

btn_encrypt_text = tk.Button(root, text=T("text_enc"), command=encrypt_text)
btn_encrypt_text.pack()
btn_decrypt_text = tk.Button(root, text=T("text_dec"), command=decrypt_text)
btn_decrypt_text.pack()

lbl_decoded_text = tk.Label(root, text=T("decoded_text"))
lbl_decoded_text.pack()
text_output = tk.Text(root, height=6, width=80)
text_output.pack()

file_in_var = tk.StringVar()
file_out_var = tk.StringVar()

file_frame = tk.Frame(root)
file_frame.pack()
btn_file_in = tk.Button(file_frame, text=T("choose_in"), command=choose_input)
btn_file_in.grid(row=0, column=0)
tk.Entry(file_frame, textvariable=file_in_var, width=60).grid(row=0, column=1)

btn_file_out = tk.Button(file_frame, text=T("choose_out"), command=choose_output)
btn_file_out.grid(row=1, column=0)
tk.Entry(file_frame, textvariable=file_out_var, width=60).grid(row=1, column=1)

btn_encrypt_file = tk.Button(root, text=T("file_enc"), command=encrypt_file, width=30)
btn_encrypt_file.pack(pady=5)
btn_decrypt_file = tk.Button(root, text=T("file_dec"), command=decrypt_file, width=30)
btn_decrypt_file.pack(pady=5)

update_language()
root.mainloop()
