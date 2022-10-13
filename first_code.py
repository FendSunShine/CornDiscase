import os
import re
# ---------------------------------------------------#
#   XML处理： 按大致图像把每种单独图像的标签给全部赋值
#   0 - 462 全是CD
#   463 -1293 全是Pp
#   1293 -2472 全是CR
#   2472-3617 全是Bt
#   3618-4319 全是ML
# ---------------------------------------------------#

# 文件需要TXT类型
def XmlChangeAllBoxName(file):
    for fname in os.listdir(file):
        with open(os.path.join(file, fname), "r") as f:
            str = f.read()
            index = int(fname[:-4])
            if index < 463:
                str = re.sub('CD|Pp|CR|ML|Bt', 'CD', str)
            elif index < 1294:
                str = re.sub('CD|Pp|CR|ML|Bt', 'Pp', str)
            elif index < 2473:
                str = re.sub('CD|Pp|CR|ML|Bt', 'CR', str)
            elif index < 3618:
                str = re.sub('CD|Pp|CR|ML|Bt', 'Bt', str)
            else:
                str = re.sub('CD|Pp|CR|ML|Bt', 'ML', str)
        with open(os.path.join(file, fname), "w") as f:
            f.write(str)

XmlChangeAllBoxName('newCreatXml')