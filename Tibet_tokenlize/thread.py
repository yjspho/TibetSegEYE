#多进程的词频计算工具
#需要提供分词工具和原始语料

import multiprocessing

from multiprocessing import Process
from tqdm import tqdm
import utils

import re
import utils


def path_create(seq_set,thread_num):   
    thr_list=[]

    thread_len=len(seq_set)//thread_num +1
    for i in (range(thread_num-1)):
       thr_list.append(seq_set[i*thread_len:(i+1)*thread_len])
    thr_list.append(seq_set[(thread_num-1)*thread_len:])
    return thr_list

def bat_process(seqs,dictory,config,
                package,
                finish_mark):

    for i in seqs:
        seq=utils.source_sequences_add_points_finally(i)
        seq=utils.appedix_restore.fina_del(seq,dictory,config)
        seq_list,seq_len,source_token_Tb=utils.input_process(seq,config)

        package.append([seq_list,seq_len,source_token_Tb]) 

    finish_mark.value+=1




def bat_model_use(model,process_list,id2label):
    res=[]
    for j in process_list:
        pred_tags=[]
        fina_seq=''
        j[0][0]=j[0][0].to('cuda')
        j[0][1]=j[0][1].to('cuda')    
        outputs=model(j[0])
        batch_output = model.crf.decode(outputs[0])
        pred_tags.extend([[id2label.get(idx) for idx in indices if idx > 0] for indices in batch_output])
        pred_tags=pred_tags[0][:j[1]]
        for i in range(len(pred_tags)):
            if pred_tags[i] =='B':
                fina_seq=fina_seq+'\\'+j[2][i]
            elif pred_tags[i] =='M':
                fina_seq=fina_seq+j[2][i]      
            elif pred_tags[i] =='E':
                fina_seq=fina_seq+j[2][i]
            elif pred_tags[i] == 'S':
                fina_seq= fina_seq+'\\'+j[2][i]
        for i in range(len(fina_seq)-1):
            if  utils.Tibet_dect(fina_seq[i])==False and fina_seq[i] not in utils.S_E and fina_seq[i]!='\\':
                if fina_seq[i+1] in utils.S_E:
                    a= fina_seq[:i+2]
                    b=fina_seq[i+2:] 
                    fina_seq=a+'\\'+b
            elif fina_seq[i] in utils.S_D and utils.Tibet_dect(fina_seq[i-2])==True:
                    a= fina_seq[:i]
                    b=fina_seq[i:] 
                    fina_seq=a+'\\'+b
        fina_seq=re.sub(r'\\་','་\\\\',fina_seq)     
        fina_seq=re.sub(r'།་','།',fina_seq)
        res.append(fina_seq)
  
    return res



    


def Process_combine(process_num,seq_set,dictory,config,
                package,
                finish_mark):




    for each in range(process_num):
        thread=Process(target=bat_process,args=(seq_set[each],dictory,config,
                package,
                finish_mark))
        thread.start()  

        
def list_restore(m_list):
    list=[]
    for i in m_list:
        list.append(i)
    return list

           
           

"""



"""