from pickle import TRUE
import tqdm
import utils

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
            if str_temp[0] >= chr(0x0F40) and str_temp[0] <= chr(0x0F6C):#对于基字再判断
            # 第二个字符是元音（ ི、 ུ、 ེ、 ོ）
            # 基字+元音
                structure["root"] = str_temp[0]
                structure["vowel"] = str_temp[1]
                mark=1
        elif str_temp[1] >= chr(0x0F40) and str_temp[1] <= chr(0x0F6C):
            # 第二个字符是前导字符
            # 基字+后加字
            if str_temp[0] >= chr(0x0F40) and str_temp[0] <= chr(0x0F6C):#对于基字再判断
                structure["root"] = str_temp[0]
                structure["suffix"] = str_temp[1]
                mark=1
        elif str_temp[1] in overlying_base:
            # 第二个字符是叠加字符
            if str_temp[1] in subscribed_appendix:
                # 第二个字符是下加字（ ྱ、 ྲ、 ླ、 ྭ）
                # 基字+下加字
                structure["root"] = str_temp[0]
                structure["subscribed"] = str_temp[1]
                mark=1
            else:
                # 上加字+基字
                if str_temp[0] in super_appendix:
                        structure["superscribed"] = str_temp[0]
                        structure["root"] = str_temp[1]
                        mark=1                
    elif len(str_temp) == 3:
        if str_temp[2] in gen_appendix:
            # 第三个字符是元音（ ི、 ུ、 ེ、 ོ）
            if str_temp[1] >= chr(0x0F40) and str_temp[1] <= chr(0x0F6C):
                if str_temp[0] in front_appendix:
                # 第二个字符是前导字符
                # 前加字+基字+元音
                    structure["prefix"] = str_temp[0]
                    structure["root"] = str_temp[1]
                    structure["vowel"] = str_temp[2]
                    mark=1
            elif str_temp[1] in overlying_base and str_temp[1] in subscribed_appendix:
                # 第二个字符是下加字（ ྱ、 ྲ、 ླ、 ྺ）
                # 基字+下加字+元音
                    structure["root"] = str_temp[0]
                    structure["subscribed"] = str_temp[1]
                    structure["vowel"] = str_temp[2]
                    mark=1
            elif str_temp[0] in super_appendix and str_temp[1] in overlying_base :
                # 上加字+基字+元音
                structure["superscribed"] = str_temp[0]
                structure["root"] = str_temp[1]
                structure["vowel"] = str_temp[2]
                mark=1
        elif str_temp[1] in gen_appendix:
            # 第二个字符是元音（ ི、 ུ、 ེ、 ོ）
            # 基字+元音+后加字
            structure["root"] = str_temp[0]
            structure["vowel"] = str_temp[1]
            structure["suffix"] = str_temp[2]
            mark=1
        else:
            if (str_temp[1] >= chr(0x0F40) and str_temp[1] <= chr(0x0F6C)
                ) and (str_temp[2] >= chr(0x0F40)
                       and str_temp[2] <= chr(0x0F6C)):
                # 第二个字符是前导字符，第三个字符是前导字符
                if (str_temp[2] == chr(0x0F51) and
                    (str_temp[1] == chr(0x0F53) or str_temp[1] == chr(0x0F62)
                     or str_temp[1] == chr(0x0F63))) or (
                         str_temp[2] == chr(0x0F66) and
                         (str_temp[1] == chr(0x0F42) or str_temp[1]
                          == chr(0x0F44) or str_temp[1] == chr(0x0F56)
                          or str_temp[1] == chr(0x0F58))):
                    # 最后两个字符为后加字+再后加字（ན、ར、ལ）+（ད）或（ག、ང、བ、མ）+（ས）
                    # 基字+后加字+再后加字
                    structure["root"] = str_temp[0]
                    structure["suffix"] = str_temp[1]
                    structure["suffix_2nd"] = str_temp[2]
                    mark=1
                elif str_temp[0] in front_appendix:
                    # 前加字+基字+后加字
                    structure["prefix"] = str_temp[0]
                    structure["root"] = str_temp[1]
                    structure["suffix"] = str_temp[2]
                    mark=1
            elif (str_temp[1] >= chr(0x0F40) and str_temp[1] <= chr(0x0F6C)
                  ) and str_temp[2] in overlying_base :
                # 第二个字符是前导字符，第三个字符是叠加字符
                if str_temp[2] in subscribed_appendix and str_temp[0] in front_appendix:
                    # 第三个字符是下加字（ ྱ、 ྲ、 ླ、 ྭ）
                    # 前加字+基字+下加字
                    structure["prefix"] = str_temp[0]
                    structure["root"] = str_temp[1]
                    structure["subscribed"] = str_temp[2]
                    mark=1
                else:
                    # 前加字+上加字+基字
                    if str_temp[0] in front_appendix and str_temp[1] in super_appendix:
                        structure["prefix"] = str_temp[0]
                        structure["superscribed"] = str_temp[1]
                        structure["root"] = str_temp[2]
                        mark=1
            elif str_temp[1] in overlying_base and str_temp[2] in overlying_base:
                # 第二个字符是叠加字符，第三个字符是叠加字符
                if str_temp[1] in subscribed_appendix and str_temp[2] in subscribed_appendix_2nd:
                    # 第二个字符是下加字（ ྱ、 ྲ、 ླ、 ྭ）
                    # 基字+下加字+再下加字
                    structure["root"] = str_temp[0]
                    structure["subscribed"] = str_temp[1]
                    structure["subscribed_2nd"] = str_temp[2]
                    mark=1
                elif str_temp[0] in super_appendix:
                    # 上加字+基字+下加字
                    structure["superscribed"] = str_temp[0]
                    structure["root"] = str_temp[1]
                    structure["subscribed"] = str_temp[2]
                    mark=1
            elif (str_temp[1] in overlying_base
                  ) and (str_temp[2] >= chr(0x0F40)
                         and str_temp[2] <= chr(0x0F6C)):
                # 第二个字符是叠加字符，第三个字符是前导字符
                if str_temp[1] in subscribed_appendix:
                    # 第二个字符是下加字（ ྱ、 ྲ、 ླ、 ྭ）
                    # 基字+下加字+后加字
                    structure["root"] = str_temp[0]
                    structure["subscribed"] = str_temp[1]
                    structure["suffix"] = str_temp[2]
                    mark=1
                elif str_temp[0] in super_appendix:
                    # 上加字+基字+后加字
                    structure["superscribed"] = str_temp[0]
                    structure["root"] = str_temp[1]
                    structure["suffix"] = str_temp[2]
                    mark=1
    elif len(str_temp) == 4:
        if str_temp[3] in gen_appendix:
            # 第四个字符是元音（ ི、 ུ、 ེ、 ོ）
            if str_temp[1] >= chr(0x0F40) and str_temp[1] <= chr(0x0F6C):
                # 第二个字符是前导字符
                if str_temp[2] in subscribed_appendix:
                    # 第三个字符是下加字（ ྱ、 ྲ、 ླ、 ྭ）
                    # 前加字+基字+下加字+元音
                    structure["prefix"] = str_temp[0]
                    structure["root"] = str_temp[1]
                    structure["subscribed"] = str_temp[2]
                    structure["vowel"] = str_temp[3]
                    mark=1
                elif str_temp[0] in front_appendix and str_temp[2] in overlying_base and str_temp[1] in super_appendix:
                    # 前加字+上加字+基字+元音
                    structure["prefix"] = str_temp[0]
                    structure["superscribed"] = str_temp[1]
                    structure["root"] = str_temp[2]
                    structure["vowel"] = str_temp[3]
                    mark=1
            else:
                if (str_temp[1] not in subscribed_appendix) and (str_temp[2] in subscribed_appendix) and(str_temp[1] in overlying_base):
                    # 第二个字符不是下加字（ ྱ、 ྲ、 ླ、 ྭ）并且第三个字符是下加字（ ྱ、 ྲ、 ླ、 ྭ）
                    # 上加字+基字+下加字+元音
                    structure["superscribed"] = str_temp[0]
                    structure["root"] = str_temp[1]
                    structure["subscribed"] = str_temp[2]
                    structure["vowel"] = str_temp[3]
                    mark=1
                elif (str_temp[1] in subscribed_appendix) and (str_temp[2] in subscribed_appendix_2nd):
                    # 第二个字符是下加字（ ྱ、 ྲ、 ླ、 ྭ）并且第三个字符是再下加字（ ྱ、 ྲ、 ླ、 ྭ）
                    # 基字+下加字+再下加字+元音
                    structure["root"] = str_temp[0]
                    structure["subscribed"] = str_temp[1]
                    structure["subscribed_2nd"] = str_temp[2]
                    structure["vowel"] = str_temp[3]
                    mark=1
        elif str_temp[2] in gen_appendix:
            # 第三个字符是元音（ ི、 ུ、 ེ、 ོ）
            if str_temp[1] >= chr(0x0F40) and str_temp[1] <= chr(0x0F6C):
                if str_temp[0] in front_appendix :
                # 第二个字符是前导字符
                # 前加字+基字+元音+后加字
                    structure["prefix"] = str_temp[0]
                    structure["root"] = str_temp[1]
                    structure["vowel"] = str_temp[2]
                    structure["suffix"] = str_temp[3]
                    mark=1
            else:
                if str_temp[1] in subscribed_appendix :
                    # 第二个字符是下加字（ ྱ、 ྲ、 ླ、 ྭ）
                    # 基字+下加字+元音+后加字
                    structure["root"] = str_temp[0]
                    structure["subscribed"] = str_temp[1]
                    structure["vowel"] = str_temp[2]
                    structure["suffix"] = str_temp[3]
                    mark=1
                elif str_temp[0] in super_appendix and str_temp[1] in overlying_base:
                    # 上加字+基字+元音+后加字
                    structure["superscribed"] = str_temp[0]
                    structure["root"] = str_temp[1]
                    structure["vowel"] = str_temp[2]
                    structure["suffix"] = str_temp[3]
                    mark=1
        elif str_temp[1] in gen_appendix:
            # 第二个字符是元音（ ི、 ུ、 ེ、 ོ）
            # 基字+元音+后加字+再后加字
            if str_temp[3] in suffix_2nd:
                structure["root"] = str_temp[0]
                structure["vowel"] = str_temp[1]
                structure["suffix"] = str_temp[2]
                structure["suffix_2nd"] = str_temp[3]
                mark=1
        else:
            if str_temp[3] >= chr(0x0F40) and str_temp[3] <= chr(0x0F6C):
                # 第四个字符是前导字符
                if (str_temp[1] >= chr(0x0F40) and str_temp[1] <= chr(0x0F6C)
                    ) and (str_temp[2] >= chr(0x0F40)
                           and str_temp[2] <= chr(0x0F6C)):
                    # 第二个字符是前导字符并且第三个字符是前导字符
                    # 前加字+基字+后加字+再后加字
                    if str_temp[3] in suffix_2nd:
                        structure["prefix"] = str_temp[0]
                        structure["root"] = str_temp[1]
                        structure["suffix"] = str_temp[2]
                        structure["suffix_2nd"] = str_temp[3]
                        mark=1
                elif (str_temp[1] >= chr(0x0F40) and str_temp[1] <= chr(0x0F6C)
                      ) and (str_temp[2] in overlying_base):
                    # 第二个字符是前导字符并且第三个字符是叠加字符
                    if str_temp[2] in subscribed_appendix:
                        # 第三个字符是下加字（ ྱ、 ྲ、 ླ、 ྭ）
                        # 前加字+基字+下加字+后加字
                        structure["prefix"] = str_temp[0]
                        structure["root"] = str_temp[1]
                        structure["subscribed"] = str_temp[2]
                        structure["suffix"] = str_temp[3]
                        mark=1
                    elif str_temp[0] in front_appendix and str_temp[1] in super_appendix:
                        # 前加字+上加字+基字+后加字
                        structure["prefix"] = str_temp[0]
                        structure["superscribed"] = str_temp[1]
                        structure["root"] = str_temp[2]
                        structure["suffix"] = str_temp[3]
                        mark=1
                elif (str_temp[1] in overlying_base) and (str_temp[2] >= chr(0x0F40)
                             and str_temp[2] <= chr(0x0F6C)):
                    # 第二个字符是叠加字符并且第三个字符是前导字符
                    if str_temp[1] in subscribed_appendix:
                        # 第二个字符是下加字（ ྱ、 ྲ、 ླ、 ྭ）
                        # 基字+下加字+后加字+再后加字
                        if str_temp[3] in suffix_2nd:
                            structure["root"] = str_temp[0]
                            structure["subscribed"] = str_temp[1]
                            structure["suffix"] = str_temp[2]
                            structure["suffix_2nd"] = str_temp[3]
                            mark=1
                    elif str_temp[0] in super_appendix and str_temp[3] in suffix_2nd:
                        # 上加字+基字+后加字+再后加字
                        structure["superscribed"] = str_temp[0]
                        structure["root"] = str_temp[1]
                        structure["suffix"] = str_temp[2]
                        structure["suffix_2nd"] = str_temp[3]
                        mark=1
                elif (str_temp[1] in overlying_base
                      ) and (str_temp[2] in overlying_base):
                    # 第二个字符是叠加字符并且第三个字符是叠加字符
                    if str_temp[1] in subscribed_appendix and str_temp[2] in subscribed_appendix_2nd:
                        # 第二个字符是下加字（ ྱ、 ྲ、 ླ、 ྭ）
                        # 基字+下加字+下加字+后加字
                        structure["root"] = str_temp[0]
                        structure["subscribed"] = str_temp[1]
                        structure["subscribed_2nd"] = str_temp[2]
                        structure["suffix"] = str_temp[3]
                        mark=1
                    elif str_temp[0] in super_appendix and str_temp[2] in subscribed_appendix:
                        # 上加字+基字+下加字+后加字
                        structure["superscribed"] = str_temp[0]
                        structure["root"] = str_temp[1]
                        structure["subscribed"] = str_temp[2]
                        structure["suffix"] = str_temp[3]
                        mark=1
            elif str_temp[0] in front_appendix and str_temp[1] in super_appendix and str_temp[2] in overlying_base and str_temp[3] in subscribed_appendix:
                # 前加字+上加字+基字+下加字
                structure["prefix"] = str_temp[0]
                structure["superscribed"] = str_temp[1]
                structure["root"] = str_temp[2]
                structure["subscribed"] = str_temp[3]
                mark=1
    elif len(str_temp) == 5:
        if str_temp[4] in gen_appendix:
            # 第五个字符是元音（ ི、 ུ、 ེ、 ོ）
            # 前加字+上加字+基字+下加字+元音
            if str_temp[0] in front_appendix and str_temp[1] in super_appendix and str_temp[2] in overlying_base and str_temp[3] in subscribed_appendix:
                structure["prefix"] = str_temp[0]
                structure["superscribed"] = str_temp[1]
                structure["root"] = str_temp[2]
                structure["subscribed"] = str_temp[3]
                structure["vowel"] = str_temp[4]
                mark=1
        elif str_temp[3] in gen_appendix:
            # 第四个字符是元音（ ི、 ུ、 ེ、 ོ）
            if str_temp[1] in subscribed_appendix and str_temp[2] in subscribed_appendix_2nd:
                # 第二个字符是叠加字符并且第二个字符是下加字（ ྱ、 ྲ、 ླ、 ྭ）
                # 基字+下加字+下加字+元音+后加字
                structure["root"] = str_temp[0]
                structure["subscribed"] = str_temp[1]
                structure["subscribed_2nd"] = str_temp[2]
                structure["vowel"] = str_temp[3]
                structure["suffix"] = str_temp[4]
                mark=1
            elif (str_temp[1] in overlying_base) and (str_temp[1] not in subscribed_appendix) :
                # 第二个字符是叠加字符并且第二个字符不是下加字（ ྱ、 ྲ、 ླ、 ྭ）
                # 上加字+基字+下加字+元音+后加字
                if str_temp[2] in subscribed_appendix and str_temp[0] in super_appendix:
                    structure["superscribed"] = str_temp[0]
                    structure["root"] = str_temp[1]
                    structure["subscribed"] = str_temp[2]
                    structure["vowel"] = str_temp[3]
                    structure["suffix"] = str_temp[4]
                    mark=1
            elif str_temp[1] >= chr(0x0F40) and str_temp[1] <= chr(0x0F6C):
                # 第二个字符是前导字符
                if str_temp[2] in subscribed_appendix:
                    # 第三个字符是下加字（ ྱ、 ྲ、 ླ、 ྭ）
                    # 前加字+基字+下加字+元音+后加字
                    if str_temp[3] in gen_appendix:
                        structure["prefix"] = str_temp[0]
                        structure["root"] = str_temp[1]
                        structure["subscribed"] = str_temp[2]
                        structure["vowel"] = str_temp[3]
                        structure["suffix"] = str_temp[4]
                        mark=1
                elif str_temp[0] in front_appendix and str_temp[2] in overlying_base and str_temp[3] in gen_appendix:
                    if str_temp[1] in super_appendix:
                    # 前加字+上加字+基字+元音+后加字
                        structure["prefix"] = str_temp[0]
                        structure["superscribed"] = str_temp[1]
                        structure["root"] = str_temp[2]
                        structure["vowel"] = str_temp[3]
                        structure["suffix"] = str_temp[4]
                        mark=1
        elif str_temp[2] in gen_appendix:
            # 第三个字符是元音（ ི、 ུ、 ེ、 ོ）
            if str_temp[1] >= chr(0x0F40) and str_temp[1] <= chr(0x0F6C):
                # 第二个字符是前导字符
                # 前加字+基字+元音+后加字+再后加字
                if str_temp[0] in front_appendix and str_temp[4] in suffix_2nd:
                    structure["prefix"] = str_temp[0]
                    structure["root"] = str_temp[1]
                    structure["vowel"] = str_temp[2]
                    structure["suffix"] = str_temp[3]
                    structure["suffix_2nd"] = str_temp[4]
                    mark=1
            else:
                if str_temp[1] in subscribed_appendix:
                    # 第二个字符是下加字（ ྱ、 ྲ、 ླ、 ྭ）
                    # 基字+下加字+元音+后加字+再后加字
                    if str_temp[4] in subscribed_appendix_2nd:
                        structure["root"] = str_temp[0]
                        structure["subscribed"] = str_temp[1]
                        structure["vowel"] = str_temp[2]
                        structure["suffix"] = str_temp[3]
                        structure["suffix_2nd"] = str_temp[4]
                        mark=1
                elif str_temp[0] in super_appendix and str_temp[1] in overlying_base:
                    if str_temp[4] in suffix_2nd:
                    # 上加字+基字+元音+后加字+再后加字
                        structure["superscribed"] = str_temp[0]
                        structure["root"] = str_temp[1]
                        structure["vowel"] = str_temp[2]
                        structure["suffix"] = str_temp[3]
                        structure["suffix_2nd"] = str_temp[4]
                        mark=1
        else:
            if (str_temp[0] >= chr(0x0F40) and str_temp[0] <= chr(0x0F6C)
                ) and (str_temp[1] in overlying_base) and (str_temp[2] in overlying_base):
                # 第一个字符是前导字符并且第二个字符是叠加字符并且第三个字符是叠加字符
                if str_temp[1] in subscribed_appendix and str_temp[2] in subscribed_appendix_2nd and str_temp[4] in suffix_2nd:
                    # 第二个字符是下加字
                    # 基字+下加字+再下加字+后加字+再后加字
                    structure["root"] = str_temp[0]
                    structure["subscribed"] = str_temp[1]
                    structure["subscribed_2nd"] = str_temp[2]
                    structure["suffix"] = str_temp[3]
                    structure["suffix_2nd"] = str_temp[4]
                    mark=1
                elif str_temp[2] in subscribed_appendix and str_temp[4] in suffix_2nd and str_temp[0] in super_appendix:
                    # 上加字+基字+下加字+后加字+再后加字
                    structure["superscribed"] = str_temp[0]
                    structure["root"] = str_temp[1]
                    structure["subscribed"] = str_temp[2]
                    structure["suffix"] = str_temp[3]
                    structure["suffix_2nd"] = str_temp[4]
                    mark=1
            elif (str_temp[1] >= chr(0x0F40) and str_temp[1] <= chr(0x0F6C)
                  ) and (str_temp[2] in overlying_base) and (str_temp[3] in overlying_base):
                # 第二个字符是前导字符并且第三个字符是叠加字符并且第四个字符是叠加字符
                # 前加字+上加字+基字+下加字+后加字
                if str_temp[0] in front_appendix and str_temp[3] in subscribed_appendix and str_temp[1] in super_appendix:
                    structure["prefix"] = str_temp[0]
                    structure["superscribed"] = str_temp[1]
                    structure["root"] = str_temp[2]
                    structure["subscribed"] = str_temp[3]
                    structure["suffix"] = str_temp[4]
                    mark=1
            else:
                if str_temp[2] in subscribed_appendix:
                    # 第三个字符是下加字（ ྱ、 ྲ、 ླ、 ྭ）
                    # 前加字+基字+下加字+后加字+再后加字
                    if str_temp[0] in front_appendix and str_temp[4] in suffix_2nd:
                        structure["prefix"] = str_temp[0]
                        structure["root"] = str_temp[1]
                        structure["subscribed"] = str_temp[2]
                        structure["suffix"] = str_temp[3]
                        structure["suffix_2nd"] = str_temp[4]
                        mark=1
                else:
                    # 前加字+上加字+基字+后加字+再后加字
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
            # 第五个字符是元音（ ི、 ུ、 ེ、 ོ）
            # 前加字+上加字+基字+下加字+元音+后加字
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
            # 第四个字符是元音（ ི、 ུ、 ེ、 ོ）
            if str_temp[1] in overlying_base:
                # 第二个字符是叠加字符
                if str_temp[1] in subscribed_appendix and str_temp[2] in subscribed_appendix_2nd:
                    # 第二个字符是下加字
                    # 基字+下加字+再下加字+元音+后加字+再后加字
                    structure["root"] = str_temp[0]
                    structure["subscribed"] = str_temp[1]
                    structure["subscribed_2nd"] = str_temp[2]
                    structure["vowel"] = str_temp[3]
                    structure["suffix"] = str_temp[4]
                    structure["suffix_2nd"] = str_temp[5]
                    mark=1
                elif str_temp[0] in front_appendix and str_temp[2] in subscribed_appendix and str_temp[5] in suffix_2nd:
                    # 上加字+基字+下加字+元音+后加字+再后加字
                    structure["superscribed"] = str_temp[0]
                    structure["root"] = str_temp[1]
                    structure["subscribed"] = str_temp[2]
                    structure["vowel"] = str_temp[3]
                    structure["suffix"] = str_temp[4]
                    structure["suffix_2nd"] = str_temp[5]
                    mark=1
            elif str_temp[1] >= chr(0x0F40) and str_temp[1] <= chr(0x0F6C):
                # 第二个字符是前导字符
                if str_temp[2] in subscribed_appendix:
                    # 第三个字符是下加字（ ྱ、 ྲ、 ླ、 ྭ）
                    # 前加字+基字+下加字+元音+后加字+再后加字
                    if str_temp[0] in front_appendix and str_temp[5] in suffix_2nd:
                        structure["prefix"] = str_temp[0]
                        structure["root"] = str_temp[1]
                        structure["subscribed"] = str_temp[2]
                        structure["vowel"] = str_temp[3]
                        structure["suffix"] = str_temp[4]
                        structure["suffix_2nd"] = str_temp[5]
                        mark=1
                elif str_temp[0] in front_appendix and str_temp[1] in super_appendix:
                    # 前加字+上加字+基字+元音+后加字+再后加字
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
            # 前加字+上加字+基字+下加字+后加字+再后加字
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



def j_del_beta(str_temp):    

    mark=tibet_to_digit(str_temp)
    

    if mark==0:

        if str_temp[-1] in gen_appendix:
            if str_temp[-1] == 'ོ':#终结助词
                ori,append=str_temp[:-2],str_temp[-2:]
                mark=tibet_to_digit(ori)
                result=ori+' '+append
                if result is None:
                    return str_temp
                return result
            elif str_temp[-1] == 'ི':#属格助词
                ori,append=str_temp[:-2],str_temp[-2:]
                mark=tibet_to_digit(ori)
                result=ori+'འ'+' '+append
                if result is None:
                    return str_temp
                return result

        elif str_temp[-2] in gen_appendix:
            ori,append=str_temp[:-3],str_temp[-3:]
            mark=tibet_to_digit(ori)
            result=ori+' '+append
            if result is None:
                return str_temp
            return result

        elif str_temp[-2] =='འ' and str_temp[-1]==('ར'):
            ori,append=str_temp[:-1],str_temp[-1]
            mark=tibet_to_digit(ori)
            result=ori+' '+append
            if result is None:
                return str_temp
            return result

        elif (str_temp[-2] ==('འ'or'མ') and str_temp[-1]=='ང') or (str_temp[-1]=='མ' and str_temp[-2] =='འ'):
            ori,append=str_temp[:-2],str_temp[-2:]
            mark=tibet_to_digit(ori)
            result=ori+' '+append
            if result is None:
                return str_temp
            return result

        elif len(str_temp)>=5:
            if str_temp[-4] =='འ' and (str_temp[-2] =='ི'):
                ori,append=str_temp[:-3],str_temp[-3:]
                mark=tibet_to_digit(ori)
                result=ori+'འ'+' '+append
                if result is None:
                    return str_temp
                return result
        else:
           return str_temp
    else:
        return str_temp

S_E=['་']
S_F=['།',]
S_double=['༄༅','།།','>>','<<']
S_D=['《','（','》','）','\"','“','”','？','༼','༽','༅','༄༅','—','(',')',':','<','>','·','?','༄']
N=['0','1','2','3','4','5','6','7','8','9','༠','༡','༢','༣','༤','༥','༦','༧','༨','༩','.']
en_word=['a','b','c','d','e','f','g','h','i','j','k','l','m','n'
      ,'o','p','q','r','s','t','u','v','w','x','y','z',
      'A','B','C','D','E','F','G','H','I','J','K','L','M','N',
      'O','P','Q','R','S','T','U','V','W','X','Y','Z']

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


def preserve(text_temp,dictory,config):#
    i=0
    while(i<len(text_temp)):
        mark2=0
        if len(text_temp[i])>=3:
            if ((text_temp[i][-1] == 'ི' and text_temp[i][-2] == 'འ') or  #
                (text_temp[i][-1] == 'ས' or (text_temp[i][-1] == 'ས' and text_temp[i][-2] == 'ི' and ((text_temp[i][-3] == 'ཡ' or text_temp[i][-3] =='འ') ) )) or #主格
                (text_temp[i][-1] == 'ར' ) or #
                (text_temp[i][-1] == 'ང' and (text_temp[i][-2] == 'ཡ' or text_temp[i][-2] == 'འ')) or #
                (text_temp[i][-1] == 'མ' and text_temp[i][-2] == 'འ') or #
                (text_temp[i][-1] == 'ོ' and text_temp[i][-2] == 'འ') #
                ):
                #---------- phase I -----------
                if i>=config.slide_size and (len(text_temp)-i)>config.slide_size: #10-gram #NEED #1
                    
                    test=''
                    front=''
                    rear=''
                    for j in range(i-1,i-config.slide_size-1,-1):
                        front=text_temp[j]+' '+front  #拼词
                    for j in range(i+config.slide_size,i,-1):
                        rear=text_temp[j]+' '+rear
                    for j in range(i-config.slide_size,i):
                        test=front+text_temp[i]+' '+rear       
                        test=test.strip(' ')
                        record=len(test)
                        
                    del_sign=0   
                    for j in range(i-config.slide_size,i+1):
                        test=front+text_temp[i]+' '+rear       
                        test=test.strip(' ')
                        record=len(test)
                        
                        if test in dictory and del_sign==0:
                            ##print(text_temp[i])
                            text_temp.insert(j,'⊙')
                            text_temp.insert(record+1,'ꈍ')
                            #text_temp.insert(record+len(test.split())-1,'⊙')
                            mark2=1
                            
                            i+=1
                            break
                        else:
                            del_sign=1
                                                       
                        
                        for k in range(i+config.slide_size,i-1,-1):
                            if test in dictory:
                                    mark2=1      
                                    ##print(text_temp[i],'&&&',text_temp[k])
                                    
                                    text_temp.insert(j,'⊙')
                                    text_temp.insert(k+2,'ꈍ')
                                    #test=test[len(text_temp[j])+1:]
                                    del_sign=1
                                    i+=1
                                    break
                               
                            else:
                                test=test[:(len(test)-len(text_temp[k])-1)]

                        
                        if test in dictory and del_sign==0:
                            ##print(text_temp[i],'&&&',text_temp[k])
                            text_temp.insert(j,'⊙')
                            text_temp.insert(k+1,'ꈍ')
                            #text_temp.insert(record+len(test.split())-1,'⊙')
                            mark2=1
                            i+=1
                            
                        
                        if mark2==1:
                            
                            break
                        else:
                            #test=test[len(text_temp[j])+1:]   
                            front=front[len(text_temp[j])+1:]                         

                elif i>=config.slide_size and (len(text_temp)-i)<config.slide_size:  #NEED  2
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
                            ##print(text_temp[i])
                            text_temp.insert(j,'⊙')
                            text_temp.insert(record+1,'ꈍ')
                            #text_temp.insert(record+len(test.split())-1,'⊙')
                            mark2=1
                            
                            i+=1
                            break
                        else:
                            del_sign=1
                                                       
                        
                        for k in range(len(text_temp)-1,i-1,-1):
                            if test in dictory:
                                    mark2=1      
                                    ##print(text_temp[i],'&&&',text_temp[k])
                                    
                                    text_temp.insert(j,'⊙')
                                    text_temp.insert(k+2,'ꈍ')
                                    #test=test[len(text_temp[j])+1:]
                                    del_sign=1
                                    i+=1
                                    break
                               
                            else:
                                test=test[:(len(test)-len(text_temp[k])-1)]

                        
                        if test in dictory and del_sign==0:
                            ##print(text_temp[i],'&&&',text_temp[k])
                            text_temp.insert(j,'⊙')
                            text_temp.insert(k+1,'ꈍ')
                            #text_temp.insert(record+len(test.split())-1,'⊙')
                            mark2=1
                            i+=1
                        
                        if mark2==1:
                            break
                        else:
                            #test=test[len(text_temp[j])+1:]   
                            front=front[len(text_temp[j])+1:]   
                elif i<config.slide_size and (len(text_temp)-i)>config.slide_size: #3
                    #i<10 部分完结 仍需测试
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
                                ##print(text_temp[i])
                                text_temp.insert(j,'⊙')
                                text_temp.insert(record+1,'ꈍ')
                                #text_temp.insert(record+len(test.split())-1,'⊙')
                                mark2=1
                                
                                i+=1
                                break
                            else:
                                del_sign=1
                                                        
                            
                            for k in range(i+config.slide_size,i-1,-1):
                                if test in dictory:
                                        mark2=1      
                                        ##print(text_temp[i],'&&&',text_temp[k])
                                        
                                        text_temp.insert(j,'⊙')
                                        text_temp.insert(k+2,'ꈍ')
                                        #test=test[len(text_temp[j])+1:]
                                        del_sign=1
                                        i+=1
                                        break
                                
                                else:
                                    test=test[:(len(test)-len(text_temp[k])-1)]

                            
                            if test in dictory and del_sign==0:
                                ##print(text_temp[i],'&&&',text_temp[k])
                                text_temp.insert(j,'⊙')
                                text_temp.insert(k+1,'ꈍ')
                                #text_temp.insert(record+len(test.split())-1,'⊙')
                                mark2=1
                                i+=1
                                
                            
                            if mark2==1:
                                
                                break
                            else:
                                #test=test[len(text_temp[j])+1:]   
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
                                ##print(text_temp[i])
                                text_temp.insert(j,'⊙')
                                text_temp.insert(record+1,'ꈍ')
                                #text_temp.insert(record+len(test.split())-1,'⊙')
                                mark2=1
                                
                                i+=1
                                break
                            else:
                                del_sign=1
                                                        
                            
                            for k in range(len(text_temp)-1,i-1,-1):
                                if test in dictory:
                                        mark2=1      
                                        ##print(text_temp[i],'&&&',text_temp[k])
                                        
                                        text_temp.insert(j,'⊙')
                                        text_temp.insert(k+2,'ꈍ')
                                        #test=test[len(text_temp[j])+1:]
                                        del_sign=1
                                        i+=1
                                        break
                                
                                else:
                                    test=test[:(len(test)-len(text_temp[k])-1)]

                            
                            if test in dictory and del_sign==0:
                                ##print(text_temp[i],'&&&',text_temp[k])
                                text_temp.insert(j,'⊙')
                                text_temp.insert(k+1,'ꈍ')
                                #text_temp.insert(record+len(test.split())-1,'⊙')
                                mark2=1
                                i+=1
                                
                            
                            if mark2==1:
                                
                                break
                            else:
                                #test=test[len(text_temp[j])+1:]   
                                front=front[len(text_temp[j])+1:]   

        i=i+1
 
 
 
    return text_temp                

                



def j_del_beta2(text_temp,dictory,config):
    divide_mark=1
    for i in range(len(text_temp)):
        if (text_temp[i]=='⊙'):
            divide_mark=0
        elif (text_temp[i]=='ꈍ'):
            divide_mark=1
        if len(text_temp[i])>=3 and (utils.Tibet_dect(text_temp[i][0])==True) and text_temp[i][0] not in (S_D+N+S_E+S_F) :
            mark2=0
            if divide_mark==1:#没找到 
                if (text_temp[i][-1] == 'ར' ):  #与格
                    test1=text_temp[i][:-1]+'འ' 
                    test2=text_temp[i][:-1] #
                    ##test_ori1=test1
                    test_ori2=test2
                    if i>config.slide_size:
                        for j in range(i-1,i-config.slide_size,-1):
                            test1=text_temp[j]+' '+test1 #
                            test2=text_temp[j]+' '+test2
                        test2=test2.strip(' ')   
                        test1=test1.strip(' ')   
                        for j in range(i-config.slide_size+1,i+1):                           
                            if test1 in dictory:
                                mark2=2  #mark2 说明该拆
                                
                                #text_temp[i]=test_ori1   #选择还原
                                text_temp[i]=test_ori2   #选择不还原                              
                                text_temp.insert(i+1,'ར')
                                break
                            if test2 in dictory:
                                mark2=2  #mark2 说明该拆
                                
                                text_temp[i]=test_ori2
                                text_temp.insert(i+1,'ར')    
                                break
                            else:
                                test2=test2[len(text_temp[j])+1:]
                                test1=test1[len(text_temp[j])+1:] #

                    else:
                #i<10 部分完结 仍需测试
                        for j in range(i-1,-1,-1):
                            test1=text_temp[j]+' '+test1
                            test2=text_temp[j]+' '+test2
                        test2=test2.strip(' ')   
                        test1=test1.strip(' ')                          
                        for j in range(i+1):
                            if test1 in dictory:
                                mark2=2
                                
                                #text_temp[i]=test_ori1   #选择还原
                                text_temp[i]=test_ori2   #选择不还原   
                                text_temp.insert(i+1,'ར')
                                break
                            if test2 in dictory:
                                mark2=2  #mark2 
                                
                                text_temp[i]=test_ori2
                                text_temp.insert(i+1,'ར')    
                                break
                            else:
                                test2=test2[len(text_temp[j])+1:]
                                test1=test1[len(text_temp[j])+1:]
                
                elif(text_temp[i][-1] == 'ི' and text_temp[i][-2] == 'འ'):
                    test1=text_temp[i][:-2]+'འ'  #属格
                    test2=text_temp[i][:-2]
                    #test_ori1=test1
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
                                
                                #text_temp[i]=test_ori1   #选择还原
                                text_temp[i]=test_ori2   #选择不还原   
                                text_temp.insert(i+1,'འི')
                                break
                            if test2 in dictory:
                                mark2=2  #mark2 说明该拆
                                
                                text_temp[i]=test_ori2
                                text_temp.insert(i+1,'འི')    
                                break
                            else:
                                test2=test2[len(text_temp[j])+1:]
                                test1=test1[len(text_temp[j])+1:]
                    else:
                    #i<10 部分完结 仍需测试
                        for j in range(i-1,-1,-1):
                            test1=text_temp[j]+' '+test1
                            test2=text_temp[j]+' '+test2
                        test2=test2.strip(' ')  
                        test1=test1.strip(' ')                          
                        for j in range(i+1):
                            if test1 in dictory:
                                mark2=2
                                
                                #text_temp[i]=test_ori1   #选择还原
                                text_temp[i]=test_ori2   #选择不还原   
                                text_temp.insert(i+1,'འི')
                                break
                            if test2 in dictory:
                                mark2=2  #mark2 说明该拆
                                
                                text_temp[i]=test_ori2
                                text_temp.insert(i+1,'འི')    
                                break
                            else:
                                test2=test2[len(text_temp[j])+1:]
                                test1=test1[len(text_temp[j])+1:]
                                
                elif(text_temp[i][-1] == 'ས'  #主格助词
                     ):
                    if text_temp[i][-2] == 'ི' and (text_temp[i][-3] == 'ཡ' or text_temp[i][-3] =='འ'): #
                        test1=text_temp[i][:-3]+'འ' #加འ还原型
                        test2=text_temp[i][:-3]
                    else:#
                        test1=text_temp[i][:-1]+'འ' ######
                        test2=text_temp[i][:-1]
                    #test_ori1=test1
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
                                
                                #text_temp[i]=test_ori1   #
                                text_temp[i]=test_ori2   #
                                text_temp.insert(i+1,'ས')
                                break
                            if test2 in dictory:
                                mark2=2  #mark2 说明该拆
                                
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
                                
                                #text_temp[i]=test_ori1   #
                                text_temp[i]=test_ori2   #  
                                text_temp.insert(i+1,'ས')
                                break
                            if test2 in dictory:
                                mark2=2  #mark2 说明该拆
                                
                                text_temp[i]=test_ori2
                                text_temp.insert(i+1,'ས')    
                                break
                            else:
                                test1=test1[len(text_temp[j])+1:]
                                test2=test2[len(text_temp[j])+1:]
                    #无需还原部分
                elif((text_temp[i][-2] == 'འ' and (text_temp[i][-1]=='ང' or text_temp[i][-1]=='མ') )or #
                     (text_temp[i][-2] == 'ཡ' and text_temp[i][-1]=='ང' ) or #
                     (text_temp[i][-2] == 'འ' and text_temp[i][-1]=='ོ') #
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
                    #i<10 部分完结 仍需测试
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
                        
                    #
                    #
                    #                   
                    #---------- phase II -----------

                if mark2==0 and divide_mark==1:#
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

def fina_del(text_temp,dictory,config):

    text_temp=input_sim_space(text_temp,divide_mark='་')
    text_temp=preserve(text_temp,dictory,config)  
    text_temp=j_del_beta2(text_temp,dictory,config)
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

