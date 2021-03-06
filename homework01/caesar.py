def  encrypt_caesar(plaintext: str) -> str:
    ciphertext = ''
    for ch in plaintext:
        if 'a' <= ch <= 'z' or 'A' <= ch <= 'Z':
            code = ord(ch)
            if code > ord('W') and code < ord('a') or code > ord('w'):
                ciphertext += chr(code-23)
            else:
               ciphertext += chr(code+3)
        else:
            ciphertext += ch
    return ciphertext



def decrypt_caesar(ciphertext: str) -> str:
    plaintext = ''
    for ch in ciphertext:
        if 'a' <= ch <= 'z' or 'A' <= ch <= 'Z':
            code = ord(ch)
            if code < ord('d') and code > ord('Z') or code < ord('D'):
                plaintext += chr(code + 23)
            else:
                plaintext += chr(code - 3)
        else:
            plaintext += ch
    print(plaintext)

