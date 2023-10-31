import struct, sys


def perfact_rever_forfloat_encoding(hex_str):
    #把十六进制字符串倒过来
    # 每两个字符分组
    hex_str_groups = [hex_str[i:i + 2] for i in range(0, len(hex_str), 2)]

    # 逆序输出并合并为一个字符串
    hex_str_reversed = ''.join(hex_str_groups[::-1])

    # 补零，使字符串长度为2的倍数
    if len(hex_str_reversed) % 2 == 1:
        hex_str_reversed += '0'
    return hex_str_reversed


def perfact_hex2float(hex_str):
    print("hex_str=", hex_str)
    #hex_str= 4479fff0
    int_value = int(hex_str, 16)
    print("int_value=", int_value)
    a = struct.pack('>I', int_value)
    print("a=", a)
    b = struct.unpack('>f', a)
    f = b[0]
    print("nixiangf=", f)
    return b


def wm_hex_to_date(hex_str):
    #['ED', '8B', '34', '01']
    print("输入参数为：", hex_str)
    result = perfact_rever_forfloat_encoding(hex_str)
    print("result=", result)
    hex_list = hex_str.split(' ')  # 将输入的字符串以空格分割成一个列表
    print(hex_list)  #['01', '34', '8B', 'ED']
    hex_list.reverse()  # 反转列表中的元素顺序

    print(hex_list)
    #10438bde
    hex_code = ''.join(hex_list)  # 将列表中的元素拼接为一个字符串
    print("hex_code=", hex_code)  #hex_code= 01348BED
    date = int(hex_code, 16)  # 将十六进制字符串转换为整数
    date_str = str(date)

    # 在需要的位置插入分隔符，例如 "20220909" 转换为 "2022-09-09"
    date_str = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"

    return date_str


def wm_hex_to_date_str(hex_str):
    hex_str = hex_str[::-1]  # 反转列表中的元素顺序=

    date = int(hex_code, 16)  # 将十六进制字符串转换为整数
    date_str = str(date)

    # 在需要的位置插入分隔符，例如 "20220909" 转换为 "2022-09-09"
    date_str = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"

    return date_str


def wm_float_to_hex(f):
    # 将浮点数转换为十六进制字符串
    hex_str = hex(struct.unpack('>I', struct.pack('>f', f))[0])[2:]

    # 每两个字符分组
    hex_str_groups = [hex_str[i:i + 2] for i in range(0, len(hex_str), 2)]

    # 逆序输出并合并为一个字符串
    hex_str_reversed = ''.join(hex_str_groups[::-1])

    # 补零，使字符串长度为2的倍数
    if len(hex_str_reversed) % 2 == 1:
        hex_str_reversed += '0'

    # 将十六进制字符串转换为二进制数据
    binary = bytes.fromhex(hex_str_reversed)

    return binary


def decode_binary_data(binary_data):
    import struct

    decoded_data = []

    for i in range(0, len(binary_data), 8):
        # 解析日期
        date_bytes = binary_data[i:i + 4]
        dateint = wm_hex_to_date(date_bytes)
        print("int_date_==", dateint)

        # 解析定点数

        fixed_point_bytes = binary_data[i + 4:i + 8]
        print("original fixed_point_bytes=", fixed_point_bytes)
        hex_string = ''.join([f'{byte:02x}' for byte in fixed_point_bytes])
        print("converted hex=", hex_string)
        print("-----ex_tohresult------ = ", perfact_rever_forfloat_encoding(hex_string))
        int_value = int(hex_string, 16)

        print("int_value=", int_value)
        a = struct.pack('>I', int_value)
        print("a=", a)
        b = struct.unpack('>f', a)
        f = b[0]
        print("nixiangf=", f)

    return decoded_data


if __name__ == "__main__":
    in_day_file = "f0ff7944"

    hex_str_reversed = perfact_rever_forfloat_encoding(in_day_file)

    print(hex_str_reversed)

    print(perfact_hex2float(hex_str_reversed))
    path = r"D:/Soft/_Stock/通达信开心果202310/T0002/signals/signals_user_999"
    code = "000001"
    market = int(code.startswith("6"))
    tdx_file = path + f"/{market}_{code}.dat"
    print("tdx file= ", tdx_file)
    with open(tdx_file, 'rb') as file:
        # 读取原始数据
        binary_data = file.read()
        print("原始数据：")
        print(binary_data)
        result = decode_binary_data(binary_data)
        print("result=", result)
        reversed_ex = perfact_rever_forfloat_encoding(binary_data)
        print(perfact_hex2float(reversed_ex))
