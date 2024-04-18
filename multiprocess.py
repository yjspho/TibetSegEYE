
#TibetSegEye MULT
#多进程文本批处理
#

import utils
import models
from importlib import import_module
import torch
import appedix_restore
import thread_u
import tools
from tqdm import tqdm
import torch.multiprocessing as multiprocessing
import time
import numpy as np

np.random.seed(0)
torch.manual_seed(0)
torch.cuda.manual_seed_all(3)
torch.backends.cudnn.deterministic=True
torch.backends.cudnn.benchmark =False

input_path=r'G:\python\2024_new\tokenization_test\file\5K1.txt'
output_path=r'G:\python\2024_new\tokenization_test\file\5K1_div.txt'


if __name__ == '__main__':
    
    
    
    a=time.time()
    config=models.config()
    dictory=appedix_restore.dict_confirm(config)
    process_num=16 # 进程数目 依照个人情况设置
    sym_dic=tools.symbol_define()
    with open(input_path,'r',encoding='utf-8') as con: 
        seq_set=[]
        for line in con:
            line=line.strip()
            if not line:
                continue
            seq_set.append(line) #
        file_num=len(seq_set)
        multiprocessing.set_start_method("spawn")
        multiprocessing.freeze_support() 
        package=multiprocessing.Manager().list()   

        finish_mark=multiprocessing.Value('d',0)


        thr_list=thread_u.path_create(seq_set,process_num)
        thread_u.Pre_Process_combine(process_num,thr_list,dictory,config,package,sym_dic,
                finish_mark)
        
        while finish_mark.value!=process_num:
            time.sleep(2)
            now=0
            if now<len(package):
                
                now=len(package)
                print("{}".format(now))
                

        print("Model start")
        with open(output_path,'w+',encoding='utf-8') as con1:
            #输出位置


            res=[]
            model=models.No_encoder_model(config)
            model.load_state_dict(torch.load(config.save_result))
            model.to(config.device)
            id2label = config.i2b

            res=thread_u.bat_model_use(model,package,id2label,sym_dic)
            for i in tqdm(res):
                con1.write(i)
                con1.write("\n")
            print("process OK! file_num={}".format(file_num))
            b=time.time()
            print("cost time:{}".format(b-a))
        
    


'''

100%|█████████████████████████████████████████████████████████████████████████████████████| 90990/90990 [00:00<00:00, 305071.62it/s]
process OK! file_num=90990
cost time:10609.23495721817


'''


'''

100%|█████████████████████████████████████████████████████████████████████████████████████| 63408/63408 [00:00<00:00, 371734.24it/s]
process OK! file_num=63408
cost time:4915.065074205399


'''

'''
score = torch.where(mask[i].unsqueeze(1), next_score, score)
100%|██████████████████████████████████████████████████████████████████████████████████████████████████████| 11876/11876 [00:00<00:00, 360846.08it/s]
process OK! file_num=11876
cost time:1322.1907305717468


'''

'''
double_test:
可以同时开启多个实例进一步提高运行速度

100%|███████████████████████████████████████████████████████████████████████████████████████| 5085/5085 [00:00<00:00, 463532.03it/s]
process OK! file_num=5085
cost time:966.8390264511108
100%|███████████████████████████████████████████████████████████████████████████████████████| 4720/4720 [00:00<00:00, 315471.76it/s]
process OK! file_num=4720
cost time:957.6709890365601


'''