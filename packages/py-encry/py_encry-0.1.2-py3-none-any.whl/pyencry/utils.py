from random import seed, randint

def get_pixels(width, height):
    for n in range(width):
        for m in range(height):
            yield (n, m)


def encode_data_to_pixel(pixel, data):
    new_pixel = [0, 0, 0, 0]

    data = bin(data)

    i = 0
    while i <= 3:
        channel = pixel[i]

        # Konverterar data till binärt i en sträng med korrekt antal siffror (8) 
        binary_data = f"0b{"0" * (10 - len(data))}{data[2:]}"
        
        # Plockar ut delen av datan att sätta i varje pixel
        subdata = int((binary_data)[2*i+2 : 2*i+4], 2)

        # Sätter in data
        channel = channel >> 2 << 2 
        channel += subdata
        
        new_pixel[i] = channel

        i += 1

    return tuple(new_pixel)


def decode_data_from_pixel(pixel):
    data = "0b"

    for channel in pixel:

        if len(bin(channel)) < 4:
            binary_data = f"0b0{bin(channel)[-1]}"
        else:
            binary_data = bin(channel)

        data += binary_data[-2:]

    data = int(data, 2)
    return data

  
def get_rail_fence_pixels(width, height, rail_fence_height):
    for n in range(width):
        for m in range(height):
            if m % (rail_fence_height * 2 - 2) == n % (rail_fence_height * 2 - 2):
                yield (n, m)

def get_random_spacing_pixels(width, height, key):
    seed(key)
    i = 0
    while i <= height:
        j = 0
        while j <= width:
            j += randint(1,5)
            yield(i, j)
        i += 1

