from flask import Flask, render_template, request
import binascii

app = Flask(__name__)



def decrypt_cisco_type7(encrypted_password):
    # Static table of characters
    tableau_de_caractere = [
        0x64, 0x73, 0x66, 0x64, 0x3b, 0x6b, 0x66, 0x6f,
        0x41, 0x2c, 0x2e, 0x69, 0x79, 0x65, 0x77, 0x72,
        0x6b, 0x6c, 0x64, 0x4a, 0x4b, 0x44, 0x48, 0x53,
        0x55, 0x42
    ]

    # Convert encrypted password to lowercase
    encrypted_password = encrypted_password.lower()

    # Check if encrypted password is a valid hexadecimal string
    if not all(c in '0123456789abcdef' for c in encrypted_password):
        raise ValueError("Invalid hexadecimal string")

    # Initialize seed value
    seed = int(encrypted_password[0:2], 16)

    # Initialize decrypted password array
    decrypted_password = []

    # Decrypt each character
    for i in range(2, len(encrypted_password), 2):
        valeur = int(encrypted_password[i:i+2], 16)
        decrypted_password.append(valeur ^ tableau_de_caractere[seed])
        seed = (seed + 1) % len(tableau_de_caractere)

    # Convert decrypted password array to string
    decrypted_password = ''.join(chr(c) for c in decrypted_password)

    return decrypted_password

@app.route('/', methods=['GET', 'POST'])
def index():
    decrypted_password = ''
    if request.method == 'POST':
        encrypted_password = request.form['encrypted_password']
        # decrypted_password = decrypt_cisco_type_7(encrypted_password)
        decrypted_password = decrypt_cisco_type7(encrypted_password)
    return render_template('index.html', decrypted_password=decrypted_password)

if __name__ == '__main__':
    app.run(debug=True)
