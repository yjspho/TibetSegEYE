****** TibetSegEYE ******

感谢使用TibetSegEYE！

TibetSegEYE是一款针对藏文的开源分词小工具，本人谨以此工具对藏文自然语言处理做出些许贡献。

如果您认可该项目，请点击星星支持！

由于本人代码能力有限，有所不足，多多包涵！


***若原始文本已经处理过黏着词，则关闭黏着词相应模块可以获得更好的处理效果。***
***若本项目带来些许帮助，希望可以在您的研究中引用本论文，谢谢！***


使用时请修改models.config中的save_result、supvoc、model_path。


*** maintest.py 单条文本数据分词
*** multiprocess.py 多进程批量文本分词。注意：需在该文件中依照个人配置设置进程数。


模型设置：


*** save_result：指向本项目模型 目前提供Segbase及V2下载。 
链接：https://pan.baidu.com/s/1j_60cDWVlfryikaP-1Nvbw 提取码：19pe。

V2:链接:https://pan.baidu.com/s/1K738XIDss5B_IDZM9vCGAw?pwd=hg9g 提取码:hg9g


*** model_path：指向预训练模型 可使用Tibert等。
*** supvoc：指向support词表（rec_dict_rset2.txt）。该部分可替换。
*** slide_size：滑动窗口大小。降低该数值可以极大幅度提高分词速度，但可能会损失精确度。


Development environment:
Python==3.10
torch==1.13.1+cu117
transformers==4.28.1


Model description:
segbase 训练自MLWS2021数据集。
后续会补充其他模型。


*update 2023.7.22：修正了一些参数，增加滑动窗口调节及多进程处理，使得该工具处理速度提高3倍以上。

*update 2024.4.10：修复了一些BUG，调整了算法逻辑，并再次提高处理性能。

*update 2024.7.18：更新V2。

E：yjspho@utibet.edu.cn(已毕业，废弃)  tpcwy08@126.com
