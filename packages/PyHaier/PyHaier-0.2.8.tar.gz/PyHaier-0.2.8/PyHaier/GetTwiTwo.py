def GetTwiTwo(payload):
    """
    Function for displaying Twi and Two paramameters, return as array
    payload - register from 141 to 156
    TODO: need to confirm its good, Two/Twi cannot be more than 51.1°C
    :return:
    """
    twitwo=[]
    twiob=[f'{divmod(int(hex(payload[5]), 16), 256)[1]:08b}'[0:4], f'{divmod(int(hex(payload[5]), 16), 256)[1]:08b}'[4:]]
    twib=f'{divmod(int(hex(payload[6]), 16), 256)[0]:08b}'
    twob=f'{divmod(int(hex(payload[6]), 16), 256)[1]:08b}'
    twi = int(str(twiob[0])+str(f'{twib:08b}'), 2)/10
    twitwo.append(twi)
    two = int(str(twiob[1])+str(f'{twob:08b}'), 2)/10
    twitwo.append(two)
    return twitwo
