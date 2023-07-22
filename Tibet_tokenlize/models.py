import torch.nn as nn
from transformers import BertModel,BertConfig,BertTokenizer
import torch
import tools
from TorchCRF import CRF
import os


from sklearn import preprocessing


class config(object):
    def __init__(self) -> None:
        self.model_name='Tibet_voctokenize'
        self.device=torch.device('cuda')
        self.batch_size=64
        self.num_epochs=320
        self.model_path=r'C:\python\2023-1-new\Tibetan\tokenlize\finetune\CINO\TiBERT' #
        self.tokenizer=BertTokenizer.from_pretrained(self.model_path)
        self.lr_rate=2e-5
        self.pad_size=512
        self.hidden_size=768
        self.slide_size=6  #滑动窗口大小
        self.save_result=r'C:\python\2023-1-new\Tibetan\save\shuffle1bilstm.cpkt'
        self.w2i,self.i2w=tools.Tibet_convert_dict(r'C:\python\2023-1-new\Tibetan\tokenlize\finetune\CINO\TiBERT\vocab.txt') #预训练模型下的词表位置
        self.b2i,self.i2b=tools.Tibet_convert_dict(r'C:\python\2023-1-new\Tibetan\update use\support\biotype.txt') #in support
        self.supvoc=r'C:\python\2023-1-new\Tibetan\update use\support\vocab.txt'#in support

class No_encoder_model(nn.Module):
    def __init__(self,config):
        super().__init__()
        self.bert=BertModel.from_pretrained(config.model_path)
        for paras in self.bert.parameters():
            paras.requires_grad = False
        #

        self.lstm=nn.LSTM(768,768)
        self.drop=nn.Dropout(0.1)

        self.vocab_dense=nn.Linear(768,5)
        self.prob_softmax=torch.nn.Softmax()

        self.bilstm=nn.LSTM(
            input_size=768,  # 1024
            hidden_size=768 // 2,  # 1024
            batch_first=True,
            num_layers=4,
            #bias=False,
            dropout=0.4,  # 0.5
            bidirectional=True,
            device=config.device
        )
        self.crf = CRF(5, batch_first=True)
        self.ly=nn.LayerNorm(768)

    def forward(self,package,use_lstm=True,use_label=None):

        context=package[0]  # shape=[128,32] 分别为batch_size与sequence_lenth 
        mask=package[1]#  *在config中设定
        hidden, pooled=self.bert(context,attention_mask=mask,return_dict=False) #hidden=64 128 768     pool=64 768  B(64) * S(solid128) * D(768)
    
        if not use_lstm:
            hidden = hidden
        else:
            hidden,_=self.bilstm(hidden) #b*s*v

        hidden=self.ly(hidden)  #
        logits_seq = self.vocab_dense(hidden) # B * (128) * labels

        outputs_loss = (logits_seq,)

        if use_label is not None:
            loss_mask = use_label.gt(0)
            loss = self.crf(logits_seq, use_label, loss_mask) * (-1)
            outputs_loss = (loss,) + outputs_loss

        return logits_seq,outputs_loss
        



