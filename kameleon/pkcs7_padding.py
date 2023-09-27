# this module add support of padding, using the pkcs7 standard

def pad(data:bytes, block_size:int)->bytes:
    rest = len(data) % block_size
    if rest == 0:
        return data
    
    size = block_size - rest
    pattern = size.to_bytes(1, 'little')
    return data + pattern * size

def unpad(data:bytes, block_size:int)->bytes:

    if len(data) % block_size != 0:
        raise Exception("Block size is incorrect")

    expected_pad = data[-1]

    if expected_pad > block_size-1:
        return data
    
    # validate the paddind
    for i in range(expected_pad):
        if data[-1] != data[-1-i]:
            raise Exception("Invalid padding")
        
    return data[:-expected_pad]
    