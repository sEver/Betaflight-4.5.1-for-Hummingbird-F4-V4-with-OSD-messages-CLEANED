# hex_to_raw_ascii.py
import argparse
import sys

def convert_hex_to_raw_ascii(input_path: str, output_path: str):
    """
    Converts each line of an Intel HEX file into its raw byte representation
    and saves it to an editable ASCII file using 'latin-1' encoding.
    """
    print(f"Reading from: {input_path}")
    print(f"Writing to: {output_path}")

    try:
        # Use 'latin-1' for output to ensure a 1-to-1 mapping for all 256 byte values.
        with open(input_path, 'r', encoding='ascii') as infile, open(output_path, 'w', encoding='latin-1') as outfile:
            for line in infile:
                stripped_line = line.strip()
                if not stripped_line.startswith(':'):
                    continue
                
                # Convert the entire hex string (e.g., "020000040800F2") to bytes
                hex_data = stripped_line[1:]
                raw_bytes = bytes.fromhex(hex_data)
                
                # Decode bytes into a 'latin-1' string and write to file
                outfile.write(raw_bytes.decode('latin-1') + '\n')

        print("Conversion successful!")

    except FileNotFoundError:
        print(f"Error: Input file not found at {input_path}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description="Convert an Intel HEX file to a raw, editable ASCII file.")
    parser.add_argument("input_file", help="Path to the input .hex file.")
    parser.add_argument("output_file", help="Path for the output raw ASCII file.")
    args = parser.parse_args()
    convert_hex_to_raw_ascii(args.input_file, args.output_file)

if __name__ == "__main__":
    main()

