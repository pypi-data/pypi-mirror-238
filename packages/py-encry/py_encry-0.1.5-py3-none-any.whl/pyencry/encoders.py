
def encode_rail_fence_cipher(message, rails):
    fence = {}
    for rail in range(rails):
        fence[rail] = ""
    rail = 0
    down = True
    for (idx, item) in enumerate(message):
        fence[rail] += item
        if down:
            rail += 1
        else:
            rail -= 1
        if rail % (rails - 1) == 0 :
            down = not down
    result = ""
    for value in fence.values():
        result += value
    return result
