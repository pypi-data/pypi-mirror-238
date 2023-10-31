import struct, sys, binascii


def Perfact_Reverse_forfloat_encoding(hex_str):
    #把十六进制字符串倒过来分组逆序后= 14f1bf71 newstr= 71bff114
    # 每两个字符分组
    if isinstance(hex_str, bytes):
        print("输入的是bytes")
        hex_str = binascii.hexlify(hex_str).decode()
    else:
        print("输入的不是bytes")
    hex_str_groups = [hex_str[i:i + 2] for i in range(0, len(hex_str), 2)]

    # 逆序输出并合并为一个字符串
    hex_str_reversed = ''.join(hex_str_groups[::-1])

    # 补零，使字符串长度为2的倍数
    if len(hex_str_reversed) % 2 == 1:
        hex_str_reversed += '0'
    return hex_str_reversed


def perfact_hex2float(hex_str):
    print(f"转换类似“4479fff0”这样的十六进制字符串为浮点数,参数为：{hex_str}")
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
    if isinstance(hex_str, bytes):
        print("输入的是bytes")
        hex_str = binascii.hexlify(hex_str).decode()
        print(f"输入的是bytes，最初二进制数据为{hex_str}，经过hexlify后的hex_str=", hex_str)
    else:
        print("输入的不是bytes")

    reversed_hex = Perfact_Reverse_forfloat_encoding(hex_str)
    print("result=", reversed_hex)

    date = int(reversed_hex, 16)  # 将十六进制字符串转换为整数
    date_str = str(date)

    return date_str


def wm_hex_to_date_str(hex_str):
    hex_str = hex_str[::-1]  # 反转列表中的元素顺序=

    date = int(hex_str, 16)  # 将十六进制字符串转换为整数
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


def decode_tdx_binary_data(binary_data):
    decoded_data = []
    for i in range(0, len(binary_data), 8):
        #每批8字节，每次4字节，分2部分解析
        # 解析日期
        date_bytes = binary_data[i:i + 4]
        print("tdx start, original date_bytes=", date_bytes)  #b'\xe5\x8b4\x01'
        dateint = wm_hex_to_date(date_bytes)
        print("int_date_==", dateint)
        decoded_data.append(dateint)
        # 解析定点数

        fixed_point_bytes = binary_data[i + 4:i + 8]
        print("original fixed_point_bytes=", fixed_point_bytes)
        hex_string = ''.join([f'{byte:02x}' for byte in fixed_point_bytes])
        print("converted hex=", hex_string)  #00008040，顺序同二进制存放，所以要先分组逆序
        resvered_hex_string = Perfact_Reverse_forfloat_encoding(hex_string)
        print("resvered hex string = ", resvered_hex_string)

        result = perfact_hex2float(resvered_hex_string)
        end_number = result[0]
        print("result=", result)
        decoded_data.append(round(end_number, 3))

    return decoded_data


def 反日期(hex_str):
    #把十六进制字符串倒过来分组逆序后= 14f1bf71 newstr= 71bff114
    # 每两个字符分组
    hex_str_groups = [hex_str[i:i + 2] for i in range(0, len(hex_str), 2)]

    # 逆序输出并合并为一个字符串
    hex_str_reversed = ''.join(hex_str_groups[::-1])

    # 补零，使字符串长度为2的倍数
    if len(hex_str_reversed) % 2 == 1:
        hex_str_reversed += '0'
    return hex_str_reversed


def date_to_hex(date_str):
    date_int = int(date_str)
    hex_code = hex(date_int)[2:].zfill(8).upper()  # 将日期转换为十六进制并填充为8位
    hex_code = ' '.join([hex_code[i:i + 2] for i in range(6, -2, -2)])  # 逆序每两个字符分组
    return hex_code


if __name__ == "__main__":
    print(date_to_hex("20220901"))
    sys.exit()

    # in_day_file = "f0ff7944"

    # hex_str_reversed = Perfact_Reverse_forfloat_encoding(in_day_file)

    # print("sample 1",hex_str_reversed)

    # print(perfact_hex2float(hex_str_reversed))

    # print("-"*40)
    print("sample 2 通达信数据读取")
    path = r"D:/Soft/_Stock/通达信开心果202310/T0002/signals/signals_user_999"
    code = "000001"
    market = int(code.startswith("6"))
    tdx_file = path + f"/{market}_{code}.dat"
    print("tdx file= ", tdx_file)
    with open(tdx_file, 'rb') as file:
        # 读取原始数据
        binary_data = file.read()
        print("读取的通达信文件的原始数据：")
        print(binary_data)
        result = decode_tdx_binary_data(binary_data)
        print("result=", result)
