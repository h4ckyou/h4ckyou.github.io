# Source Generated with Decompyle++
# File: l11l1_442_.pyc (Python 2.7)

import sys
check_version = sys.version_info[0] == 2
sub_const = 2048
mod_const = 7

def decode_unicode(unicode_value):
    last_byte = ord(unicode_value[-1])
    value_exclude_last = unicode_value[:-1]
    mod = last_byte % len(value_exclude_last)
    gen_string = value_exclude_last[:mod] + value_exclude_last[mod:]
    if check_version:
        decoded_value = unicode().join([ unichr(ord(char) - sub_const - (idx + last_byte) % mod_const) for idx, char in enumerate(gen_string) ])
    else:
        decoded_value = str().join([ chr(ord(char) - sub_const - (idx + last_byte) % mod_const) for idx, char in enumerate(gen_string) ])
    return eval(decoded_value)



def help(value):
    if not value:
        print(decode_unicode(u'࡭࡫࡬ࡱࡰࡩࡳࡻ࡜࡯ࡥࡲࡱࡲࡧ࡮ࡥࡵ࡟ࡲ࠯ࡴࡥࡸ࡞ࡱ࠮ࡳ࡫ࡸࡵ࡞ࡱ࠮࡫ࡲࡡࡨ࡞ࡱ࠮࡭࡫࡬ࡱࠀ'))
    else:
        print(decode_unicode(u'࡮ࡥ࡭ࡲࡱࡪࡴࡵ࡝ࡰࡦࡳࡲࡳࡡ࡯ࡦࡶࡠࡳ࠰࡮ࡦࡹ࡟ࡲ࠯ࡴࡥࡹࡶ࡟ࡲ࠯࡮ࡥ࡭ࡲࠁ'))
