# My program that I created for the university for laboratory work "Creating a program for encrypting text using the gamming method"
# 🔐 Метод гамування / Stream Cipher — XOR Gamma Method Encryption Tool

Графічна Python (Tkinter) програма для шифрування та розшифрування текстових файлів методом **гамування (XOR stream cipher)**.  
Підтримує українську та англійську мови інтерфейсу.

A graphical Python (Tkinter) application for encrypting and decrypting text files using the **XOR stream cipher (gamma method)**.  
Supports both Ukrainian and English interface languages.

---

## ✨ Можливості програми

- 🔑 Arbitrary length key generation/Генерація ключа довільної довжини  
- 🔐 Encrypt and decrypt using XOR stream cipher/Шифрування та розшифрування методом XOR  
- 📁 Select plaintext and key files/Вибір файлів відкритого тексту та ключа  
- 💾 Automatically saves `encrypted.dat` and `decrypted.dat`/Автоматичне створення `encrypted.dat` і `decrypted.dat`  
- 🔣 UTF-8 safe processing/Підтримка UTF-8  
- 🧵 True streaming XOR encryption/Потокове XOR-шифрування  
- 🔏 Password protection/Захист паролем  
- 🌐 Language selection (UA/EN)/Перемикання мови інтерфейсу (UA/EN)
🔑 Generate a key of any custom length

## 🖥️ Interface screenshot/Скриншот інтерфейсу
UA:
<img width="989" height="910" alt="image" src="https://github.com/user-attachments/assets/7dff8b8d-28b4-43b3-879b-113d910dd11d" />
EN:
<img width="996" height="859" alt="image" src="https://github.com/user-attachments/assets/6713dc73-8785-4d0e-a4e0-fe911336ff0a" />

---

## 🚀 Запуск

### 1️⃣ Install Python/Встановити Python (3.10+)

### 2️⃣ Install tkinter(if necessary)/Встановити tkinter (якщо потрібно):

```
bash
pip install tk

python main.py
```

### Project Structure/Структура проєкту

1. main.py              # Main program code/Основний код програми
2. before.dat           # Input plaintext/Вхідний відкритий текст
3. key.dat              # Encryption key/Ключ для шифрування
4. encrypted.dat        # Encrypted text/Зашифрований текст
5. decrypted.dat        # Decrypted text/Розшифрований текст
6. README.md            # Documentation/Документація

