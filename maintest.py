
import utils
import models
from importlib import import_module
import torch
import appedix_restore
import numpy as np
import time
import tools
#TibetSegEye
#单次输入


config=models.config()

model=models.No_encoder_model(config)
np.random.seed(0)
torch.manual_seed(0)
torch.cuda.manual_seed_all(3)

torch.backends.cudnn.deterministic=True
torch.backends.cudnn.benchmark =False

#use
model.load_state_dict(torch.load(config.save_result))
id2label = config.i2b
model.to(config.device)
dictory=appedix_restore.dict_confirm(config)
sym_dic=tools.symbol_define()
while 1:
    seq=input()
    a=time.time()
    seq_out=utils.model_use(model,config,seq,dictory,id2label,sym_dic)
    b=time.time()-a
    
    print(b)
    print(seq_out)
pass


####330####