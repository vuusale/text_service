import os
import argparse
import random
import string

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, help="File to create OTP for")
    parser.add_argument("-o", "--output", type=str, help="Output file name")
    args = parser.parse_args()

    size = os.path.getsize(args.file)

    otp = "".join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation) for _ in range(size))

    with open(args.output, "w") as f:
        f.write(otp)
    print(f"OTP successfully created > {args.output}")

if __name__ == "__main__":
    main()