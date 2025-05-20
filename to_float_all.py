import numpy as np

def hex_to_float(hex_list):
    """Convert list of hex strings to float32."""
    return [np.frombuffer(bytes.fromhex(h), dtype=np.float32)[0] for h in hex_list]

def parse_log_lines(lines):
    merged_lines = []
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        parts = line.split()
        if line.endswith("+") or "+\n" in lines[i]:
            if len(parts) >= 7:
                prefix = " ".join(parts[:6])
                hex_value = parts[6].rstrip("+")
                j = i + 1
                while j < len(lines):
                    cont_parts = lines[j].rstrip().split()
                    if len(cont_parts) >= 7:
                        new_hex = cont_parts[6].rstrip("+")
                        hex_value = new_hex + hex_value
                    if not lines[j].endswith("+") and "+\n" not in lines[j]:
                        break
                    j += 1
                remaining_content = ""
                if len(parts) > 7:
                    remaining_content = " " + " ".join(parts[7:])
                merged_line = f"{prefix} {hex_value}{remaining_content}"
                merged_lines.append(merged_line)
                i = j + 1
            else:
                merged_lines.append(line)
                i += 1
        else:
            merged_lines.append(line)
            i += 1
    return merged_lines

def find_log_pattern_index(file_name: str):
    with open(file_name, 'r') as file:
        lines = file.readlines()
        lines = parse_log_lines(lines)

    required_values = ["00123000", "00123456", "00234000", "00234567", "00345000", "00345678"]
    found_values = []
    pattern_indices = []
    current_pattern_start = None

    for i, line in enumerate(lines):
        columns = line.split()
        if len(columns) > 6:
            value = columns[6]
            if value in required_values:
                if current_pattern_start is None and value == required_values[0]:
                    current_pattern_start = i
                found_values.append(value)
            if all(val in found_values for val in required_values):
                pattern_indices.append(current_pattern_start)
                found_values = []
                current_pattern_start = None
            if len(pattern_indices) == 2:
                break
    return pattern_indices

def process_file(file_name: str, delete_log_files: bool = False):
    start_end = find_log_pattern_index(file_name)
    if len(start_end) < 2:
        print("Pattern not found twice in log.")
        return None
    start_index, end_index = start_end
    real, imag = [], []

    with open(file_name, 'r') as file:
        lines = parse_log_lines(file.readlines())

    if delete_log_files:
        import os
        os.remove(file_name)

    save_to_real = True
    is_vectorized = False

    for i in range(start_index, end_index):
        line = lines[i]
        if not is_vectorized:
            if "vsetvli" in line:
                is_vectorized = True
                continue
            if "flw" in line or "c.flw" in line:
                words = line.split()
                op = "flw" if "flw" in line else "c.flw"
                idx = words.index(op)
                if idx > 0:
                    if save_to_real:
                        real.append(words[idx - 1])
                        save_to_real = False
                    else:
                        imag.append(words[idx - 1])
                        save_to_real = True
        else:
            if "vle32.v" in line:
                words = line.split()
                idx = words.index("vle32.v")
                if save_to_real:
                    real.append(words[idx - 1])
                    save_to_real = False
                else:
                    imag.append(words[idx - 1])
                    save_to_real = True

    if is_vectorized:
        realVal, imagVal = [], []
        for r, im in zip(real, imag):
            r_chunks = [r[i:i+8] for i in range(0, len(r), 8)][::-1]
            im_chunks = [im[i:i+8] for i in range(0, len(im), 8)][::-1]
            realVal.extend(r_chunks)
            imagVal.extend(im_chunks)
        real = realVal
        imag = imagVal

    return np.array(hex_to_float(real)) + 1j * np.array(hex_to_float(imag))


if _name_ == "_main_":
    file_path = "fft_vector_output.log"
    complex_vals = process_file(file_path)
    if complex_vals is not None:
        print("Shape:", complex_vals.shape)
        print("First 10 values:")
        print(complex_vals[:10])