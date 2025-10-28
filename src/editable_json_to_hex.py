# editable_json_to_hex.py
import argparse
import sys
import json

def create_hex_line(record: dict) -> str:
    """
    Creates a single line for an Intel HEX file from a structured record.
    It recalculates byte_count and checksum.
    """
    record_type = record["record_type"]
    address = record["address"]

    # Re-encode ASCII data to hex for data records, or use existing hex for others.
    if record_type == 0:
        # Use `latin-1` to ensure every character maps back to a byte value (0-255).
        data_bytes = record["data_ascii"].encode('latin-1')
        data_hex = data_bytes.hex()
    else:
        data_hex = record.get("data_hex", "")

    byte_count = len(data_hex) // 2

    # --- Checksum Recalculation ---
    hex_sum = byte_count
    hex_sum += (address >> 8) & 0xFF
    hex_sum += address & 0xFF
    hex_sum += record_type

    for i in range(0, len(data_hex), 2):
        hex_sum += int(data_hex[i:i+2], 16)

    checksum = (256 - (hex_sum & 0xFF)) & 0xFF
    # --- End Checksum Recalculation ---

    return (f":{byte_count:02X}{address:04X}{record_type:02X}{data_hex}{checksum:02X}").upper()

def convert_editable_json_to_hex(input_path: str, output_path: str):
    """
    Reads an editable JSON file and converts it back to an Intel HEX file.
    """
    print(f"Reading from: {input_path}")
    print(f"Writing to: {output_path}")

    try:
        with open(input_path, 'r', encoding='utf-8') as infile:
            hex_records = json.load(infile)

        with open(output_path, 'w', encoding='utf-8') as outfile:
            for record in hex_records:
                hex_line = create_hex_line(record)
                outfile.write(hex_line + '\n')

        print("Conversion successful!")

    except FileNotFoundError:
        print(f"Error: Input file not found at {input_path}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description="Convert an editable JSON file back to Intel HEX format.")
    parser.add_argument("input_file", help="Path to the input .json file.")
    parser.add_argument("output_file", help="Path for the output .hex file.")
    args = parser.parse_args()
    convert_editable_json_to_hex(args.input_file, args.output_file)

if __name__ == "__main__":
    main()
