
from tqdm import tqdm
from torch.utils.data import TensorDataset,DataLoader
import torch.nn as nn
import torch
import time
import pickle as pkl
import os
from  datetime import timedelta
import tools 
import re
import appedix_restore
        
PAD,CLS='[PAD]','[CLS]'
SEP='[SEP]'

def load_dataset(file_path,config):

    contents=[]

    Tibet_tokenizer=config.tokenizer
    vocab = tools.load_vocab(config.model_path)
    with open(file_path,'r',encoding='UTF-8') as f:
            for line in tqdm(f):
                line=line.strip() 
                if not line:
                    continue
                source_sequences,target_sequences=line.split('\t')

                source_token_Tb=tools.Tibet_simple_tokenize(source_sequences,vocab) 
                target_token=target_sequences.split(' ')

                source_token_Tb_len=len(source_token_Tb)
                target_seq_len=len(target_token)
                
                    
                target_token=target_convert_to_id(target_token,config.b2i)
                
                mask=[]
                source_token_ids_Tb=Tibet_tokenizer.convert_tokens_to_ids(source_token_Tb)
                

                
                pad_size=config.pad_size
                
                if pad_size:
                    if len(source_token_Tb)<pad_size:
                        mask=[1]*len(source_token_ids_Tb)+([0]*(pad_size-source_token_Tb_len))
                        source_token_ids_Tb=source_token_ids_Tb+([0]*(pad_size-source_token_Tb_len))
                    else:
                        mask=[1]*pad_size 
                        source_token_ids_Tb=source_token_ids_Tb[:pad_size]

                    
                    if len(target_token)<pad_size:
                        
                        target_token=target_token+([0]*(pad_size-target_seq_len))
                    else:
                        target_token=target_token[:pad_size]
                    
                
                contents.append([source_token_ids_Tb,target_token,source_token_Tb_len,target_seq_len,mask])
                
            if len(contents)==0:
                print("error is here")
                print("error is here")    
    return contents

            
def build_dataset1(config):
    train=load_dataset(config.train,config)  
    dev=load_dataset(config.dev,config)
    test=load_dataset(config.test,config)

    return train ,dev, test


def data_loader(config,content):
    source_token_ids=torch.LongTensor([item[0] for item in content]).to(config.device) 
    
    target_token_ids=(torch.LongTensor([item[1] for item in content]).to(config.device))
    
    source_seq=torch.LongTensor([item[2] for item in content]).to(config.device)
    
    
    target_seq=torch.LongTensor([item[3] for item in content]).to(config.device)
    
    mask=torch.LongTensor([item[4] for item in content]).to(config.device)
    data = TensorDataset(source_token_ids,mask,source_seq,target_seq,target_token_ids)
    loader = DataLoader(data, batch_size=config.batch_size, shuffle=True)
    return loader


def build_dataset(config):
    '''

    
    '''

    if os.path.exists(config.datasetpk):

        dataset=pkl.load(open(config.datasetpk,'rb'))
        train=dataset['train']
        dev=dataset['dev']
        test=dataset['test']
        if config.split_head!=0:
            for i in train:
                    i[3]=i[3]+[1]*config.split_head   
                    
            for i in test:
                    i[3]=i[3]+[1]*config.split_head
            for i in dev:
                    i[3]=i[3]+[1]*config.split_head     
    else:
        
        train=load_dataset(config.train,config)  
        dev=load_dataset(config.dev,config)
        test=load_dataset(config.test,config)
        dataset={}
        dataset['train']=train
        dataset['dev']=dev
        dataset['test']=test
        pkl.dump(dataset,open(config.datasetpk,'wb'))
        if config.split_head!=0:
            for i in train:
                    i[3]=i[3]+[1]*config.split_head 
                    
            for i in test:
                    i[3]=i[3]+[1]*config.split_head
            for i in dev:
                    i[3]=i[3]+[1]*config.split_head  
    return train ,dev, test

    
def get_time_dif(start_time):
    '''
    获取使用时间
    '''
    end_time=time.time()
    time_dif =end_time-start_time
    return timedelta(seconds=int(round(time_dif)))

def list_add(a,b):
    if len(a)!=len(b):
        return False
    else:
        for i in range(len(a)):
            a[i]=a[i]+b[i]

def target_convert_to_id(target,b2i):
    
    target_id=[]
    for i in target:
        target_id.append(b2i[i])
    return target_id
    '''
    for i in target:
         i=b2i[i]
    return target
    '''


def source_sequences_add_points(source_sequences,sym_dic):
    '''
    为藏文数字和符号 字母统一添加S_E 方便tokenlize操作
    默认字母后面加·
    '''
    for i in range(len(source_sequences)-1):
        
        if source_sequences[i]in sym_dic['N'] and source_sequences[i+1] not in (sym_dic['S_E']+sym_dic['N']) and i!=len(source_sequences)-1: 

            a=source_sequences[:i+1]
            b=source_sequences[i+1:]
            source_sequences=a+sym_dic['S_E'][0]+b
        elif source_sequences[i] not in (sym_dic['S_E']+sym_dic['S_D']+sym_dic['S_F']+sym_dic['S_double']+sym_dic['N']+sym_dic['en_word']) and source_sequences[i+1] in sym_dic['N'] :

            a=source_sequences[:i+1]
            b=source_sequences[i+1:]
            source_sequences=a+sym_dic['S_E'][0]+b
        elif Chinese_dect(source_sequences[i])==True and Chinese_dect(source_sequences[i+1])==False : 

            a=source_sequences[:i+1]
            b=source_sequences[i+1:]
            source_sequences=a+sym_dic['S_E'][0]+b
        elif (Chinese_dect(source_sequences[i])==False and source_sequences[i] not in sym_dic['S_E']) and Chinese_dect(source_sequences[i+1])==True :

            a=source_sequences[:i+1]
            b=source_sequences[i+1:]
            source_sequences=a+sym_dic['S_E'][0]+b
            
            '''
            
            
            '''     
        elif source_sequences[i] in sym_dic['en_word']:
            if source_sequences[i+1] not in sym_dic['en_word']:
                
                a=source_sequences[:i+1]
                b=source_sequences[i+1:]
                source_sequences=a+sym_dic['S_E'][0]+b 


            
        elif   source_sequences[i] not in (sym_dic['S_E']+sym_dic['S_D']+sym_dic['S_F']+sym_dic['S_double']+sym_dic['N']+sym_dic['en_word']) and source_sequences[i+1] in (sym_dic['S_D']+sym_dic['S_F']+sym_dic['S_double']+sym_dic['N']+sym_dic['en_word']) :

            a=source_sequences[:i+1]
            b=source_sequences[i+1:]
            source_sequences=a+sym_dic['S_E'][0]+b

        elif source_sequences[i] in sym_dic['S_D'] and source_sequences[i+1] not in  ['༅' , '>' , '<'] : 
            
            
            if source_sequences[i-1] in sym_dic['S_E']: 
                a=source_sequences[:i+1]
                b=source_sequences[i+1:]
                source_sequences=a+sym_dic['S_E'][0]+b 
            elif source_sequences[i+1] not in (sym_dic['S_E']+sym_dic['S_F']+sym_dic['S_D']): 
                a=source_sequences[:i+1]
                b=source_sequences[i+1:]
                source_sequences=a+sym_dic['S_E'][0]+b 
            elif source_sequences[i+1] in sym_dic['S_D']: 
                a=source_sequences[:i+1]
                b=source_sequences[i+2:]
                c=source_sequences[i+1]
                source_sequences=a+sym_dic['S_E'][0]+c+sym_dic['S_E'][0]+b
        elif source_sequences[i]  in  ['༄' , '།' , '>' , '<'] : 
            if source_sequences[i+1]  in  ['༅' , '།' , '>' , '<'] :
                a=source_sequences[:i+2]
                b=source_sequences[i+2:]
                source_sequences=a+sym_dic['S_E'][0]+b          
            else:
                a=source_sequences[:i+1]
                b=source_sequences[i+1:]
                source_sequences=a+sym_dic['S_E'][0]+b        
        else:
            if else_dect(source_sequences[i],sym_dic)==True and else_dect(source_sequences[i+1],sym_dic)==False and i!=len(source_sequences)-1: 

                a=source_sequences[:i+1]
                b=source_sequences[i+1:]
                source_sequences=a+sym_dic['S_E'][0]+b
            elif else_dect(source_sequences[i],sym_dic)==False and else_dect(source_sequences[i+1],sym_dic)==True and i!=len(source_sequences)-1:

                a=source_sequences[:i+1]
                b=source_sequences[i+1:]
                source_sequences=a+sym_dic['S_E'][0]+b

    if source_sequences[-1] in sym_dic['S_F'] and source_sequences[-2] not in sym_dic['S_E']:
        a=source_sequences[:-1]
        b=source_sequences[-1]
        source_sequences=a+sym_dic['S_E'][0]+b     
    source_sequences=re.sub(r'།',"་།",source_sequences)
    submark=True
    ori_len=len(source_sequences)
    while submark:
        source_sequences=re.sub(r'་་',"་",source_sequences)
        if len(source_sequences)==ori_len:
            submark=False
        else:
            ori_len=len(source_sequences)    
    
    return source_sequences

def source_sequences_add_points_finally(source_sequences,sym_dic):
    source_sequences=source_sequences_add_points(source_sequences,sym_dic)
    source_sequences=source_sequences_add_points(source_sequences,sym_dic)
    return source_sequences

def input_process(language_seq,config,sym_dic):

    vocab = tools.load_vocab(config.model_path)
    source_sequences=source_sequences_add_points_finally(language_seq,sym_dic)

    source_token_Tb=tools.Tibet_simple_tokenize(source_sequences,vocab,sym_dic) 
    pad_size=config.pad_size
    source_token_ids_Tb=config.tokenizer.convert_tokens_to_ids(source_token_Tb)
    seq_len=len(source_token_ids_Tb)
    if pad_size:
        if len(source_token_Tb)<pad_size:
            mask=[1]*len(source_token_ids_Tb)+([0]*(pad_size-len(source_token_Tb)))
            source_token_ids_Tb=source_token_ids_Tb+([0]*(pad_size-len(source_token_Tb)))
        else:
            mask=[1]*pad_size 
            source_token_ids_Tb=source_token_ids_Tb[:pad_size]
    source_token_ids_Tb=torch.LongTensor([source_token_ids_Tb])
    mask=torch.LongTensor([mask])
    
    return [source_token_ids_Tb,mask],seq_len,source_token_Tb

    

def model_use(model,config,seq,dictory,id2label,sym_dic):
    pred_tags=[]
    fina_seq=''
    seq=seq.strip()
    seq=source_sequences_add_points_finally(seq,sym_dic)
    seq=appedix_restore.fina_del(seq,dictory,config,sym_dic) 
    seq_list,seq_len,source_token_Tb=input_process(seq,config,sym_dic)
    seq_list[0]=seq_list[0].to(device=config.device)
    seq_list[1]=seq_list[1].to(device=config.device)
    outputs=model(seq_list)
    batch_output = model.crf.decode(outputs[0])
    pred_tags.extend([[id2label.get(idx) for idx in indices if idx > 0] for indices in batch_output])
    pred_tags=pred_tags[0][:seq_len]
    for i in range(len(pred_tags)):
        if pred_tags[i] =='B':
            fina_seq=fina_seq+'\\'+source_token_Tb[i]
        elif pred_tags[i] =='M':
            fina_seq=fina_seq+source_token_Tb[i]      
        elif pred_tags[i] =='E':
            fina_seq=fina_seq+source_token_Tb[i]
        elif pred_tags[i] == 'S':
            fina_seq= fina_seq+'\\'+source_token_Tb[i]
    for i in range(len(fina_seq)-1):
        if  Tibet_dect(fina_seq[i],sym_dic)==False and fina_seq[i] not in sym_dic['S_E'] and fina_seq[i]!='\\':
            if fina_seq[i+1] in sym_dic['S_E']:
                a= fina_seq[:i+2]
                b=fina_seq[i+2:] 
                fina_seq=a+'\\'+b
        elif fina_seq[i] in sym_dic['S_D'] and Tibet_dect(fina_seq[i-2],sym_dic)==True:
                a= fina_seq[:i]
                b=fina_seq[i:] 
                fina_seq=a+'\\'+b
    fina_seq=re.sub(r'\\་','་\\\\',fina_seq)     
    fina_seq=re.sub(r'།་','།',fina_seq)
    
    return fina_seq


def Chinese_dect(char):
    if ord(char) <=0x9fbb and ord(char) >=0x4e00:
        return True
    else:
        return False
    
def Tibet_dect(char,sym_dic):
    '''
    
    '''
    if ord(char) <=0x0fff and ord(char) >=0x0f00:
        if char not in sym_dic['S_E']:
            return True
        else:
            return False
    else:
        return False
    
def else_dect(char,sym_dic):
    if Chinese_dect(char)==False and Tibet_dect(char,sym_dic)==False:
        if char not in (sym_dic['S_E']+sym_dic['S_F']+sym_dic['S_D']+sym_dic['en_word']+sym_dic['N']):
            return True
        
    else:
        return False
        
        
def symbol_dect(str,sym_dic):
    char=str[0]
    if char in sym_dic['S_F']:
        return True
    elif char in sym_dic['S_D']:
        return True
    elif char in sym_dic['en_word']:
        return True
    elif char in sym_dic['N']:
        return True
    elif Chinese_dect(char)==True:
        return True
    else:
        return False
    


