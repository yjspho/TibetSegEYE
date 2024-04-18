from pickle import TRUE
import tqdm
import utils
import re
import tools

def dict_confirm(config):
    dictory=[]
    with open(config.supvoc,'r',encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue 
            dictory.append(line)
        return dictory       
    
super_appendix= [chr(0x0F62),chr(0x0F63),chr(0x0F66)]
overlying_base=[chr(0x0F90),chr(0x0F91),chr(0x0F92),chr(0x0F93),chr(0x0F94),chr(0x0F95),chr(0x0F96),chr(0x0F97),chr(0x0F98),chr(0x0F99),
           chr(0x0F9A),chr(0x0F9B),chr(0x0F9C),chr(0x0F9D),chr(0x0F9E),chr(0x0F9F),chr(0x0FA0),chr(0x0FA1),chr(0x0FA2),chr(0x0FA3),
           chr(0x0FA4),chr(0x0FA5),chr(0x0FA6),chr(0x0FA7),chr(0x0FA8),chr(0x0FA9),chr(0x0FAA),chr(0x0FAB),chr(0x0FAC),chr(0x0FAD),chr(0x0FAE),
           chr(0x0FAF),chr(0x0FB0),chr(0x0FB1),chr(0x0FB2),chr(0x0FB3),chr(0x0FB4),chr(0x0FB5),chr(0x0FB6),chr(0x0FB7),chr(0x0FB8),
           chr(0x0FB9),chr(0x0FBA),chr(0x0FBB),chr(0x0FBC),chr(0x0FBD)]
subscribed_appendix=[chr(0x0FB1),chr(0x0FB2),chr(0x0FB3),chr(0x0FBA)]
subscribed_appendix_2nd=['ྭ']
front_appendix=[chr(0x0F42),chr(0x0F51),chr(0x0F56),chr(0x0F58),chr(0x0F60)]
gen_appendix=[chr(0x0F72),chr(0x0F7A),chr(0x0F74),chr(0x0F7C)]
suffix_2nd=[chr(0x0F51),chr(0x0F66)]

def tibet_to_digit(str_temp):
    
    structure = dict()
    mark=0
    if len(str_temp) == 1:
        structure["root"] = str_temp[0]
        mark=1        
    elif len(str_temp) == 2:

        if str_temp[1] == chr(0x0F72) or str_temp[1] == chr(
                0x0F74) or str_temp[1] == chr(0x0F7A) or str_temp[1] == chr(
                    0x0F7C):
            if str_temp[0] >= chr(0x0F40) and str_temp[0] <= chr(0x0F6C):
            
            
                structure["root"] = str_temp[0]
                structure["vowel"] = str_temp[1]
                mark=1
        elif str_temp[1] >= chr(0x0F40) and str_temp[1] <= chr(0x0F6C):
            
            
            if str_temp[0] >= chr(0x0F40) and str_temp[0] <= chr(0x0F6C):
                structure["root"] = str_temp[0]
                structure["suffix"] = str_temp[1]
                mark=1
        elif str_temp[1] in overlying_base:
            
            if str_temp[1] in subscribed_appendix:
                
                
                structure["root"] = str_temp[0]
                structure["subscribed"] = str_temp[1]
                mark=1
            else:
                
                if str_temp[0] in super_appendix:
                        structure["superscribed"] = str_temp[0]
                        structure["root"] = str_temp[1]
                        mark=1                
    elif len(str_temp) == 3:
        if str_temp[2] in gen_appendix:
            
            if str_temp[1] >= chr(0x0F40) and str_temp[1] <= chr(0x0F6C):
                if str_temp[0] in front_appendix:
                
                
                    structure["prefix"] = str_temp[0]
                    structure["root"] = str_temp[1]
                    structure["vowel"] = str_temp[2]
                    mark=1
            elif str_temp[1] in overlying_base and str_temp[1] in subscribed_appendix:
                
                
                    structure["root"] = str_temp[0]
                    structure["subscribed"] = str_temp[1]
                    structure["vowel"] = str_temp[2]
                    mark=1
            elif str_temp[0] in super_appendix and str_temp[1] in overlying_base :
                
                structure["superscribed"] = str_temp[0]
                structure["root"] = str_temp[1]
                structure["vowel"] = str_temp[2]
                mark=1
        elif str_temp[1] in gen_appendix:
            
            
            structure["root"] = str_temp[0]
            structure["vowel"] = str_temp[1]
            structure["suffix"] = str_temp[2]
            mark=1
        else:
            if (str_temp[1] >= chr(0x0F40) and str_temp[1] <= chr(0x0F6C)
                ) and (str_temp[2] >= chr(0x0F40)
                       and str_temp[2] <= chr(0x0F6C)):
                
                if (str_temp[2] == chr(0x0F51) and
                    (str_temp[1] == chr(0x0F53) or str_temp[1] == chr(0x0F62)
                     or str_temp[1] == chr(0x0F63))) or (
                         str_temp[2] == chr(0x0F66) and
                         (str_temp[1] == chr(0x0F42) or str_temp[1]
                          == chr(0x0F44) or str_temp[1] == chr(0x0F56)
                          or str_temp[1] == chr(0x0F58))):
                    
                    
                    structure["root"] = str_temp[0]
                    structure["suffix"] = str_temp[1]
                    structure["suffix_2nd"] = str_temp[2]
                    mark=1
                elif str_temp[0] in front_appendix:
                    
                    structure["prefix"] = str_temp[0]
                    structure["root"] = str_temp[1]
                    structure["suffix"] = str_temp[2]
                    mark=1
            elif (str_temp[1] >= chr(0x0F40) and str_temp[1] <= chr(0x0F6C)
                  ) and str_temp[2] in overlying_base :
                
                if str_temp[2] in subscribed_appendix and str_temp[0] in front_appendix:
                    
                    
                    structure["prefix"] = str_temp[0]
                    structure["root"] = str_temp[1]
                    structure["subscribed"] = str_temp[2]
                    mark=1
                else:
                    
                    if str_temp[0] in front_appendix and str_temp[1] in super_appendix:
                        structure["prefix"] = str_temp[0]
                        structure["superscribed"] = str_temp[1]
                        structure["root"] = str_temp[2]
                        mark=1
            elif str_temp[1] in overlying_base and str_temp[2] in overlying_base:
                
                if str_temp[1] in subscribed_appendix and str_temp[2] in subscribed_appendix_2nd:
                    
                    
                    structure["root"] = str_temp[0]
                    structure["subscribed"] = str_temp[1]
                    structure["subscribed_2nd"] = str_temp[2]
                    mark=1
                elif str_temp[0] in super_appendix:
                    
                    structure["superscribed"] = str_temp[0]
                    structure["root"] = str_temp[1]
                    structure["subscribed"] = str_temp[2]
                    mark=1
            elif (str_temp[1] in overlying_base
                  ) and (str_temp[2] >= chr(0x0F40)
                         and str_temp[2] <= chr(0x0F6C)):
                
                if str_temp[1] in subscribed_appendix:
                    
                    
                    structure["root"] = str_temp[0]
                    structure["subscribed"] = str_temp[1]
                    structure["suffix"] = str_temp[2]
                    mark=1
                elif str_temp[0] in super_appendix:
                    
                    structure["superscribed"] = str_temp[0]
                    structure["root"] = str_temp[1]
                    structure["suffix"] = str_temp[2]
                    mark=1
    elif len(str_temp) == 4:
        if str_temp[3] in gen_appendix:
            
            if str_temp[1] >= chr(0x0F40) and str_temp[1] <= chr(0x0F6C):
                
                if str_temp[2] in subscribed_appendix:
                    
                    
                    structure["prefix"] = str_temp[0]
                    structure["root"] = str_temp[1]
                    structure["subscribed"] = str_temp[2]
                    structure["vowel"] = str_temp[3]
                    mark=1
                elif str_temp[0] in front_appendix and str_temp[2] in overlying_base and str_temp[1] in super_appendix:
                    
                    structure["prefix"] = str_temp[0]
                    structure["superscribed"] = str_temp[1]
                    structure["root"] = str_temp[2]
                    structure["vowel"] = str_temp[3]
                    mark=1
            else:
                if (str_temp[1] not in subscribed_appendix) and (str_temp[2] in subscribed_appendix) and(str_temp[1] in overlying_base):
                    
                    
                    structure["superscribed"] = str_temp[0]
                    structure["root"] = str_temp[1]
                    structure["subscribed"] = str_temp[2]
                    structure["vowel"] = str_temp[3]
                    mark=1
                elif (str_temp[1] in subscribed_appendix) and (str_temp[2] in subscribed_appendix_2nd):
                    
                    
                    structure["root"] = str_temp[0]
                    structure["subscribed"] = str_temp[1]
                    structure["subscribed_2nd"] = str_temp[2]
                    structure["vowel"] = str_temp[3]
                    mark=1
        elif str_temp[2] in gen_appendix:
            
            if str_temp[1] >= chr(0x0F40) and str_temp[1] <= chr(0x0F6C):
                if str_temp[0] in front_appendix :
                
                
                    structure["prefix"] = str_temp[0]
                    structure["root"] = str_temp[1]
                    structure["vowel"] = str_temp[2]
                    structure["suffix"] = str_temp[3]
                    mark=1
            else:
                if str_temp[1] in subscribed_appendix :
                    
                    
                    structure["root"] = str_temp[0]
                    structure["subscribed"] = str_temp[1]
                    structure["vowel"] = str_temp[2]
                    structure["suffix"] = str_temp[3]
                    mark=1
                elif str_temp[0] in super_appendix and str_temp[1] in overlying_base:
                    
                    structure["superscribed"] = str_temp[0]
                    structure["root"] = str_temp[1]
                    structure["vowel"] = str_temp[2]
                    structure["suffix"] = str_temp[3]
                    mark=1
        elif str_temp[1] in gen_appendix:
            
            
            if str_temp[3] in suffix_2nd:
                structure["root"] = str_temp[0]
                structure["vowel"] = str_temp[1]
                structure["suffix"] = str_temp[2]
                structure["suffix_2nd"] = str_temp[3]
                mark=1
        else:
            if str_temp[3] >= chr(0x0F40) and str_temp[3] <= chr(0x0F6C):
                
                if (str_temp[1] >= chr(0x0F40) and str_temp[1] <= chr(0x0F6C)
                    ) and (str_temp[2] >= chr(0x0F40)
                           and str_temp[2] <= chr(0x0F6C)):
                    
                    
                    if str_temp[3] in suffix_2nd:
                        structure["prefix"] = str_temp[0]
                        structure["root"] = str_temp[1]
                        structure["suffix"] = str_temp[2]
                        structure["suffix_2nd"] = str_temp[3]
                        mark=1
                elif (str_temp[1] >= chr(0x0F40) and str_temp[1] <= chr(0x0F6C)
                      ) and (str_temp[2] in overlying_base):
                    
                    if str_temp[2] in subscribed_appendix:
                        
                        
                        structure["prefix"] = str_temp[0]
                        structure["root"] = str_temp[1]
                        structure["subscribed"] = str_temp[2]
                        structure["suffix"] = str_temp[3]
                        mark=1
                    elif str_temp[0] in front_appendix and str_temp[1] in super_appendix:
                        
                        structure["prefix"] = str_temp[0]
                        structure["superscribed"] = str_temp[1]
                        structure["root"] = str_temp[2]
                        structure["suffix"] = str_temp[3]
                        mark=1
                elif (str_temp[1] in overlying_base) and (str_temp[2] >= chr(0x0F40)
                             and str_temp[2] <= chr(0x0F6C)):
                    
                    if str_temp[1] in subscribed_appendix:
                        
                        
                        if str_temp[3] in suffix_2nd:
                            structure["root"] = str_temp[0]
                            structure["subscribed"] = str_temp[1]
                            structure["suffix"] = str_temp[2]
                            structure["suffix_2nd"] = str_temp[3]
                            mark=1
                    elif str_temp[0] in super_appendix and str_temp[3] in suffix_2nd:
                        
                        structure["superscribed"] = str_temp[0]
                        structure["root"] = str_temp[1]
                        structure["suffix"] = str_temp[2]
                        structure["suffix_2nd"] = str_temp[3]
                        mark=1
                elif (str_temp[1] in overlying_base
                      ) and (str_temp[2] in overlying_base):
                    
                    if str_temp[1] in subscribed_appendix and str_temp[2] in subscribed_appendix_2nd:
                        
                        
                        structure["root"] = str_temp[0]
                        structure["subscribed"] = str_temp[1]
                        structure["subscribed_2nd"] = str_temp[2]
                        structure["suffix"] = str_temp[3]
                        mark=1
                    elif str_temp[0] in super_appendix and str_temp[2] in subscribed_appendix:
                        
                        structure["superscribed"] = str_temp[0]
                        structure["root"] = str_temp[1]
                        structure["subscribed"] = str_temp[2]
                        structure["suffix"] = str_temp[3]
                        mark=1
            elif str_temp[0] in front_appendix and str_temp[1] in super_appendix and str_temp[2] in overlying_base and str_temp[3] in subscribed_appendix:
                
                structure["prefix"] = str_temp[0]
                structure["superscribed"] = str_temp[1]
                structure["root"] = str_temp[2]
                structure["subscribed"] = str_temp[3]
                mark=1
    elif len(str_temp) == 5:
        if str_temp[4] in gen_appendix:
            
            
            if str_temp[0] in front_appendix and str_temp[1] in super_appendix and str_temp[2] in overlying_base and str_temp[3] in subscribed_appendix:
                structure["prefix"] = str_temp[0]
                structure["superscribed"] = str_temp[1]
                structure["root"] = str_temp[2]
                structure["subscribed"] = str_temp[3]
                structure["vowel"] = str_temp[4]
                mark=1
        elif str_temp[3] in gen_appendix:
            
            if str_temp[1] in subscribed_appendix and str_temp[2] in subscribed_appendix_2nd:
                
                
                structure["root"] = str_temp[0]
                structure["subscribed"] = str_temp[1]
                structure["subscribed_2nd"] = str_temp[2]
                structure["vowel"] = str_temp[3]
                structure["suffix"] = str_temp[4]
                mark=1
            elif (str_temp[1] in overlying_base) and (str_temp[1] not in subscribed_appendix) :
                
                
                if str_temp[2] in subscribed_appendix and str_temp[0] in super_appendix:
                    structure["superscribed"] = str_temp[0]
                    structure["root"] = str_temp[1]
                    structure["subscribed"] = str_temp[2]
                    structure["vowel"] = str_temp[3]
                    structure["suffix"] = str_temp[4]
                    mark=1
            elif str_temp[1] >= chr(0x0F40) and str_temp[1] <= chr(0x0F6C):
                
                if str_temp[2] in subscribed_appendix:
                    
                    
                    if str_temp[3] in gen_appendix:
                        structure["prefix"] = str_temp[0]
                        structure["root"] = str_temp[1]
                        structure["subscribed"] = str_temp[2]
                        structure["vowel"] = str_temp[3]
                        structure["suffix"] = str_temp[4]
                        mark=1
                elif str_temp[0] in front_appendix and str_temp[2] in overlying_base and str_temp[3] in gen_appendix:
                    if str_temp[1] in super_appendix:
                    
                        structure["prefix"] = str_temp[0]
                        structure["superscribed"] = str_temp[1]
                        structure["root"] = str_temp[2]
                        structure["vowel"] = str_temp[3]
                        structure["suffix"] = str_temp[4]
                        mark=1
        elif str_temp[2] in gen_appendix:
            
            if str_temp[1] >= chr(0x0F40) and str_temp[1] <= chr(0x0F6C):
                
                
                if str_temp[0] in front_appendix and str_temp[4] in suffix_2nd:
                    structure["prefix"] = str_temp[0]
                    structure["root"] = str_temp[1]
                    structure["vowel"] = str_temp[2]
                    structure["suffix"] = str_temp[3]
                    structure["suffix_2nd"] = str_temp[4]
                    mark=1
            else:
                if str_temp[1] in subscribed_appendix:
                    
                    
                    if str_temp[4] in subscribed_appendix_2nd:
                        structure["root"] = str_temp[0]
                        structure["subscribed"] = str_temp[1]
                        structure["vowel"] = str_temp[2]
                        structure["suffix"] = str_temp[3]
                        structure["suffix_2nd"] = str_temp[4]
                        mark=1
                elif str_temp[0] in super_appendix and str_temp[1] in overlying_base:
                    if str_temp[4] in suffix_2nd:
                    
                        structure["superscribed"] = str_temp[0]
                        structure["root"] = str_temp[1]
                        structure["vowel"] = str_temp[2]
                        structure["suffix"] = str_temp[3]
                        structure["suffix_2nd"] = str_temp[4]
                        mark=1
        else:
            if (str_temp[0] >= chr(0x0F40) and str_temp[0] <= chr(0x0F6C)
                ) and (str_temp[1] in overlying_base) and (str_temp[2] in overlying_base):
                
                if str_temp[1] in subscribed_appendix and str_temp[2] in subscribed_appendix_2nd and str_temp[4] in suffix_2nd:
                    
                    
                    structure["root"] = str_temp[0]
                    structure["subscribed"] = str_temp[1]
                    structure["subscribed_2nd"] = str_temp[2]
                    structure["suffix"] = str_temp[3]
                    structure["suffix_2nd"] = str_temp[4]
                    mark=1
                elif str_temp[2] in subscribed_appendix and str_temp[4] in suffix_2nd and str_temp[0] in super_appendix:
                    
                    structure["superscribed"] = str_temp[0]
                    structure["root"] = str_temp[1]
                    structure["subscribed"] = str_temp[2]
                    structure["suffix"] = str_temp[3]
                    structure["suffix_2nd"] = str_temp[4]
                    mark=1
            elif (str_temp[1] >= chr(0x0F40) and str_temp[1] <= chr(0x0F6C)
                  ) and (str_temp[2] in overlying_base) and (str_temp[3] in overlying_base):
                
                
                if str_temp[0] in front_appendix and str_temp[3] in subscribed_appendix and str_temp[1] in super_appendix:
                    structure["prefix"] = str_temp[0]
                    structure["superscribed"] = str_temp[1]
                    structure["root"] = str_temp[2]
                    structure["subscribed"] = str_temp[3]
                    structure["suffix"] = str_temp[4]
                    mark=1
            else:
                if str_temp[2] in subscribed_appendix:
                    
                    
                    if str_temp[0] in front_appendix and str_temp[4] in suffix_2nd:
                        structure["prefix"] = str_temp[0]
                        structure["root"] = str_temp[1]
                        structure["subscribed"] = str_temp[2]
                        structure["suffix"] = str_temp[3]
                        structure["suffix_2nd"] = str_temp[4]
                        mark=1
                else:
                    
                    if str_temp[0] in front_appendix and str_temp[1] in super_appendix:
                        if str_temp[2] in overlying_base and str_temp[4] in suffix_2nd:
                            structure["prefix"] = str_temp[0]
                            structure["superscribed"] = str_temp[1]
                            structure["root"] = str_temp[2]
                            structure["suffix"] = str_temp[3]
                            structure["suffix_2nd"] = str_temp[4]
                            mark=1
    elif len(str_temp) == 6:
        if str_temp[4] in gen_appendix:
            
            
            if str_temp[0] in front_appendix and str_temp[1] in super_appendix:
                if str_temp[2] in overlying_base and str_temp[3] in subscribed_appendix:
                    structure["prefix"] = str_temp[0]
                    structure["superscribed"] = str_temp[1]
                    structure["root"] = str_temp[2]
                    structure["subscribed"] = str_temp[3]
                    structure["vowel"] = str_temp[4]
                    structure["suffix"] = str_temp[5]
                    mark=1
        elif str_temp[3] in gen_appendix:
            
            if str_temp[1] in overlying_base:
                
                if str_temp[1] in subscribed_appendix and str_temp[2] in subscribed_appendix_2nd:
                    
                    
                    structure["root"] = str_temp[0]
                    structure["subscribed"] = str_temp[1]
                    structure["subscribed_2nd"] = str_temp[2]
                    structure["vowel"] = str_temp[3]
                    structure["suffix"] = str_temp[4]
                    structure["suffix_2nd"] = str_temp[5]
                    mark=1
                elif str_temp[0] in front_appendix and str_temp[2] in subscribed_appendix and str_temp[5] in suffix_2nd:
                    
                    structure["superscribed"] = str_temp[0]
                    structure["root"] = str_temp[1]
                    structure["subscribed"] = str_temp[2]
                    structure["vowel"] = str_temp[3]
                    structure["suffix"] = str_temp[4]
                    structure["suffix_2nd"] = str_temp[5]
                    mark=1
            elif str_temp[1] >= chr(0x0F40) and str_temp[1] <= chr(0x0F6C):
                
                if str_temp[2] in subscribed_appendix:
                    
                    
                    if str_temp[0] in front_appendix and str_temp[5] in suffix_2nd:
                        structure["prefix"] = str_temp[0]
                        structure["root"] = str_temp[1]
                        structure["subscribed"] = str_temp[2]
                        structure["vowel"] = str_temp[3]
                        structure["suffix"] = str_temp[4]
                        structure["suffix_2nd"] = str_temp[5]
                        mark=1
                elif str_temp[0] in front_appendix and str_temp[1] in super_appendix:
                    
                    if str_temp[2] in overlying_base and str_temp[5] in suffix_2nd:
                        structure["prefix"] = str_temp[0]
                        structure["superscribed"] = str_temp[1]
                        structure["root"] = str_temp[2]
                        structure["vowel"] = str_temp[3]
                        structure["suffix"] = str_temp[4]
                        structure["suffix_2nd"] = str_temp[5]
                        mark=1
        elif str_temp[0] in front_appendix and str_temp[1] in super_appendix:
            if str_temp[2] in overlying_base and str_temp[3] in subscribed_appendix and str_temp[5] in suffix_2nd:
            
                structure["prefix"] = str_temp[0]
                structure["superscribed"] = str_temp[1]
                structure["root"] = str_temp[2]
                structure["subscribed"] = str_temp[3]
                structure["suffix"] = str_temp[4]
                structure["suffix_2nd"] = str_temp[5]
                mark=1
    elif len(str_temp) == 7:
        if str_temp[0] in front_appendix and str_temp[1] in super_appendix:
            if str_temp[2] in overlying_base and str_temp[3] in subscribed_appendix and str_temp[4] in gen_appendix and str_temp[6] in suffix_2nd:
                structure["prefix"] = str_temp[0]
                structure["superscribed"] = str_temp[1]
                structure["root"] = str_temp[2]
                structure["subscribed"] = str_temp[3]
                structure["vowel"] = str_temp[4]
                structure["suffix"] = str_temp[5]
                structure["suffix_2nd"] = str_temp[6]
                mark=1
        
    return mark


def input_sim_space(text,divide_mark=' '):
    if text[-1]==divide_mark:
        text=text[:-1]
    if divide_mark==' ': 
        text=text.strip()       
        text_temp=text.split(' ')
    elif divide_mark=='་':
        text=text.strip()     
        text_temp=text.split('་')        
    return  text_temp   



def input_sim_tibet(text):
    text=text.strip()       
    text_temp=text.split('་')
    return  text_temp   






def preserve(text_temp,dictory,config,sym_dic):
    i=0
    end_mark=0
    while(i<len(text_temp)):   
        mark2=0  
        
        if len(text_temp[i])!=0 and utils.symbol_dect(text_temp[i][0],sym_dic)==True:
            end_mark=i
        
        elif len(text_temp[i])>=2 :
            if ((text_temp[i][-1] == 'ི' and text_temp[i][-2] == 'འ') or
                (text_temp[i][-1] == 'ི' and text_temp[i][-2] == 'ཡ') or
                (text_temp[i][-1] == 'ས' or (text_temp[i][-1] == 'ས' and text_temp[i][-2] == 'ི' and ((text_temp[i][-3] == 'ཡ' or text_temp[i][-3] =='འ') ) )) or 
                (text_temp[i][-1] == 'ར' ) or 
                (text_temp[i][-1] == 'ང' and (text_temp[i][-2] == 'ཡ' or text_temp[i][-2] == 'འ')) or 
                (text_temp[i][-1] == 'མ' and text_temp[i][-2] == 'འ')  
                ):
                

                if i-end_mark>config.slide_size:
                    slide_window=config.slide_size
                else:
                    slide_window=i-end_mark-1
                re_count=config.slide_size
                
                if i>=config.slide_size and (len(text_temp)-i)>config.slide_size: 
                    
                    test=''
                    front=''
                    rear=''
                    '''
                    for j in range(i-slide_window,i,1):
                        front=front+' '+text_temp[j]     
                        new_slide+=1
                    '''
                    front=text_temp[i-slide_window:i]
                        
                    for j in range(i+config.slide_size,i,-1):
                        if utils.symbol_dect(text_temp[i][0],sym_dic)==True:
                            re_count=j
                            break
                    rear=text_temp[i+1:re_count+1]
                            
                            
                   
                    front_count=slide_window
                    rear_copy=rear
                    for j in range(len(front),-1,-1):  
                        
                        if len(rear_copy)+front_count>=config.limit_preserve:
                            
                            
                            test=' '.join(front)+' '+text_temp[i]+' '+' '.join(rear_copy)
                            test=test.strip(' ')

                            for k in range(i+len(rear_copy),i-1,-1):
                                
                                if test in dictory:  
                                        mark2=1      
                                        
                                        
                                        text_temp.insert(i,'⊙')
                                        text_temp.insert(k+2,'ꈍ')
                                        end_mark=k+2
                                        
                                        i=k+2
                                        
                                        break
                                
                                else:
                                    rear_copy=rear_copy[:-1]  
                                    test=' '.join(front)+' '+text_temp[i]+' '+' '.join(rear_copy)
                                    test=test.strip(' ')
                                    
                            if test in dictory and mark2!=1:
                                    mark2=1      
                                    
                                    
                                    text_temp.insert(i,'⊙')
                                    text_temp.insert(k+2,'ꈍ')
                                    end_mark=k+2
                                    
                                    i=k+2
                            if mark2==1:
                                
                                break
                            else:
                                
                                front=front[1:]
                                front_count-=1     
                                rear_copy=rear            
                        else:
                            break        

                elif i>=config.slide_size and (len(text_temp)-i)<config.slide_size:  
                    test=''
                    front=''
                    rear=''
                    front=text_temp[i-slide_window:i]
                        
                    for j in range(len(text_temp)-1,i,-1):
                        if utils.symbol_dect(text_temp[i][0],sym_dic)==True:
                            re_count=j
                            break
                    rear=text_temp[i+1:re_count+1]
                            
                            
                   
                    front_count=slide_window
                    rear_copy=rear
                                    
                    for j in range(len(front),-1,-1):
                        
                        if len(rear_copy)+front_count>=config.limit_preserve:
                            
                            
                            test=' '.join(front)+' '+text_temp[i]+' '+' '.join(rear_copy)
                            test=test.strip(' ')

                            for k in range(i+len(rear_copy),i-1,-1):
                                
                                if test in dictory:  
                                        mark2=1      
                                        
                                        
                                        text_temp.insert(i,'⊙')
                                        text_temp.insert(k+2,'ꈍ')
                                        end_mark=k+2
                                        
                                        i=k+2
                                        break
                                
                                else:
                                    rear_copy=rear_copy[:-1]  
                                    test=' '.join(front)+' '+text_temp[i]+' '+' '.join(rear_copy)
                                    test=test.strip(' ')
                                    
                            if test in dictory and mark2!=1:
                                    mark2=1      
                                    
                                    
                                    text_temp.insert(i,'⊙')
                                    text_temp.insert(k+2,'ꈍ')
                                    end_mark=k+2
                                    
                                    i=k+2
                            if mark2==1:
                                
                                break
                            else:
                                
                                front=front[1:]
                                front_count-=1     
                                rear_copy=rear            
                        else:
                            break        
                                
                elif i<config.slide_size and (len(text_temp)-i)>config.slide_size: 
                    
                        test=''
                        front=''
                        rear=''
                        '''
                        for j in range(i-slide_window,i,1):
                            front=front+' '+text_temp[j]     
                            new_slide+=1
                        '''
                        front=text_temp[i-slide_window:i]
                            
                        for j in range(i+config.slide_size,i,-1):
                            if utils.symbol_dect(text_temp[i][0],sym_dic)==True:
                                re_count=j
                                break
                        rear=text_temp[i+1:re_count+1]
                                
                                
                    
                        front_count=slide_window
                        rear_copy=rear
                        for j in range(len(front),-1,-1):
                            
                            if len(rear_copy)+front_count>=config.limit_preserve:
                                
                                
                                test=' '.join(front)+' '+text_temp[i]+' '+' '.join(rear_copy)
                                test=test.strip(' ')

                                for k in range(i+len(rear_copy),i-1,-1):
                                    
                                    if test in dictory:  
                                            mark2=1      
                                            
                                            
                                            text_temp.insert(i,'⊙')
                                            text_temp.insert(k+2,'ꈍ')
                                            end_mark=k+2
                                            
                                            i=k+2
                                            
                                            break
                                    
                                    else:
                                        rear_copy=rear_copy[:-1]  
                                        test=' '.join(front)+' '+text_temp[i]+' '+' '.join(rear_copy)
                                        test=test.strip(' ')
                                        
                                if test in dictory and mark2!=1:
                                        mark2=1      
                                        
                                        
                                        text_temp.insert(i,'⊙')
                                        text_temp.insert(k+2,'ꈍ')
                                        end_mark=k+2
                                        
                                        i=k+2
                                if mark2==1:
                                    
                                    break
                                else:
                                    
                                    front=front[1:]
                                    front_count-=1     
                                    rear_copy=rear            
                            else:
                                break      
                elif i<config.slide_size and (len(text_temp)-i)<config.slide_size: 
                        test=''
                        front=''
                        rear=''
                        '''
                        for j in range(i-slide_window,i,1):
                            front=front+' '+text_temp[j]     
                            new_slide+=1
                        '''
                        front=text_temp[i-slide_window:i]
                            
                        for j in range(len(text_temp)-1,i,-1):
                            if utils.symbol_dect(text_temp[i][0],sym_dic)==True:
                                re_count=j
                                break
                        rear=text_temp[i+1:re_count+1]
                                
                                
                    
                        front_count=slide_window
                        rear_copy=rear
                        for j in range(len(front),-1,-1):
                            
                            if len(rear_copy)+front_count>=config.limit_preserve:
                                
                                
                                test=' '.join(front)+' '+text_temp[i]+' '+' '.join(rear_copy)
                                test=test.strip(' ')

                                for k in range(i+len(rear_copy),i-1,-1):
                                    
                                    if test in dictory:  
                                            mark2=1      
                                            
                                            
                                            text_temp.insert(j,'⊙')
                                            text_temp.insert(k+2,'ꈍ')
                                            end_mark=k+2
                                            
                                            i=k+2
                                            break
                                    
                                    else:
                                        rear_copy=rear_copy[:-1]  
                                        test=' '.join(front)+' '+text_temp[i]+' '+' '.join(rear_copy)
                                        test=test.strip(' ')
                                        
                                if test in dictory and mark2!=1:
                                        mark2=1      
                                        
                                        
                                        text_temp.insert(i,'⊙')
                                        text_temp.insert(k+2,'ꈍ')
                                        end_mark=k+2
                                        
                                        i=k+2
                                if mark2==1:
                                    
                                    break
                                else:
                                    
                                    front=front[1:]
                                    front_count-=1     
                                    rear_copy=rear            
                            else:
                                break        
                
                
                if (len(text_temp[i])>=3 or text_temp[i][-1]=='ས')  and (utils.Tibet_dect(text_temp[i][0],sym_dic)==True) and text_temp[i][0] not in (sym_dic['S_D']+sym_dic['N']+sym_dic['S_E']+sym_dic['S_F']) and mark2==0:
                    
                    if (text_temp[i][-1] == 'ར' ):  
                        
                        test2=text_temp[i][:-1] 
                        
                        test_ori2=test2
                        if i>config.slide_size:
                            for j in range(i-1,i-config.slide_size,-1):
                                
                                test2=text_temp[j]+' '+test2
                            test2=test2.strip(' ')   
                            
                            for j in range(i-config.slide_size+1,i+1):   
                                '''                        
                                if test1 in dictory:
                                    mark2=2  
                                    
                                    
                                    text_temp[i]=test_ori2   
                                    text_temp.insert(i+1,'ར')
                                    break
                                '''
                                if test2 in dictory:
                                    mark2=2  
                                    
                                    text_temp[i]=test_ori2
                                    text_temp.insert(i+1,'ར')    
                                    break
                                else:
                                    test2=test2[len(text_temp[j])+1:]
                                    

                        else:
                    
                            for j in range(i-1,-1,-1):
                                
                                test2=text_temp[j]+' '+test2
                            test2=test2.strip(' ')   
                            
                            for j in range(i+1):
                                '''
                                if test1 in dictory:
                                    mark2=2
                                    
                                    
                                    text_temp[i]=test_ori2   
                                    text_temp.insert(i+1,'ར')
                                    break
                                '''
                                if test2 in dictory:
                                    mark2=2  
                                    
                                    text_temp[i]=test_ori2
                                    text_temp.insert(i+1,'ར')    
                                    break
                                else:
                                    test2=test2[len(text_temp[j])+1:]
                                    
                    
                    elif((text_temp[i][-1] == 'ི' and text_temp[i][-2] == 'འ') or(text_temp[i][-1] == 'ི' and text_temp[i][-2] == 'ཡ') ):
                        test1=text_temp[i][:-2]+'འ'  
                        test2=text_temp[i][:-2]
                        
                        test_ori2=test2
                        if i>config.slide_size:
                            for j in range(i-1,i-config.slide_size,-1):
                                test1=text_temp[j]+' '+test1
                                test2=text_temp[j]+' '+test2
                            test2=test2.strip(' ')   
                            test1=test1.strip(' ')   
                            for j in range(i-config.slide_size+1,i+1):                           
                                if test1 in dictory:
                                    mark2=2
                                    
                                    
                                    text_temp[i]=test_ori2   
                                    text_temp.insert(i+1,'འི')
                                    break
                                if test2 in dictory:
                                    mark2=2  
                                    
                                    text_temp[i]=test_ori2
                                    text_temp.insert(i+1,'འི')    
                                    break
                                else:
                                    test2=test2[len(text_temp[j])+1:]
                                    test1=test1[len(text_temp[j])+1:]
                        else:
                        
                            for j in range(i-1,-1,-1):
                                test1=text_temp[j]+' '+test1
                                test2=text_temp[j]+' '+test2
                            test2=test2.strip(' ')  
                            test1=test1.strip(' ')                          
                            for j in range(i+1):
                                if test1 in dictory:
                                    mark2=2
                                    
                                    
                                    text_temp[i]=test_ori2   
                                    text_temp.insert(i+1,'འི')
                                    break
                                if test2 in dictory:
                                    mark2=2  
                                    
                                    text_temp[i]=test_ori2
                                    text_temp.insert(i+1,'འི')    
                                    break
                                else:
                                    test2=test2[len(text_temp[j])+1:]
                                    test1=test1[len(text_temp[j])+1:]
                                    
                    elif(text_temp[i][-1] == 'ས'  
                        ):
                        if text_temp[i][-2] == 'ི' and ( text_temp[i][-3] =='འ'): 
                            test1=text_temp[i][:-3]+'འ' 
                            test2=text_temp[i][:-3]
                            test_ori2=test2
                            if i>config.slide_size:
                                for j in range(i-1,i-config.slide_size,-1):
                                    test1=text_temp[j]+' '+test1
                                    test2=text_temp[j]+' '+test2
                                test2=test2.strip(' ')  
                                test1=test1.strip(' ')   
                                for j in range(i-config.slide_size+1,i+1):                           
                                    if test1 in dictory:
                                        mark2=2
                                        
                                        
                                        text_temp[i]=test_ori2   
                                        text_temp.insert(i+1,'ས')
                                        break
                                    if test2 in dictory:
                                        mark2=2  
                                        
                                        text_temp[i]=test_ori2
                                        text_temp.insert(i+1,'ས')    
                                        break
                                    else:
                                        test2=test2[len(text_temp[j])+1:]
                                        test1=test1[len(text_temp[j])+1:]
                            else:

                                for j in range(i-1,-1,-1):
                                    test1=text_temp[j]+' '+test1
                                    test2=text_temp[j]+' '+test2
                                test2=test2.strip(' ')  
                                test1=test1.strip(' ')  
                                
                                for j in range(i+1):
                                    if test1 in dictory:
                                        mark2=2
                                        
                                        
                                        text_temp[i]=test_ori2   
                                        text_temp.insert(i+1,'ས')
                                        break
                                    if test2 in dictory:
                                        mark2=2  
                                        
                                        text_temp[i]=test_ori2
                                        text_temp.insert(i+1,'ས')    
                                        break
                                    else:
                                        test1=test1[len(text_temp[j])+1:]
                                        test2=test2[len(text_temp[j])+1:]
                        else:
                            if text_temp[i][-2] == 'ི' and (text_temp[i][-3] == 'ཡ' ):
                                
                                test2=text_temp[i][:-2]
                            else:
                                
                                test2=text_temp[i][:-1]
                            
                            test_ori2=test2
                            if i>config.slide_size:
                                for j in range(i-1,i-config.slide_size,-1):
                                    
                                    test2=text_temp[j]+' '+test2
                                test2=test2.strip(' ')   
                                
                                for j in range(i-config.slide_size+1,i+1):   
                                    '''                        
                                    if test1 in dictory:
                                        mark2=2  
                                        
                                        
                                        text_temp[i]=test_ori2   
                                        text_temp.insert(i+1,'ར')
                                        break
                                    '''
                                    if test2 in dictory:
                                        mark2=2  
                                        
                                        text_temp[i]=test_ori2
                                        text_temp.insert(i+1,'ས')    
                                        break
                                    else:
                                        test2=test2[len(text_temp[j])+1:]
                                        

                            else:
                        
                                for j in range(i-1,-1,-1):
                                    
                                    test2=text_temp[j]+' '+test2
                                test2=test2.strip(' ')   
                                
                                for j in range(i+1):
                                    '''
                                    if test1 in dictory:
                                        mark2=2
                                        
                                        
                                        text_temp[i]=test_ori2   
                                        text_temp.insert(i+1,'ར')
                                        break
                                    '''
                                    if test2 in dictory:
                                        mark2=2  
                                        
                                        text_temp[i]=test_ori2
                                        text_temp.insert(i+1,'ས')    
                                        break
                                    else:
                                        test2=test2[len(text_temp[j])+1:]
                                        
                    elif((text_temp[i][-2] == 'འ' or text_temp[i][-2] == 'ཡ')and (text_temp[i][-1] == 'ང' or text_temp[i][-1] == 'མ') 
                        ):

                        test1=text_temp[i][:-2]+'འ' 
                        test2=text_temp[i][:-2]
                        
                        test_ori2=test2
                        if i>config.slide_size:
                            for j in range(i-1,i-config.slide_size,-1):
                                test1=text_temp[j]+' '+test1
                                test2=text_temp[j]+' '+test2
                            test2=test2.strip(' ')  
                            test1=test1.strip(' ')   
                            for j in range(i-config.slide_size+1,i+1):                           
                                if test1 in dictory:
                                    mark2=2
                                    
                                    
                                    text_temp[i]=test_ori2   
                                    text_temp.insert(i+1,'ས')
                                    break
                                if test2 in dictory:
                                    mark2=2  
                                    
                                    text_temp[i]=test_ori2
                                    text_temp.insert(i+1,'ས')    
                                    break
                                else:
                                    test2=test2[len(text_temp[j])+1:]
                                    test1=test1[len(text_temp[j])+1:]
                        else:

                            for j in range(i-1,-1,-1):
                                test1=text_temp[j]+' '+test1
                                test2=text_temp[j]+' '+test2
                            test2=test2.strip(' ')  
                            test1=test1.strip(' ')  
                            
                            for j in range(i+1):
                                if test1 in dictory:
                                    mark2=2
                                    
                                    
                                    text_temp[i]=test_ori2   
                                    text_temp.insert(i+1,'ས')
                                    break
                                if test2 in dictory:
                                    mark2=2  
                                    
                                    text_temp[i]=test_ori2
                                    text_temp.insert(i+1,'ས')    
                                    break
                                else:
                                    test1=test1[len(text_temp[j])+1:]
                                    test2=test2[len(text_temp[j])+1:]
                        
                    '''
                    elif((text_temp[i][-2] == 'འ' and (text_temp[i][-1]=='ང' or text_temp[i][-1]=='མ') )or 
                        (text_temp[i][-2] == 'ཡ' and text_temp[i][-1]=='ང' ) or 
                        (text_temp[i][-2] == 'འ' and text_temp[i][-1]=='ོ') 
                        ):

                        test1=text_temp[i][:-2]
                        test_ori=test1
                        append=text_temp[i][-2:]
                        if i>config.slide_size:
                            for j in range(i-1,i-config.slide_size,-1):
                                test1=text_temp[j]+' '+test1
                            test1=test1.strip(' ')   
                            for j in range(i-config.slide_size+1,i+1):                           
                                if test1 in dictory:
                                    mark2=2
                                    
                                    text_temp[i]=test_ori
                                    text_temp.insert(i+1,append)
                                    break
                                else:
                                    test1=test1[len(text_temp[j])+1:]
                        else:
                        
                            for j in range(i-1,-1,-1):
                                test1=text_temp[j]+' '+test1
                            test1=test1.strip(' ')  
                            for j in range(i+1):
                                if test1 in dictory:
                                    mark2=2
                                    
                                    text_temp[i]=test_ori
                                    text_temp.insert(i+1,append)
                                    break
                                else:
                                    test1=test1[len(text_temp[j])+1:]                   
                            
                        
                        
                        
                        
                    '''
                    if mark2==0 :
                        mark=tibet_to_digit(text_temp[i])
                        ori=''
                        append=''
                        if mark==0:
                            result=''
                            if text_temp[i][-1] in gen_appendix:
                                if text_temp[i][-1] == 'ོ':
                                    ori,append=text_temp[i][:-2],text_temp[i][-2:]
                                    mark=tibet_to_digit(ori)
                                    result=ori+' '+append
                                    if result is None:
                                        continue
                                    else:
                                        text_temp[i]=ori
                                        text_temp.insert(i+1,append)                                    
                                elif text_temp[i][-1] == 'ི':
                                    ori,append=text_temp[i][:-2],text_temp[i][-2:]
                                    mark=tibet_to_digit(ori)
                                    result=ori+'འ'+' '+append
                                    if result is None:
                                        continue
                                    else:
                                        text_temp[i]=ori
                                        text_temp.insert(i+1,append)        

                            elif text_temp[i][-2] in gen_appendix:
                                ori,append=text_temp[i][:-3],text_temp[i][-3:]
                                mark=tibet_to_digit(ori)
                                result=ori+' '+append
                                if result is None:
                                    continue
                                else:
                                    text_temp[i]=ori
                                    text_temp.insert(i+1,append)        

                            elif text_temp[i][-2] =='འ' and text_temp[i][-1]==('ར'):
                                ori,append=text_temp[i][:-1],text_temp[i][-1]
                                mark=tibet_to_digit(ori)
                                result=ori+' '+append
                                if result is None:
                                    continue
                                else:
                                    text_temp[i]=ori
                                    text_temp.insert(i+1,append)      

                            elif (text_temp[i][-2] ==('འ'or'མ') and text_temp[i][-1]=='ང') or (text_temp[i][-1]=='མ' and text_temp[i][-2] =='འ'):
                                ori,append=text_temp[i][:-2],text_temp[i][-2:]
                                mark=tibet_to_digit(ori)
                                result=ori+' '+append
                                if result is None:
                                    continue
                                else:
                                    text_temp[i]=ori
                                    text_temp.insert(i+1,append)      
                            '''
                            elif len(text_temp[i])>=5:
                                if text_temp[i][-4] =='འ' and (text_temp[i][-2] =='ི'):
                                    ori,append=text_temp[i][:-3],text_temp[i][-3:]
                                    mark=tibet_to_digit(ori)
                                    result=ori+'འ'+' '+append
                                if result is None:
                                    continue
                                else:
                                    text_temp[i]=ori
                                    text_temp.insert(i+1,append)  
                            '''                   
        i=i+1
 
 
 
 
    return text_temp                

                

def j_del_beta2(text_temp,dictory,config,sym_dic):
    divide_mark=1
    for i in range(len(text_temp)):
        if (text_temp[i]=='⊙'):
            divide_mark=0
        elif (text_temp[i]=='ꈍ'):
            divide_mark=1
        if divide_mark==1:
            if len(text_temp[i])>=3 and (utils.Tibet_dect(text_temp[i][0],sym_dic)==True) and text_temp[i][0] not in (sym_dic['S_D']+sym_dic['N']+sym_dic['S_E']+sym_dic['S_F']) :
                mark2=0
                if (text_temp[i][-1] == 'ར' ):  
                    test1=text_temp[i][:-1]+'འ' 
                    test2=text_temp[i][:-1] 
                    
                    test_ori2=test2
                    if i>config.slide_size:
                        for j in range(i-1,i-config.slide_size,-1):
                            test1=text_temp[j]+' '+test1 
                            test2=text_temp[j]+' '+test2
                        test2=test2.strip(' ')   
                        test1=test1.strip(' ')   
                        for j in range(i-config.slide_size+1,i+1):                           
                            if test1 in dictory:
                                mark2=2  
                                
                                
                                text_temp[i]=test_ori2   
                                text_temp.insert(i+1,'ར')
                                break
                            if test2 in dictory:
                                mark2=2  
                                
                                text_temp[i]=test_ori2
                                text_temp.insert(i+1,'ར')    
                                break
                            else:
                                test2=test2[len(text_temp[j])+1:]
                                test1=test1[len(text_temp[j])+1:] 

                    else:
                
                        for j in range(i-1,-1,-1):
                            test1=text_temp[j]+' '+test1
                            test2=text_temp[j]+' '+test2
                        test2=test2.strip(' ')   
                        test1=test1.strip(' ')                          
                        for j in range(i+1):
                            if test1 in dictory:
                                mark2=2
                                
                                
                                text_temp[i]=test_ori2   
                                text_temp.insert(i+1,'ར')
                                break
                            if test2 in dictory:
                                mark2=2  
                                
                                text_temp[i]=test_ori2
                                text_temp.insert(i+1,'ར')    
                                break
                            else:
                                test2=test2[len(text_temp[j])+1:]
                                test1=test1[len(text_temp[j])+1:]
                
                elif(text_temp[i][-1] == 'ི' and text_temp[i][-2] == 'འ'):
                    test1=text_temp[i][:-2]+'འ'  
                    test2=text_temp[i][:-2]
                    
                    test_ori2=test2
                    if i>config.slide_size:
                        for j in range(i-1,i-config.slide_size,-1):
                            test1=text_temp[j]+' '+test1
                            test2=text_temp[j]+' '+test2
                        test2=test2.strip(' ')   
                        test1=test1.strip(' ')   
                        for j in range(i-config.slide_size+1,i+1):                           
                            if test1 in dictory:
                                mark2=2
                                
                                
                                text_temp[i]=test_ori2   
                                text_temp.insert(i+1,'འི')
                                break
                            if test2 in dictory:
                                mark2=2  
                                
                                text_temp[i]=test_ori2
                                text_temp.insert(i+1,'འི')    
                                break
                            else:
                                test2=test2[len(text_temp[j])+1:]
                                test1=test1[len(text_temp[j])+1:]
                    else:
                    
                        for j in range(i-1,-1,-1):
                            test1=text_temp[j]+' '+test1
                            test2=text_temp[j]+' '+test2
                        test2=test2.strip(' ')  
                        test1=test1.strip(' ')                          
                        for j in range(i+1):
                            if test1 in dictory:
                                mark2=2
                                
                                
                                text_temp[i]=test_ori2   
                                text_temp.insert(i+1,'འི')
                                break
                            if test2 in dictory:
                                mark2=2  
                                
                                text_temp[i]=test_ori2
                                text_temp.insert(i+1,'འི')    
                                break
                            else:
                                test2=test2[len(text_temp[j])+1:]
                                test1=test1[len(text_temp[j])+1:]
                                
                elif(text_temp[i][-1] == 'ས'  
                    ):
                    if text_temp[i][-2] == 'ི' and (text_temp[i][-3] == 'ཡ' or text_temp[i][-3] =='འ'): 
                        test1=text_temp[i][:-3]+'འ' 
                        test2=text_temp[i][:-3]
                    else:
                        test1=text_temp[i][:-1]+'འ' 
                        test2=text_temp[i][:-1]
                    
                    test_ori2=test2
                    if i>config.slide_size:
                        for j in range(i-1,i-config.slide_size,-1):
                            test1=text_temp[j]+' '+test1
                            test2=text_temp[j]+' '+test2
                        test2=test2.strip(' ')  
                        test1=test1.strip(' ')   
                        for j in range(i-config.slide_size+1,i+1):                           
                            if test1 in dictory:
                                mark2=2
                                
                                
                                text_temp[i]=test_ori2   
                                text_temp.insert(i+1,'ས')
                                break
                            if test2 in dictory:
                                mark2=2  
                                
                                text_temp[i]=test_ori2
                                text_temp.insert(i+1,'ས')    
                                break
                            else:
                                test2=test2[len(text_temp[j])+1:]
                                test1=test1[len(text_temp[j])+1:]
                    else:

                        for j in range(i-1,-1,-1):
                            test1=text_temp[j]+' '+test1
                            test2=text_temp[j]+' '+test2
                        test2=test2.strip(' ')  
                        test1=test1.strip(' ')  
                        
                        for j in range(i+1):
                            if test1 in dictory:
                                mark2=2
                                
                                
                                text_temp[i]=test_ori2   
                                text_temp.insert(i+1,'ས')
                                break
                            if test2 in dictory:
                                mark2=2  
                                
                                text_temp[i]=test_ori2
                                text_temp.insert(i+1,'ས')    
                                break
                            else:
                                test1=test1[len(text_temp[j])+1:]
                                test2=test2[len(text_temp[j])+1:]
                    
                elif((text_temp[i][-2] == 'འ' and (text_temp[i][-1]=='ང' or text_temp[i][-1]=='མ') )or 
                    (text_temp[i][-2] == 'ཡ' and text_temp[i][-1]=='ང' ) or 
                    (text_temp[i][-2] == 'འ' and text_temp[i][-1]=='ོ') 
                    ):

                    test1=text_temp[i][:-2]
                    test_ori=test1
                    append=text_temp[i][-2:]
                    if i>config.slide_size:
                        for j in range(i-1,i-config.slide_size,-1):
                            test1=text_temp[j]+' '+test1
                        test1=test1.strip(' ')   
                        for j in range(i-config.slide_size+1,i+1):                           
                            if test1 in dictory:
                                mark2=2
                                
                                text_temp[i]=test_ori
                                text_temp.insert(i+1,append)
                                break
                            else:
                                test1=test1[len(text_temp[j])+1:]
                    else:
                    
                        for j in range(i-1,-1,-1):
                            test1=text_temp[j]+' '+test1
                        test1=test1.strip(' ')  
                        for j in range(i+1):
                            if test1 in dictory:
                                mark2=2
                                
                                text_temp[i]=test_ori
                                text_temp.insert(i+1,append)
                                break
                            else:
                                test1=test1[len(text_temp[j])+1:]                   
                        
                    
                    
                    
                    

                if mark2==0 and divide_mark==1:
                    mark=tibet_to_digit(text_temp[i])
                    ori=''
                    append=''
                    if mark==0:
                        result=''
                        if text_temp[i][-1] in gen_appendix:
                            if text_temp[i][-1] == 'ོ':
                                ori,append=text_temp[i][:-2],text_temp[i][-2:]
                                mark=tibet_to_digit(ori)
                                result=ori+' '+append
                                if result is None:
                                    continue
                                else:
                                    text_temp[i]=ori
                                    text_temp.insert(i+1,append)                                    
                            elif text_temp[i][-1] == 'ི':
                                ori,append=text_temp[i][:-2],text_temp[i][-2:]
                                mark=tibet_to_digit(ori)
                                result=ori+'འ'+' '+append
                                if result is None:
                                    continue
                                else:
                                    text_temp[i]=ori
                                    text_temp.insert(i+1,append)        

                        elif text_temp[i][-2] in gen_appendix:
                            ori,append=text_temp[i][:-3],text_temp[i][-3:]
                            mark=tibet_to_digit(ori)
                            result=ori+' '+append
                            if result is None:
                                continue
                            else:
                                text_temp[i]=ori
                                text_temp.insert(i+1,append)        

                        elif text_temp[i][-2] =='འ' and text_temp[i][-1]==('ར'):
                            ori,append=text_temp[i][:-1],text_temp[i][-1]
                            mark=tibet_to_digit(ori)
                            result=ori+' '+append
                            if result is None:
                                continue
                            else:
                                text_temp[i]=ori
                                text_temp.insert(i+1,append)      

                        elif (text_temp[i][-2] ==('འ'or'མ') and text_temp[i][-1]=='ང') or (text_temp[i][-1]=='མ' and text_temp[i][-2] =='འ'):
                            ori,append=text_temp[i][:-2],text_temp[i][-2:]
                            mark=tibet_to_digit(ori)
                            result=ori+' '+append
                            if result is None:
                                continue
                            else:
                                text_temp[i]=ori
                                text_temp.insert(i+1,append)      

                        elif len(text_temp[i])>=5:
                            if text_temp[i][-4] =='འ' and (text_temp[i][-2] =='ི'):
                                ori,append=text_temp[i][:-3],text_temp[i][-3:]
                                mark=tibet_to_digit(ori)
                                result=ori+'འ'+' '+append
                            if result is None:
                                continue
                            else:
                                text_temp[i]=ori
                                text_temp.insert(i+1,append)      


    return text_temp



                                       
def str_combine(text_temp):
    text=''
    for i in text_temp:  
        text=text+' '+i
    text.split()
    return text              

def fina_del(text_temp,dictory,config,sym_dic):
    
    

    text_temp=input_sim_space(text_temp,divide_mark='་')
    text_temp=preserve(text_temp,dictory,config,sym_dic)  
    
    output_temp_str = ''
    output_list = []
    for i in range(len(text_temp)):
        if text_temp[i] != '⊙' and text_temp[i] != 'ꈍ':
            output_list.append(text_temp[i])
    for i in range(len(output_list)):
        if i:
            output_temp_str += '་'
        output_temp_str += output_list[i]

    return output_temp_str







def preserve_old(text_temp,dictory,config):
    i=0
    while(i<len(text_temp)):
        mark2=0
        if len(text_temp[i])>=3:
            if ((text_temp[i][-1] == 'ི' and text_temp[i][-2] == 'འ') or  
                (text_temp[i][-1] == 'ས' or (text_temp[i][-1] == 'ས' and text_temp[i][-2] == 'ི' and ((text_temp[i][-3] == 'ཡ' or text_temp[i][-3] =='འ') ) )) or 
                (text_temp[i][-1] == 'ར' ) or 
                (text_temp[i][-1] == 'ང' and (text_temp[i][-2] == 'ཡ' or text_temp[i][-2] == 'འ')) or 
                (text_temp[i][-1] == 'མ' and text_temp[i][-2] == 'འ') or 
                (text_temp[i][-1] == 'ོ' and text_temp[i][-2] == 'འ') 
                ):
                
                if i>=config.slide_size and (len(text_temp)-i)>config.slide_size: 
                    
                    test=''
                    front=''
                    rear=''
                    for j in range(i-1,i-config.slide_size-1,-1):
                        front=text_temp[j]+' '+front  

                    for j in range(i+config.slide_size,i,-1):
                        rear=text_temp[j]+' '+rear

                        
                    del_sign=0   
                    for j in range(i-config.slide_size,i+1):
                        test=front+text_temp[i]+' '+rear       
                        test=test.strip(' ')
                        record=len(test)

                        if test in dictory and del_sign==0:
                            
                            text_temp.insert(j,'⊙')
                            text_temp.insert(record+1,'ꈍ')
                            
                            mark2=1
                            
                            i+=1
                            break
                        else:
                            del_sign=1
                                                       
                        
                        for k in range(i+config.slide_size,i-1,-1):
                            if test in dictory:
                                    mark2=1      
                                    
                                    
                                    text_temp.insert(j,'⊙')
                                    text_temp.insert(k+2,'ꈍ')
                                    
                                    del_sign=1
                                    i+=1
                                    break
                               
                            else:
                                test=test[:(len(test)-len(text_temp[k])-1)]

                        
                        if test in dictory and del_sign==0:
                            
                            text_temp.insert(j,'⊙')
                            text_temp.insert(k+1,'ꈍ')
                            
                            mark2=1
                            i+=1
                            
                        if mark2==1:
                            
                            break
                        else:
                            
                            front=front[len(text_temp[j])+1:]                         

                elif i>=config.slide_size and (len(text_temp)-i)<config.slide_size:  
                    test=''
                    front=''
                    rear=''
                    for j in range(i-1,i-config.slide_size-1,-1):
                        front=text_temp[j]+' '+front  

                    for j in range(len(text_temp)-1,i,-1):
                        rear=text_temp[j]+' '+rear
                        
                    del_sign=0   
                    for j in range(i-config.slide_size,i+1):
                        test=front+text_temp[i]+' '+rear       
                        test=test.strip(' ')
                        record=len(test)
                        
                        if test in dictory and del_sign==0:
                            
                            text_temp.insert(j,'⊙')
                            text_temp.insert(record+1,'ꈍ')
                            
                            mark2=1
                            
                            i+=1
                            break
                        else:
                            del_sign=1
                                                       
                        
                        for k in range(len(text_temp)-1,i-1,-1):
                            if test in dictory:
                                    mark2=1      
                                    
                                    
                                    text_temp.insert(j,'⊙')
                                    text_temp.insert(k+2,'ꈍ')
                                    
                                    del_sign=1
                                    i+=1
                                    break
                               
                            else:
                                test=test[:(len(test)-len(text_temp[k])-1)]

                        
                        if test in dictory and del_sign==0:
                            
                            text_temp.insert(j,'⊙')
                            text_temp.insert(k+1,'ꈍ')
                            
                            mark2=1
                            i+=1
                        
                        if mark2==1:
                            break
                        else:
                            
                            front=front[len(text_temp[j])+1:]   
                elif i<config.slide_size and (len(text_temp)-i)>config.slide_size: 
                    
                        test=''
                        front=''
                        rear=''

                        for j in range(i-1,-1,-1):
                            front=text_temp[j]+' '+front  

                        for j in range(i+config.slide_size,i,-1):
                            rear=text_temp[j]+' '+rear
                        del_sign=0   
                        for j in range(0,i+1):
                            test=front+text_temp[i]+' '+rear       
                            test=test.strip(' ')
                            record=len(test)
                            
                            if test in dictory and del_sign==0:
                                
                                text_temp.insert(j,'⊙')
                                text_temp.insert(record+1,'ꈍ')
                                
                                mark2=1
                                
                                i+=1
                                break
                            else:
                                del_sign=1
                                                        
                            
                            for k in range(i+config.slide_size,i-1,-1):
                                if test in dictory:
                                        mark2=1      
                                        
                                        
                                        text_temp.insert(j,'⊙')
                                        text_temp.insert(k+2,'ꈍ')
                                        
                                        del_sign=1
                                        i+=1
                                        break
                                
                                else:
                                    test=test[:(len(test)-len(text_temp[k])-1)]

                            
                            if test in dictory and del_sign==0:
                                
                                text_temp.insert(j,'⊙')
                                text_temp.insert(k+1,'ꈍ')
                                
                                mark2=1
                                i+=1
                                
                            
                            if mark2==1:
                                
                                break
                            else:
                                
                                front=front[len(text_temp[j])+1:]     

                else:
                        test=''
                        front=''
                        rear=''

                        for j in range(i-1,-1,-1):
                            front=text_temp[j]+' '+front  

                        for j in range(len(text_temp)-1,i,-1):
                            rear=text_temp[j]+' '+rear
                           
                        del_sign=0   
                        for j in range(0,i+1):
                            test=front+text_temp[i]+' '+rear       
                            test=test.strip(' ')
                            record=len(test)
                            
                            if test in dictory and del_sign==0:
                                
                                text_temp.insert(j,'⊙')
                                text_temp.insert(record+1,'ꈍ')
                                
                                mark2=1
                                
                                i+=1
                                break
                            else:
                                del_sign=1
                                                        
                            
                            for k in range(len(text_temp)-1,i-1,-1):
                                if test in dictory:
                                        mark2=1      
                                        
                                        
                                        text_temp.insert(j,'⊙')
                                        text_temp.insert(k+2,'ꈍ')
                                        
                                        del_sign=1
                                        i+=1
                                        break
                                
                                else:
                                    test=test[:(len(test)-len(text_temp[k])-1)]

                            
                            if test in dictory and del_sign==0:
                                
                                text_temp.insert(j,'⊙')
                                text_temp.insert(k+1,'ꈍ')
                                
                                mark2=1
                                i+=1
                                
                            
                            if mark2==1:
                                
                                break
                            else:
                                
                                front=front[len(text_temp[j])+1:]   

        i=i+1
 
 
 
    return text_temp                
   

                



def j_del_beta2_old(text_temp,dictory,config,sym_dic):
    divide_mark=1
    for i in range(len(text_temp)):
        if (text_temp[i]=='⊙'):
            divide_mark=0
        elif (text_temp[i]=='ꈍ'):
            divide_mark=1
        if len(text_temp[i])>=3 and (utils.Tibet_dect(text_temp[i][0],sym_dic)==True) and text_temp[i][0] not in (sym_dic['S_D']+sym_dic['N']+sym_dic['S_E']+sym_dic['S_F']) :
            mark2=0
            if divide_mark==1:
                if (text_temp[i][-1] == 'ར' ):  
                    test1=text_temp[i][:-1]+'འ' 
                    test2=text_temp[i][:-1] 
                    
                    test_ori2=test2
                    if i>config.slide_size:
                        for j in range(i-1,i-config.slide_size,-1):
                            test1=text_temp[j]+' '+test1 
                            test2=text_temp[j]+' '+test2
                        test2=test2.strip(' ')   
                        test1=test1.strip(' ')   
                        for j in range(i-config.slide_size+1,i+1):                           
                            if test1 in dictory:
                                mark2=2  
                                
                                
                                text_temp[i]=test_ori2   
                                text_temp.insert(i+1,'ར')
                                break
                            if test2 in dictory:
                                mark2=2  
                                
                                text_temp[i]=test_ori2
                                text_temp.insert(i+1,'ར')    
                                break
                            else:
                                test2=test2[len(text_temp[j])+1:]
                                test1=test1[len(text_temp[j])+1:] 

                    else:
                
                        for j in range(i-1,-1,-1):
                            test1=text_temp[j]+' '+test1
                            test2=text_temp[j]+' '+test2
                        test2=test2.strip(' ')   
                        test1=test1.strip(' ')                          
                        for j in range(i+1):
                            if test1 in dictory:
                                mark2=2
                                
                                
                                text_temp[i]=test_ori2   
                                text_temp.insert(i+1,'ར')
                                break
                            if test2 in dictory:
                                mark2=2  
                                
                                text_temp[i]=test_ori2
                                text_temp.insert(i+1,'ར')    
                                break
                            else:
                                test2=test2[len(text_temp[j])+1:]
                                test1=test1[len(text_temp[j])+1:]
                
                elif(text_temp[i][-1] == 'ི' and text_temp[i][-2] == 'འ'):
                    test1=text_temp[i][:-2]+'འ'  
                    test2=text_temp[i][:-2]
                    
                    test_ori2=test2
                    if i>config.slide_size:
                        for j in range(i-1,i-config.slide_size,-1):
                            test1=text_temp[j]+' '+test1
                            test2=text_temp[j]+' '+test2
                        test2=test2.strip(' ')   
                        test1=test1.strip(' ')   
                        for j in range(i-config.slide_size+1,i+1):                           
                            if test1 in dictory:
                                mark2=2
                                
                                
                                text_temp[i]=test_ori2   
                                text_temp.insert(i+1,'འི')
                                break
                            if test2 in dictory:
                                mark2=2  
                                
                                text_temp[i]=test_ori2
                                text_temp.insert(i+1,'འི')    
                                break
                            else:
                                test2=test2[len(text_temp[j])+1:]
                                test1=test1[len(text_temp[j])+1:]
                    else:
                    
                        for j in range(i-1,-1,-1):
                            test1=text_temp[j]+' '+test1
                            test2=text_temp[j]+' '+test2
                        test2=test2.strip(' ')  
                        test1=test1.strip(' ')                          
                        for j in range(i+1):
                            if test1 in dictory:
                                mark2=2
                                
                                
                                text_temp[i]=test_ori2   
                                text_temp.insert(i+1,'འི')
                                break
                            if test2 in dictory:
                                mark2=2  
                                
                                text_temp[i]=test_ori2
                                text_temp.insert(i+1,'འི')    
                                break
                            else:
                                test2=test2[len(text_temp[j])+1:]
                                test1=test1[len(text_temp[j])+1:]
                                
                elif(text_temp[i][-1] == 'ས'  
                     ):
                    if text_temp[i][-2] == 'ི' and (text_temp[i][-3] == 'ཡ' or text_temp[i][-3] =='འ'): 
                        test1=text_temp[i][:-3]+'འ' 
                        test2=text_temp[i][:-3]
                    else:
                        test1=text_temp[i][:-1]+'འ' 
                        test2=text_temp[i][:-1]
                    
                    test_ori2=test2
                    if i>config.slide_size:
                        for j in range(i-1,i-config.slide_size,-1):
                            test1=text_temp[j]+' '+test1
                            test2=text_temp[j]+' '+test2
                        test2=test2.strip(' ')  
                        test1=test1.strip(' ')   
                        for j in range(i-config.slide_size+1,i+1):                           
                            if test1 in dictory:
                                mark2=2
                                
                                
                                text_temp[i]=test_ori2   
                                text_temp.insert(i+1,'ས')
                                break
                            if test2 in dictory:
                                mark2=2  
                                
                                text_temp[i]=test_ori2
                                text_temp.insert(i+1,'ས')    
                                break
                            else:
                                test2=test2[len(text_temp[j])+1:]
                                test1=test1[len(text_temp[j])+1:]
                    else:

                        for j in range(i-1,-1,-1):
                            test1=text_temp[j]+' '+test1
                            test2=text_temp[j]+' '+test2
                        test2=test2.strip(' ')  
                        test1=test1.strip(' ')  
                        
                        for j in range(i+1):
                            if test1 in dictory:
                                mark2=2
                                
                                
                                text_temp[i]=test_ori2   
                                text_temp.insert(i+1,'ས')
                                break
                            if test2 in dictory:
                                mark2=2  
                                
                                text_temp[i]=test_ori2
                                text_temp.insert(i+1,'ས')    
                                break
                            else:
                                test1=test1[len(text_temp[j])+1:]
                                test2=test2[len(text_temp[j])+1:]
                    
                elif((text_temp[i][-2] == 'འ' and (text_temp[i][-1]=='ང' or text_temp[i][-1]=='མ') )or 
                     (text_temp[i][-2] == 'ཡ' and text_temp[i][-1]=='ང' ) or 
                     (text_temp[i][-2] == 'འ' and text_temp[i][-1]=='ོ') 
                     ):

                    test1=text_temp[i][:-2]
                    test_ori=test1
                    append=text_temp[i][-2:]
                    if i>config.slide_size:
                        for j in range(i-1,i-config.slide_size,-1):
                            test1=text_temp[j]+' '+test1
                        test1=test1.strip(' ')   
                        for j in range(i-config.slide_size+1,i+1):                           
                            if test1 in dictory:
                                mark2=2
                                
                                text_temp[i]=test_ori
                                text_temp.insert(i+1,append)
                                break
                            else:
                                test1=test1[len(text_temp[j])+1:]
                    else:
                    
                        for j in range(i-1,-1,-1):
                            test1=text_temp[j]+' '+test1
                        test1=test1.strip(' ')  
                        for j in range(i+1):
                            if test1 in dictory:
                                mark2=2
                                
                                text_temp[i]=test_ori
                                text_temp.insert(i+1,append)
                                break
                            else:
                                test1=test1[len(text_temp[j])+1:]                   
                        
                    
                    
                    
                    

                if mark2==0 and divide_mark==1:
                    mark=tibet_to_digit(text_temp[i])
                    ori=''
                    append=''
                    if mark==0:
                        result=''
                        if text_temp[i][-1] in gen_appendix:
                            if text_temp[i][-1] == 'ོ':
                                ori,append=text_temp[i][:-2],text_temp[i][-2:]
                                mark=tibet_to_digit(ori)
                                result=ori+' '+append
                                if result is None:
                                    continue
                                else:
                                    text_temp[i]=ori
                                    text_temp.insert(i+1,append)                                    
                            elif text_temp[i][-1] == 'ི':
                                ori,append=text_temp[i][:-2],text_temp[i][-2:]
                                mark=tibet_to_digit(ori)
                                result=ori+'འ'+' '+append
                                if result is None:
                                    continue
                                else:
                                    text_temp[i]=ori
                                    text_temp.insert(i+1,append)        

                        elif text_temp[i][-2] in gen_appendix:
                            ori,append=text_temp[i][:-3],text_temp[i][-3:]
                            mark=tibet_to_digit(ori)
                            result=ori+' '+append
                            if result is None:
                                continue
                            else:
                                text_temp[i]=ori
                                text_temp.insert(i+1,append)        

                        elif text_temp[i][-2] =='འ' and text_temp[i][-1]==('ར'):
                            ori,append=text_temp[i][:-1],text_temp[i][-1]
                            mark=tibet_to_digit(ori)
                            result=ori+' '+append
                            if result is None:
                                continue
                            else:
                                text_temp[i]=ori
                                text_temp.insert(i+1,append)      

                        elif (text_temp[i][-2] ==('འ'or'མ') and text_temp[i][-1]=='ང') or (text_temp[i][-1]=='མ' and text_temp[i][-2] =='འ'):
                            ori,append=text_temp[i][:-2],text_temp[i][-2:]
                            mark=tibet_to_digit(ori)
                            result=ori+' '+append
                            if result is None:
                                continue
                            else:
                                text_temp[i]=ori
                                text_temp.insert(i+1,append)      

                        elif len(text_temp[i])>=5:
                            if text_temp[i][-4] =='འ' and (text_temp[i][-2] =='ི'):
                                ori,append=text_temp[i][:-3],text_temp[i][-3:]
                                mark=tibet_to_digit(ori)
                                result=ori+'འ'+' '+append
                            if result is None:
                                continue
                            else:
                                text_temp[i]=ori
                                text_temp.insert(i+1,append)      


    return text_temp
