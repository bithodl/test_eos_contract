#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
import os
import commands
import json
from os import path

DEFAULT_ACCOUNT = 'youreosaccount'

def get_counter_json():
    contract_name = 'eos3dio12345'
    cmd = "/bin/sh cleos.sh get table %s %s counter" % (contract_name, contract_name)
    print cmd
    output = commands.getoutput(cmd)
    # print output
    try: 
        content = json.loads(output)
        if content != None:
            print content['rows'][0]
            return content['rows'][0]
    except Exception as e:
        msg = 'Failed to get counter table, Exception: %s' % e
        print msg
        return None


def main():

    while True:   

        counter_json = get_counter_json() 
        if counter_json == None:
            time.sleep(1) 
            continue
        
        last_buyer = counter_json['last_buyer']
        if last_buyer == DEFAULT_ACCOUNT:
            print "last_buyer is me."
        else:
            end_time = counter_json['end_time']
            now_time = int(time.time())
            # print end_time
            
            key_price = float(counter_json['key_price']) / 10000
            print "final time:" + str(end_time - now_time)
            if end_time - now_time < 20:
                cmd = "/bin/sh cleos.sh wallet unlock -n yourwallet --password yourwalletpassword; "
                cmd += "/bin/sh cleos.sh transfer %s  eos3dio12345 '%s EOS'" % (DEFAULT_ACCOUNT, str(key_price))
                print cmd
                os.system(cmd)
        time.sleep(1)        


if __name__ == "__main__":
    main()

