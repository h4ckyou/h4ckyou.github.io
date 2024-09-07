# Source Generated with Decompyle++
# File: main.pyc (Python 2.7)

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


import base64
import time
from Crypto.Cipher import DES
import menu
import seed
import rand

class Program:
    
    def code(self, s):
        return sum(map(ord, s))

    
    def job(self):
        print(decode_unicode(u'ࡨࡰࡨࡵ࡭ࡦ࠮ࡴࡱ࡫ࡡࡴࡧࡩࡳࡺࡥࡳࡼࡳࡺࡸ࡯ࡣࡰࡩ࠿ࠨࠄ')) # -> enter your name
        name = input()
        sum_name = 0

        for i in name:
            sum_name += ord(i)
        
        sum_name %= 225
        sum_name += 95
        print(decode_unicode(u'࡬ࡸ࡯ࡳࡧࠤࡳࡵࡷࠨࠅ') % int(time.time())) # -> current time

        is_used = 1
        while True:
            print(decode_unicode(u'ࡌࡴࡽࡤࡣࡱࠤ࡮ࡨࡦ࡮ࡳࠤࡾࡵࡵ࠮ࠆ') + name + decode_unicode(u'ࡀࠇ')) # -> how can i help you
            choice = input()

            if self.code(choice) == 425: 
                menu.help(is_used)
                continue

            if self.code(choice) == 330:
                seed.new()
                continue

            if self.code(choice) == 447:
                res = rand.guess_random()
                if res % 2 == 1:
                    sum_name -= 1
                    is_used = 0
                    print(decode_unicode(u'ࡤࡶࡵ࡭ࡪࡹࡢࡴࡨࠤࡱ࡫ࡦࡵࠈ') % sum_name)
                
            if self.code(choice) == 410:
                cipher = DES.new(str(sum_name) * 4)
                b64_enc = decode_unicode(u'ࠨ࠹ࡳࡶࡻࡕ࠹ࡕࡴ࠹ࡅ࡭ࡆࡑࡩࡨࡉࡅࡆࡥ࠷ࡏࡍࡹࡗࡈࡴࡍࡘࡏ࡫ࡵࡱࡹ࡮ࡺࡴࡗ࠷࡞࠺ࡹࡧࠉ')
                b64_enc += chr(61)
                b64_decoded = base64.b64decode(b64_enc)
                for i in range(sum_name * 4):
                    decrypted = cipher.decrypt(b64_decoded)
                
                print(base64.b64encode(decrypted))
                continue

            print(decode_unicode(u'ࡘࡴࡲࡲ࡬ࡩ࡯ࡲࡸࡸࠊ')) # -> error msg


if __name__ == '__main__':
    Program().job()
