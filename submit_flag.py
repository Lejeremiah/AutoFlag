import requests
import time
import os
import paramiko
import my_log
import logging

class AutoFlag():
    '''
    针对单一目标的自动化flag提交工具
    '''
    def __init__(self,
                 platform_url:str,
                 taken:str,
                 sleep_time:int,
                 target_ip:str,
                 target_port:int,
                 target_payload:str,
                 target_username=None,
                 target_password=None):
        self.target_ip = target_ip
        self.target_port = target_port
        self.target_payload = target_payload
        self.target_ssh = None
        self.target_username = target_username
        self.target_password = target_password

        self.platform_url = platform_url
        self.taken = taken
        self.sleep_time = sleep_time

        self.flags_log_filename = f'./logs/{self.target_ip}.txt'
        self.count = 0
        self.ssh_retry = 3

        if not os.path.exists('./logs/'):
            os.makedirs('./logs/')
        with open(f'./logs/{self.target_ip}.txt','a+') as f:
            f.write('\n')

    def check_flag(self,target_flag) -> bool:
        '''
        从日志中寻找上一轮提交过的flag，看是否和上一轮的重复
        '''
        if 'flag{' in target_flag:
            f = open(self.flags_log_filename, 'r')
            lines = f.readlines()
            f.close()

            for line in lines:
                if target_flag in line:
                    # print(f'[flag-exist]:{target_flag}')
                    logging.info(f'[flag-exist]:{target_flag}')
                    return False
            with open(self.flags_log_filename,'a+') as f:
                f.write(target_flag+'\n')
            # print(f"[flag-writed]:{target_flag}")
            logging.info(f"[flag-writed]:{target_flag}")
            return True
        else:
            # print(f"[flag-error]:{target_flag}")
            logging.error(f"[flag-error]:{target_flag}")
            return False



    def get_flag_byGet(self):
        url = f"http://{self.target_ip}:{self.target_port}{self.target_payload}"
        response_flag = requests.get(url).text
        if self.check_flag(response_flag):
            return response_flag
        else:
            return None


    def get_flag_byPost(self):
        '''
        针对flag获取不是GET请求的情况下做扩展
        '''
        pass


    def init_SSH(self) -> bool:
        try:
            self.target_ssh = paramiko.SSHClient()
            self.target_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.target_ssh.connect(hostname=self.target_ip,port=self.target_port,username=self.target_username,password=self.target_password)
            return True
        except Exception as e:
            # print(f'[initSSH-error]:{str(e)}')
            logging.error(f'[initSSH-error]:{str(e)}')
            return False
    def get_flag_bySSH(self):
        if self.init_SSH():
            try:
                cmd = self.target_payload.encode()
                # print(cmd)
                logging.info(f'[payload-info]:{cmd.decode()}')
                stdin,stdout,stderr = self.target_ssh.exec_command(cmd)
                flag = stdout.read().decode().strip()
                if not flag:
                    flag = stderr.read()
                    self.target_ssh.close()
                    # print(f'[ssh-error]:{flag}')
                    logging.error(f'[ssh-error]:{flag}')
                    return None
                self.target_ssh.close()
                if self.check_flag(flag):
                    return flag
                else:
                    return None
            except Exception as e:
                # print(f'[ssh-cmdError]:{str(e)}):')
                logging.error(f'[ssh-cmdError]:{str(e)}):')
                self.target_ssh.close()
                self.target_ssh = None
                if self.ssh_retry > 0:
                    self.ssh_retry = self.ssh_retry - 1
                    return self.get_flag_bySSH()
                else:
                    return None
        else:
            pass

    def submit_flag_once(self):
        flag = self.get_flag_bySSH()
        if flag:
            '''
            更具比赛平台提供的接口具体再修改
            '''
            headers = {
                'Content-Type':'application/json',
                'Authorization':self.taken
            }
            data = {
                'flag':flag
            }
            try:
                response = requests.post(self.platform_url,headers=headers,json=data).text
            except Exception as e:
                # print(f"[requests-error]:{str(e)}")
                logging.error(f"[requests-error]:{str(e)}")
                return False
            return [flag,response]
        else:
            return False


    def submit_flag_nTimes(self):
        while True:
            # print(f"count:{self.count}")
            logging.info(f"count:{self.count}")
            result = self.submit_flag_once()
            if result:
                # print(f'[submit-info]:{result[0]}---{result[1]}')
                logging.info(f'[submit-info]:{result[0]}---{result[1]}')
            else:
                # print('[submit-info]:error')
                logging.error('[submit-info]:error')
            time.sleep(60*self.sleep_time)
            self.count = self.count + 1

