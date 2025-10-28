# hex_to_editable.py
import argparse
import sys
import json

def parse_hex_line(line: str, line_num: int) -> dict:
    """
    Parses a single line of an Intel HEX file and returns a structured dictionary.
    """
    if not line.startswith(':'):
        return None

    try:
        hex_string = line.strip()[1:]
        byte_count = int(hex_string[0:2], 16)
        address = int(hex_string[2:6], 16)
        record_type = int(hex_string[6:8], 16)

        data_start_index = 8
        data_end_index = data_start_index + (byte_count * 2)
        data_hex = hex_string[data_start_index:data_end_index]

        # --- Checksum Verification ---
        checksum_from_file = int(hex_string[data_end_index:data_end_index + 2], 16)
        calculated_sum = 0
        for i in range(0, len(hex_string) - 2, 2):
            calculated_sum += int(hex_string[i:i+2], 16)
        calculated_checksum = (256 - (calculated_sum & 0xFF)) & 0xFF

        if checksum_from_file != calculated_checksum:
            print(f"Warning: Checksum mismatch on line {line_num}: {line.strip()}", file=sys.stderr)
            return None
        # --- End Checksum Verification ---

        # For data records, convert data to ASCII for editing.
        # For all other records, just store the raw data hex.
        if record_type == 0:
            data_bytes = bytes.fromhex(data_hex)
            # Use `latin-1` to ensure every byte value (0-255) maps to a character.
            data_ascii = data_bytes.decode('latin-1')
            return {
                "record_type": record_type,
                "address": address,
                "data_ascii": data_ascii
            }
        else:
            return {
                "record_type": record_type,
                "address": address,
                "data_hex": data_hex
            }

    except (ValueError, IndexError) as e:
        print(f"Warning: Could not parse line {line_num}: {line.strip()}. Error: {e}", file=sys.stderr)
        return None

def convert_hex_to_editable_json(input_path: str, output_path: str):
    """
    Reads an Intel HEX file and converts it to a structured, editable JSON file.
    """
    print(f"Reading from: {input_path}")
    print(f"Writing to: {output_path}")
    hex_records = []

    try:
        with open(input_path, 'r', encoding='utf-8') as infile:
            for i, line in enumerate(infile, 1):
                record = parse_hex_line(line, i)
                if record:
                    hex_records.append(record)

        with open(output_path, 'w', encoding='utf-8') as outfile:
            json.dump(hex_records, outfile, indent=2, ensure_ascii=False)

        print("Conversion successful!")

    except FileNotFoundError:
        print(f"Error: Input file not found at {input_path}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description="Convert an Intel HEX file to an editable JSON file.")
    parser.add_argument("input_file", help="Path to the input .hex file.")
    parser.add_argument("output_file", help="Path for the output .json file.")
    args = parser.parse_args()
    convert_hex_to_editable_json(args.input_file, args.output_file)

if __name__ == "__main__":
    main()
