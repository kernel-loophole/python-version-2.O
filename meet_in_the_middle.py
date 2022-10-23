import array
from des import DesKey
from multiprocessing import Pool
from functools import partial
from pyDes import des

key0 = DesKey(b"messages")                  # for DES
key1 = DesKey(b"messages")

ciper_text_1=key0.encrypt(b"messages")

cipher_text_2=key1.encrypt(ciper_text_1)

cipher_text_2

def generate_keys(num):
    for n in range(num):
        arr = [0] * 8
        powers = [7, 6, 5, 4, 3, 2, 1, 0]
        for i, p in enumerate(powers):
            arr[i] = n // (128 ** p)
            n = n - (arr[i] * (128 ** p)) if n >= (128 ** p) else n
        yield array.array('B', arr).tostring()

# encrypt given plaintext with key
def encrypt(key, plain_text):
    cipher = des(key)
    return cipher.encrypt(plain_text)


# decrypt given plaintext with key
def decrypt(key, cipher_text):
    cipher = des(key)
    return cipher.decrypt(cipher_text)

def hex_formating(bs):
    return ''.join([format(b, '02x') for b in bs])


# convert a bytes string into something more human readable
def int_formating(bs):
    return [int(b) for b in bs]

def meet_in_the_middle(nkeys, plain_text, cipher_text, pool=None):
  table = {}
  # generate all the encryption
  for k in generate_keys(nkeys):
    c = encrypt(k, plain_text)
    table[c] = k
     # partial composes a function with standard args
    print(table)
    # iterate each decryption and quit if we find a match
    for k in generate_keys(nkeys):
        p = decrypt(k, cipher_text)
        if p in table.keys():
            k1 = int_formating(table[p])
            k2 = int_formating(k)
            print('found keys: (k1:{}, k2:{})'.format(k1, k2))
            print('apply k2 then k1 to decrypt')
            return (k1, k2)

    # if here then we didn't find anything
    print('did not find keys')

def convert_string_to_bytes(s):
  return bytes(s,encoding='utf-8')
if __name__=="__main__":
	p ="messages"
	cho =cipher_text_2
	ph = convert_string_to_bytes(p)
	ch = cho
	print('plain text:', ph)
	print('cipher text:', ch)
	if len(ph) != len(ch):
	  print('please provide plain and cipher text with matching lengths')
	  print('the current lengths are:\n\tplain: {}\n\tcipher: {}'.format(len(ph), len(ch)))
	else:
	  with Pool() as p:
	    keys = meet_in_the_middle(127**2, ph, ch, p)
	    print(f"k1:{hex_formating(keys[0])}, k2{hex_formating(keys[1])}")

