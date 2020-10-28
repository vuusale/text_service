import os
import multiprocessing as mp

def run_command(options):
    os.system(f"python3 client.py {options}")

pool = mp.Pool(3)
results = pool.map(run_command, ["-m change_text -t sample.txt -k swap.json", \
    "-m encode_decode -t sample.txt -k key.txt", \
    "-m change_text -t big.txt -k swap.json"] )

