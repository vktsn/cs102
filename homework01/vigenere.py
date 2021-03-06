def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    chiphertext = ''
    for index, ch in enumerate(plaintext):
        if 'a' <= ch <= 'z' or 'A' <= ch <= 'Z':
            shift = ord(keyword[index % len(keyword)]) #
            if 'a' <= ch <= 'z':
                shift -= ord('a')
            else: shift -= ord('A')  
            code = ord(ch) + shift 
            if 'a' <= ch <= 'z' and code > ord('z'): 
                code -= 26
            elif 'A' <= ch <= 'Z' and code > ord('Z'):
                code -= 26
            chiphertext += chr(code)
        else:
            chiphertext += ch
    return chiphertext

def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    plaintext = ''
    for index, ch in enumerate(ciphertext):
        if 'a' <= ch <= 'z' or 'A' <= ch <= 'Z':
            shift = ord(keyword[index % len(keyword)])
            shift -= ord('a') if 'a' <= ch <= 'z' else ord('A')
            code = ord(ch) - shift
            if 'a' <= ch <= 'z' and code < ord('a'):
                code += 26
            elif 'A' <= ch <= 'Z' and code < ord('A'):
                code += 26
            plaintext += chr(code)
        else:
            plaintext += ch
    return plaintext
