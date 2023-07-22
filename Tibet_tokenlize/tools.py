
import collections
from transformers.tokenization_utils import PreTrainedTokenizer
import re 
VOCAB_FILES_NAMES = {"vocab_file": "vocab.txt"}

unk_token="[UNK]",
sep_token="[SEP]",
pad_token="[PAD]",
cls_token="[CLS]",
mask_token="[MASK]",
eos_token='[EOS]'
bos_token='[BOS]'

S_E=['་',]
S_F=['།',]
S_double=['༄༅','།།','>>','<<']
S_D=['《','（','》','）','\"','“','”','？','༼','༽','༅','༄༅','—','(',')',':','<','>','·','?','.','༄']
N=['0','1','2','3','4','5','6','7','8','9','༠','༡','༢','༣','༤','༥','༦','༧','༨','༩']
en_word=['a','b','c','d','e','f','g','h','i','j','k','l','m','n'
      ,'o','p','q','r','s','t','u','v','w','x','y','z',
      'A','B','C','D','E','F','G','H','I','J','K','L','M','N',
      'O','P','Q','R','S','T','U','V','W','X','Y','Z']


def read_tokenlize(filename,writename):
    #设置标注标签#

    

    with open (filename,'r',encoding='utf-8') as f:
        with open(writename,'r+',encoding='utf-8') as f1:
            for line in f:
                line=line.strip()
                line=line[:-1]#
                tagging=line.split('/')
                symbol=symbol_creat(tagging)
                symstr=list_to_str(symbol).strip()
                f1.write(symstr+'\n')
    



def symbol_creat(vocab_list):#
    symbol=[]
    appendix_mark=0
    for i in range(len(vocab_list)):
        vocab_list[i]=vocab_list[i].strip()
        if vocab_list[i] =='':
            continue
        elif vocab_list[i] in S_F:
            symbol.append('S ')            
        elif vocab_list[i] in S_D: #
            symbol.append('S ')
        elif vocab_list[i] in N: #
            symbol.append('S ')
        elif vocab_list[i] in S_double: # 
            symbol.append('S ')
        else:

            if appendix_mark==1:
                symbol.append('S_E ') #
                appendix_mark=0
            else :
                if vocab_list[i][-1] not in S_E and i!=len(vocab_list)-1:
                    if vocab_list[i+1] not in (S_F + S_D + N + en_word): 
                        appendix_mark=0
                Tibet_syllable=vocab_list[i].split('་')   #
                if Tibet_syllable[-1]=='':
                    Tibet_syllable=Tibet_syllable[:-1]
                if len(Tibet_syllable) == 1 and appendix_mark!=1:
                    symbol.append('S ')
                else:
                    for j in range(len(Tibet_syllable)):
                        if j==0:
                            symbol.append('B ')
                        elif j!=len(Tibet_syllable)-1:
                            symbol.append('M ')
                        elif j==len(Tibet_syllable)-1 and appendix_mark==0:
                            symbol.append('E ')
    return symbol

def list_to_str(list):
    str1=''
    for i in list:
        str1=str1+i
    return str1

def load_vocab(vocab_file):
    """Loads a vocabulary file into a dictionary."""
    vocab = collections.OrderedDict()
    with open(vocab_file+'\\vocab.txt', "r", encoding="utf-8") as reader:
        tokens = reader.readlines()
    for index, token in enumerate(tokens):
        token = token.rstrip("\n")
        vocab[token] = index
    return vocab


def Tibet_simple_tokenize_old(tibet_str,vocab):

    tibet_str=tibet_str.strip()
    tibet_token_str=''
    for i in range(len(tibet_str)-1):

        if tibet_str[i] in (S_F  + S_D):
            tibet_token_str=tibet_token_str+' '+tibet_str[i]+' '#
        elif tibet_str[i] in (S_E):  
            tibet_token_str=tibet_token_str+' '+tibet_str[i]
        else:
            tibet_token_str=tibet_token_str+tibet_str[i]
    tibet_token_str=tibet_token_str.strip().split(' ')
    for i in tibet_token_str:
        if i not in vocab:
            i=unk_token   #
    while "" in tibet_token_str:
        tibet_token_str.remove("")

    return tibet_token_str   

def Tibet_simple_tokenize(tibet_str,vocab):
    
    tibet_str=tibet_str.strip()
    tibet_token_str=''
    for i in range(len(tibet_str)):
        if tibet_str[i] in (S_F  + S_D):
            tibet_token_str=tibet_token_str+' '+tibet_str[i]+' '#
        elif tibet_str[i] in (S_E):  
            tibet_token_str=tibet_token_str+' '+tibet_str[i]
        else:
            tibet_token_str=tibet_token_str+tibet_str[i]
    tibet_token_str=re.sub(r' ་ ',' ་',tibet_token_str)   
    tibet_token_str=re.sub(r'་ ་',' ་',tibet_token_str)     
    tibet_token_str=tibet_token_str.strip().split(' ')
   


    while "" in tibet_token_str:
        tibet_token_str.remove("")
        
    if len(tibet_token_str)>2:
        if tibet_token_str[-1] ==tibet_token_str[-2]:
            tibet_token_str[-2]=tibet_token_str[-2]+tibet_token_str[-1]
            tibet_token_str.pop()
    return tibet_token_str           
    

def Tibet_convert_dict(vocab_path):
    w2i = {}
    i2w = {}
    vocab = open(vocab_path, "r", encoding="utf-8").read().strip().split("\n")
    print("vocab path: {}, containing words: {}".format(vocab_path, len(vocab)))
    for i, w in enumerate(vocab):
        w2i[w] = i  #word to id
        i2w[i] = w  #id to word 
    return w2i, i2w


def POINT_ADD(filename,writename):

    with open (filename,'r',encoding='utf-8') as f:
        with open(writename,'r+',encoding='utf-8') as f1:
            for line in f:
                line=line.strip()
                for i in range(1,len(line)-1):
                    if line[i] !='་' and line[i+1] =='/' and line[i] not in (S_D+N+ S_F+S_double+en_word):
                        a=line[:i+1]
                        b=line[i+1:]
                        line=a+'་'+b
                f1.write(line+'\n')


