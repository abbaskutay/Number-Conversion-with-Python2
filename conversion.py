import sys
'''
IEEE 754-1985 SINGLE FLOATING POINT PRECISION a.k.a float32

number = 0x3E20 0000
memory: 00111110001000000000000000000000 = 
memory: 0 01111100 01000000000000000000000 => sign = 0 exponent = 01111100 rounded_mantissa = 01000000000000000000000
sign = 0 = 0
exponent = 01111100 = 124
rounded_mantissa = 01000000000000000000000 = 0.25
since it is single precision, exponent is 8 bits => bias = (2**(8-1))-1 = 127
real_exponent = exponent - bias = 127 - 124 = -3

number = (-1)**sign * 2(real_exponent) * (1 + rounded_mantissa) = 1 * (1/8) * (1.25) = 0.15625
'''

'''
MODIFIED IEEE 754, MODIFIED EXPONENT AFFECTS FINAL NUMBER

number = 0x3E20 0000
memory: 00111110001000000000000000000000 = 
memory: 0 0111110001 000000000000000000000 => sign = 0 exponent = 0111110001 rounded_mantissa = 000000000000000000000
sign = 0 = 0
exponent = 0111110001 = 497
rounded_mantissa = 000000000000000000000 = 0.0
since it is single precision, exponent is 10 bits => bias = (2**(10-1))-1 = 511
real_exponent = exponent - bias = 497 - 511 = -14

number = (-1)**sign * 2(real_exponent) * (1 + rounded_mantissa) = 1 * (2**(-14)) * (1 + 0.0) = 0.0000610352
'''

def check_hex_value(num):
    full_num = str(num)
    num_nibbles = 0
    ok_number = True
    allowed_digits = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
    for nibble in str(full_num):
        if nibble in allowed_digits:
            num_nibbles += 1
            ok_number = True
        else:
            ok_number = False
            break
    if num_nibbles % 2 == 1:
        full_num = '0'+full_num
    if len(full_num) > 8 or ok_number == False:
        print('Invalid Number. Please use max 4 Bytes and capital letters.')
        sys.exit(1)
    return full_num

    
def convert_nibble_to_binary(nibble):
    ret_val = ''
    if ord(nibble)-ord('0') >= 0 and ord(nibble)-ord('0') <= 9:
        val = int(nibble)
    else:
        val = int(ord(nibble)-ord('A')) + 10
    while val > 0:
        ret_val += str(val % 2)
        val = val / 2
    return (4-len(ret_val))*'0'+ret_val[::-1]


def convert_binary_to_decimal(num):
    ret_val = 0
    for idx,n in enumerate(num[::-1]):
        ret_val += int(n)*2**(idx)
    return ret_val


def convert_fraction_to_decimal(num):
    ret_val = 0.0
    for idx,n in enumerate(num):
        ret_val += int(n)*2**(-idx-1)
    return ret_val


def round_to_even(num):
    rounded = 0
    if num > 0.5:
        rounded = 1
    else:
        rounded = 0
    return rounded
    
    
def convert_hex_to_float(num):
    num_bytes = len(num)/2
    binary = ''
    exp_len = 2*num_bytes + 2
    sign_len = 1
    rounding = 8*num_bytes - exp_len - sign_len
    if num_bytes in [3,4]:
        rounding = 13
    bias = 2**(exp_len-1)-1
    for i in num:
        binary += convert_nibble_to_binary(i)
    exp_part = binary[1:exp_len+1]
    rest = binary[exp_len+1:][rounding:]
    rounded = str(round_to_even(convert_fraction_to_decimal(rest)))
    rounded_mantissa = binary[exp_len+1:][:rounding-1]+rounded
    mantissa = binary[exp_len+1:]
    sign = binary[0]
    fraction = 1.0 + convert_fraction_to_decimal(rounded_mantissa)
    if '0' not in exp_part and ('0' in mantissa and '1' in mantissa):
        return "NaN"
    elif '0' not in exp_part and ('1' not in mantissa):
        res = '-Inf'if sign == '1' else "Inf"
        return res
    elif '1' not in exp_part and ('1' not in mantissa):
        res = '-0'if sign == '1' else "0"
        return res
    decimal = ((-1)**int(sign)) * (2**(convert_binary_to_decimal(exp_part)-bias)) * fraction
    dec_flt = str(decimal).split('e')
    decimal = "%.5f"%(float(dec_flt[0])) if len(dec_flt) == 1 else "%.5f"%(float(dec_flt[0])) + 'e' + dec_flt[1]
    return decimal


def convert_hex_to_signed(num):
    binary = ''
    first_complement = ''
    for i in num:
        binary += convert_nibble_to_binary(i)
    if binary[0] == '1':
        for b in binary:
            first_complement += '1' if b == '0' else '0'
        second_complement = convert_binary_to_decimal(first_complement) + 1
        final_num = int(second_complement) * (-1)**int(binary[0])
    else:
        final_num = convert_binary_to_decimal(binary)
    return final_num


def convert_hex_to_unsigned(num):
    binary = ''
    for i in num:
        binary += convert_nibble_to_binary(i)
    final_num = convert_binary_to_decimal(binary)
    return final_num


    
if __name__ == '__main__':
    """Enter hex number in with capital letters: ABCDEF
    Enter data type with capital letters: FSU"""
    '''
    0x78 & 0xF8 => Inf and -Inf
    0x00 & 0x80 => 0 and -0
    0x7A,0x79 & 0xFA,0xF9 => NaN
    '''
    number = input("Enter a hex number: ")
    type = input("Enter a conversion type: ")
    num = check_hex_value(number)
    if type == 'F':
        print(convert_hex_to_float(num))
    elif type == 'S':
        print(convert_hex_to_signed(num))
    elif type == 'U':
        print(convert_hex_to_unsigned(num))