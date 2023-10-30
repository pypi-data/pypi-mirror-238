def GetTdTs(payload):
    """
    Thanks to Daniel Mentel
    Function for displaying Td and Ts paramameters, return as array
    payload - register from 241 to 261
    :return:
    """
    tdts=[]
    td = int(str(f'{divmod(int(hex(payload[10]), 16), 256)[1]:x}')+str(f'{divmod(int(hex(payload[11]), 16), 256)[0]:x}'), 16)/10
    ts = divmod(int(hex(payload[11]), 16), 256)[1]
    tdts.append(td)
    tdts.append(ts)
    return tdts
