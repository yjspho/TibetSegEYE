
#TibetSegEye MULT
#多进程文本批处理
#

import utils
import models
from importlib import import_module
import torch
import appedix_restore
import thread

from tqdm import tqdm
import multiprocessing
import time
import numpy as np

np.random.seed(0)
torch.manual_seed(0)
torch.cuda.manual_seed_all(3)
torch.backends.cudnn.deterministic=True
torch.backends.cudnn.benchmark =False



if __name__ == '__main__':
    config=models.config()
    dictory=appedix_restore.dict_confirm(config)
    process_num=8 # 进程数目 依照个人情况设置
    with open(r'C:\python\2023-1-new\Tibetan\update use\classificate\folkways.txt','r',encoding='utf-8') as con: #读入文本
        seq_set=[]
        for line in con:
            line=line.strip()
            if not line:
                continue
    
            seq_set.append(line) #
        multiprocessing.freeze_support() 
        package=multiprocessing.Manager().list()   

        finish_mark=multiprocessing.Value('d',0)


        thr_list=thread.path_create(seq_set,process_num)
        thread.Process_combine(process_num,thr_list,dictory,config,package,
                finish_mark)
        while finish_mark.value!=process_num:
            time.sleep(5)
            now=0
            if now<len(package):
                now=len(package)
                print("{}".format(now))
                

        print("Model start")
        with open(r'C:\python\2023-1-new\Tibetan\update use\classificate\Sfolkways.txt','r+',encoding='utf-8') as con1:
            #输出位置


            res=[]
            model=models.No_encoder_model(config)
            model.load_state_dict(torch.load(config.save_result))
            model.to(config.device)
            id2label = config.i2b

            res=thread.bat_model_use(model,package,id2label)
            for i in tqdm(res):
                con1.write(i)
                con1.write("\n")
            print("process OK!")

        
    


