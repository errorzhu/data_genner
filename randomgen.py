# coding=utf-8
import random
import time
import datetime
import string
import const

class RandomGenner(object):
    def __init__(self):
        #常用中文姓氏
        self.last_name = const.last_name
        #邮箱后缀
        self.mail_suffix = const.mail_suffix
        #手机前缀
        self.mobile_prefix = const.mobile_start
        #身份证区号
        self.identity_prefix = const.identity_prefix
        #训练数据集生成的word map
        self.word_dict = self.init_source_text()
    # 数字
    def gen_number(self, range=None):
        if range is None:
            return random.random()
        elif len(range) != 2:
            raise Exception('range only has top and bottom')
        else:
            bottom = range[0]
            top = range[1]
            return random.uniform(bottom, top)

    # 字母
    def gen_letter(self, length=1):
        return ''.join(random.choice(string.ascii_letters) for _ in range(length))

    # 混合数字字母
    def gen_mix_number_letter(self, length=1):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

    # 中文名
    def gen_chinese_name(self):
        name = []
        name.append(random.choice(self.last_name))
        name.append(''.join(chr(random.randint(0x4e00, 0x9fbf)) for _ in range(random.randint(1, 2))))
        return ''.join(name)

    # 电话号码
    def gen_mobile(self):
        return random.choice(self.mobile_prefix) + str(random.randint(10000000, 99999999))

    # 日期
    def gen_date(self,format='%Y-%m-%d %H:%M:%S'):
        start = (1976, 1, 1, 0, 0, 0, 0, 0, 0)
        end = time.localtime(time.time())
        start_stamp = time.mktime(start)
        end_stamp = time.mktime(end)
        ti = random.randint(start_stamp,end_stamp)
        date_touple = time.localtime(ti)
        date = time.strftime(format, date_touple)
        return date

    # 邮箱
    def gen_mail(self):
        return '%s@%s' % (self.gen_mix_number_letter(random.randint(5, 10)), random.choice(self.mail_suffix))

    # 给定范围的枚举
    def gen_enum(self, seq):
        return random.choice(seq)

    def gen_identity_no(self):
        id = random.choice(self.identity_prefix)
        id = id + str(random.randint(1970, datetime.datetime.today().year))
        da = datetime.date.today() + datetime.timedelta(days=random.randint(1, 366))
        id = id + da.strftime('%m%d')
        id = id + str(random.randint(100, 300))
        i = 0
        count = 0
        weight = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        checkcode = {'0': '1', '1': '0', '2': 'X', '3': '9', '4': '8', '5': '7', '6': '6', '7': '5', '8': '5', '9': '3',
                     '10': '2'}
        for i in range(0, len(id)):
            count = count + int(id[i]) * weight[i]
        id = id + checkcode[str(count % 11)]
        return id


    def init_source_text(self):
        words = []
        punc = ',.!?[]()%#@&1234567890"":'
        # 中英文标点映射表
        table = {ord(f): ord(t) for f, t in zip(
            u'，。！？【】（）％＃＠＆１２３４５６７８９０”“：、',
            u',.!?[]()%#@&1234567890"":.')}
        with open('source_text', 'r', encoding='utf-8') as f:
            text = f.read()
            text = text.translate(table)
            # 去换行符和空白
            text = text.replace('\\s+', '')
            text = text.replace('\n', '')
            text = text.replace('　', '')
            words = [word for word in text if word != '' and word not in punc]
        word_dict = {}
        for i in range(1, len(words)):
            if words[i - 1] not in word_dict:
                # 为单词新建一个词典
                word_dict[words[i - 1]] = {}
            if words[i] not in word_dict[words[i - 1]]:
                word_dict[words[i - 1]][words[i]] = 0
                word_dict[words[i - 1]][words[i]] = word_dict[words[i - 1]][words[i]] + 1

        return word_dict

                # 随机连贯文本，马尔科夫链
    def gen_random_text(self,startup='你',length=10):

        word = startup
        result=[]
        for i in range(length):
            result.append(word)
            arr = []
            for j in self.word_dict[word]:
                for k in range(self.word_dict[word][j]):
                    arr.append(j)
            word = arr[int((len(arr)) * random.random())]
        return ''.join(result)


if __name__ == "__main__":
    genner = RandomGenner()
  #  print(genner.gen_letter(52))
  #   print(genner.gen_enum(['男', '女']))
  #   print(genner.gen_chinese_name())
  #   print(genner.gen_mobile())
  #   print(genner.gen_mail())
  #   print(genner.gen_identity_no())
  #   #%Y-%m-%d %H:%M:%S
  #   print(genner.gen_date('%Y-%m-%d'))
    for i in range(100):
        m = genner.gen_random_text(random.choice(['青','春','幸','光','明','活','福','卫']),random.randint(2,4))
        print (m)


