import submit_flag
'''
example
'''

#platform_url:str,taken:str,sleep_time:int,target_ip:str,target_port:int
autoFlag = AutoFlag('http://xxx.xxx.xxx.xxx:xxxx/api/flag',
                    '0569615a005d7192cd4db6473de08ee6',
                    5,

                    'xxx.xxx.xxx.xxx',
                    22,
                    'cat /flag',
                    'xxxx',
                    'xxxxx')
autoFlag.submit_flag_nTimes()