
def pretty_print_bytes(data):
    hex_repr = data.hex()
    formatted = ' '.join(hex_repr[i:i+2].upper() for i in range(0, len(hex_repr), 2))
    grouped = [formatted[i:i+48] for i in range(0, len(formatted), 48)]
    return '\n'.join(grouped)

