import hashlib, struct
import codecs
from random import randint


ver = 0x20400000
prev_block = "00000000000000000006a4a234288a44e715275f1775b77b2fddb6c02eb6b72f"
mrkl_root = "2dc60c563da5368e0668b81bc4d8dd369639a1134f68e425a9a74e428801e5b8"
time_ = 0x5DB8AB5E
bits =  0x17148EDF

exp = bits >> 24
mant = bits & 0xffffff
target_hexstr = '%064x' % (mant * (1<<(8*(exp - 3))))
target_str = codecs.decode(target_hexstr, 'hex')

nonce1_start = 3000000000
nonce1_final = 3100000000
print("Primele 5 valori hash: ")
for nonce1_current in range(nonce1_start, nonce1_final):
	header = (struct.pack("<L", ver)+ codecs.decode(prev_block, 'hex')[::-1] + codecs.decode(mrkl_root, 'hex')[::-1] + struct.pack("<LLL", time_, bits, nonce1_current))
	hash = hashlib.sha256(hashlib.sha256(header).digest()).digest()

	if nonce1_current < nonce1_start+5:
		print(nonce1_current,codecs.encode(hash[::-1], 'hex'))

	if hash[::-1] < target_str:
		print("Nonce1: {}\nBlock Hash: {}".format(nonce1_current,codecs.encode(hash[::-1], 'hex')))

		nonce2_start = nonce1_current + randint(0, 1000000)

		print("Nonce2 Start: {}".format(nonce2_start))

		for i in range(100000000):
			nonce2_current = nonce2_start+1
			header2 = (struct.pack("<L", ver)+ codecs.decode(prev_block, 'hex')[::-1] + codecs.decode(mrkl_root, 'hex')[::-1] + struct.pack("<LLL", time_, bits, nonce2_current))
			hash2 = hashlib.sha256(hashlib.sha256(header2).digest()).digest()
			if hash2[::-1] < target_str:
				print("Numar Testari: {}\nSucces: DA\n    Nonce2: {}\n    Hash2: {}".format(i+1, nonce2_current, codecs.encode(hash2[::-1], 'hex')))
				break
		else:
				print("Numar Testari: {}\nSucces: NU\n    Nonce2: -\n    Hash2: -".format(i+1))

		break


