import re
import sys, os
from pyltp import SentenceSplitter, Segmentor, Postagger, Parser, NamedEntityRecognizer, SementicRoleLabeller
import pandas as pd
class ltp_api(object):
    def __init__(self, MODELDIR, exword_path='lexion'):
        self.MODELDIR = MODELDIR
        # self.output = {}
        self.words = None
        self.postags = None
        self.netags = None
        self.arcs = None
        self.exword_path = exword_path  # e.x: '‪E:\LTP\ltp_data_v3.4.0\exwords.txt'
        # 分词
        self.segmentor = Segmentor()
        if not self.exword_path:
            # 是否加载额外词典
            self.segmentor.load(os.path.join(self.MODELDIR, "cws.model"))
        else:
            self.segmentor.load_with_lexicon(os.path.join(self.MODELDIR, "cws.model"), self.exword_path)
        # 模型引用
        # 词性标注
        self.postagger = Postagger()
        self.postagger.load(os.path.join(self.MODELDIR, "pos.model"))
        # 依存句法
        self.parser = Parser()
        self.parser.load(os.path.join(self.MODELDIR, "parser.model"))
        # # 命名实体识别
        # self.recognizer = NamedEntityRecognizer()
        # self.recognizer.load(os.path.join(self.MODELDIR, "ner.model"))
        # 语义角色
        # self.labeller = SementicRoleLabeller()
        # self.labeller.load(os.path.join(MODELDIR, "pisrl.model"))
    # 分句
    def ltp_sentence_splitter(self, paragraph):
        sentence = SentenceSplitter.split(paragraph)  # 分句的列表
        # print ('\n'.join(sentence))
        return sentence

    # 分词
    def ltp_segmentor(self, sentence):
        words = self.segmentor.segment(sentence)
        # self.segmentor.release()
        return words#返回词的列表

    # 词性标注
    def ltp_postagger(self, words):
        postags = self.postagger.postag(words)
        # self.postagger.release()
        return postags#返回词性的列表

    # 依存语法
    def ltp_parser(self, words, postags):
        arcs = self.parser.parse(words, postags)
        # self.parser.release()
        return arcs

    # 命名实体识别
    def ltp_recognizer(self, words, postags):
        netags = self.recognizer.recognize(words, postags)
        # self.recognizer.release()
        return netags

    # 语义角色识别
    def ltp_labeller(self, words, postags, arcs):
        output = []
        roles = self.labeller.label(words, postags, arcs)
        # self.labeller.release()
        for role in roles:
            output.append([(role.index, arg.name, arg.range.start, arg.range.end) for arg in role.arguments])
        return output

    # 各种结果
    def get_result(self, sentence):
        self.words = self.ltp_segmentor(sentence)  # 句子变成词
        self.postags = self.ltp_postagger(self.words)  # 词性标注
        self.arcs = self.ltp_parser(self.words, self.postags)  # 依存句法
        self.netags = self.ltp_recognizer(self.words, self.postags)  # 命名实体
        # 载入output，以字典形式输出各种结果
        self.output['role'] = self.ltp_labeller(self.words, self.postags, self.arcs)  # 语义角色
        self.output['words'] = list(self.words)
        self.output['postags'] = list(self.postags)
        self.output['arcs'] = [(arc.head, arc.relation) for arc in self.arcs]
        self.output['netags'] = list(self.netags)
        return self.output
    def release(self):
        self.segmentor.release()
        self.postagger.release()
        self.parser.release()
        # self.recognizer.release()
        # self.labeller.release()
def nodu(path = '网贷平台评论.xlsx'):#输入Excel路径，输出去重的dataframe
    data0 = pd.read_excel(path)
    data = data0.iloc[:,1:5]
    data_nodu = data.drop_duplicates(['评论内容'])
    #data_nodu.to_csv()
    return data_nodu
def extract(dataframe):
    paragraphs = dataframe['评论内容'].values
    # print(paragraphs)#多个字符串组成的列表
    all_comments_shortcut = []
    for i in range(len(paragraphs)):
        # print (paragraphs[i])
        comment_shortcut = []
        for sentence in ltp.ltp_sentence_splitter(paragraphs[i]):
            sentence_shortcut = []
            sentence = "".join(sentence.split())  # 去除空格
            sentence = sentence.replace('*', '不可描述词')
            # sentence = sentence.replace('x','')# 去除*符号
            words = ltp.ltp_segmentor(sentence)  # 分词
            words_list = list(words)# 分词
            postags = ltp.ltp_postagger(words)  # 词性
            postags_list = list(postags)
            arcs = ltp.ltp_parser(words, postags)  # 依存
            arcs_list = ",".join("%d:%s" % (arc.head, arc.relation) for arc in arcs)
            arcs_list = arcs_list.split(',')
            # tuples_words = Parser2dataframe(words, postags, arcs)
            combine = [0]*len(words)#分词分成了7块
            # print(len(arcs))#7
            # print(len(list(arcs)))#7
            # print(arcs_list)#['3:SBV', '3:ADV', '0:HED', '5:ADV', '7:ATT', '5:RAD', '3:VOB']
            # print(len(arcs_list))#7
            #筛选含态度的短语
            for i in range(len(arcs_list)):
                s = re.match('\w*:VOB',arcs_list[i])
                if not str(s) == 'None':
                    p = int(re.sub(':.*','',arcs_list[i]))
                    combine[p-1] = i
                ss = re.match('\w*:FOB', arcs_list[i])
                if not str(ss) == 'None':
                    p = int(re.sub(':.*', '', arcs_list[i]))
                    combine[p - 1] = i
            #取出关系的父的索引，第一个词的索引为1
            #combine列表的索引是父的位置，值是子的位置。第一个词的位置是0
            # print(combine)#len(arcs)时:[0, 0, 6, 0, 0, 0, 0]
            for i in range(len(combine)):
                if combine[i] != 0:#子的位置不是0时:i = 2 combine[2] = 6
                    #组合含态度的短语
                    cut = ''
                    fword = ['没有','不是','并没']#,'尚未','还未','未','不用','不好'
                    judge = [0]*(combine[i]+1)
                    # print(judge)#[0, 0, 0, 0, 0, 0, 0]7个
                    for m in range(i,combine[i]+1):#从父位置开始到子位置的短语
                        if words_list[m] in fword:
                            judge[m] = 1#记录否定词的位置,judge[0,0,0,0,0,1,0]
                    # print(judge)#[0,0,1,0,0,0,0]把否定词的位置找到
                    if not 1 in judge:#如果没有否定词就直接把短句输出
                        for m in range(i,combine[i]+1):
                            cut = cut + words_list[m]
                        if cut != '':
                            sentence_shortcut.append(cut)
                    else:#如果有否定词
                        if postags_list[combine[i]] == 'a':#如果子是形容词
                            modify = '不' + words_list[combine[i]]#否定那个形容词
                            for m in range(i,combine[i]):#从父到子短语的遍历
                                if judge[m] == 1:#如果否定词出现
                                    wo = ''#wo设为空
                                else:#如果没有否定词
                                    wo = words_list[m]#wo还是原来的词
                                cut = cut + wo#cut为从父到子之前所有词的组合（去除否定词）
                            cut = cut + modify#cut为cut和否定的子的组合，完成了否定词否定到子本身的修改
                            if cut!='':
                                sentence_shortcut.append(cut)
                        else:#如果子不是形容词
                            for m in range(i,combine[i]+1):
                                cut = cut + list(words)[m]#直接cut从父到子
                            if cut != '':
                                sentence_shortcut.append(cut)
            if len(sentence_shortcut) != 0:
                comment_shortcut.append(sentence_shortcut)
        all_comments_shortcut.append(comment_shortcut)#所有的从父到子都加到shortcut里，每一个短句会有几个cut，每个短句的cut应该放到一个comment_shortcut里面
    return all_comments_shortcut# [[['求你们了快还钱吧']], [['是我在浙江投资的算是', '算是一个非常好的平台', '提出他们的服务', '有什么问题', '得到很好的回复', '是越来越透明', '希望越来越好']],...]

def extract1(paragraphs):
    n_a_para = [ ]
    for paragraph in paragraphs:
        # adj = []
        # noun = []
        adj_noun = []
        for comment in paragraph:
            for sentence in comment:
                for phrase in sentence:
                    words = ltp.ltp_segmentor(phrase)
                    word_list = list(words)
                    postags = ltp.ltp_postagger(words)
                    postags_list = list(postags)
                    if 'a' in postags_list and 'n' in postags_list:
                        obn = word_list[postags_list.index('n')]
                        # noun.append(obn)#noun存放着名词
                        oba = word_list[postags_list.index('a')]
                        # adj.append(oba)#adj存放着形容词
                        adj_noun.append(obn+oba)
        n_a_para.append(adj_noun)
    return n_a_para
        # frames = []
        # mylist = list(set(noun))#mylist存放着名词去重之后的结果
        # for noun in mylist:
        #     adjnew=[]
        #     for i in range(len(adj)):
        #         if noun == noun(i):
        #             adjnew.append(adj[i])
        #     #adjnew存放着对去重之后的名词按顺序
        #     singleadjlist = []
        #     adjlist = list(set(adjnew))
        #     for i in adjlist:
        #         num = str(adjnew.count(i))
        #         singleadjlist.append(num+'_'+i)
        #     if len(singleadjlist)>1:
        #         frames.append(pd.DataFrame({n:singleadjlist}))
        #     print (frames)
                # n_a = pd.concat(frames,axis=1)
                # print (n_a)
        # n_a_para.append(n_a)
        # n_a.to_csv('pn.csv')
    # return  n_a_para

def data_insert(list_insert,name,path):
    data = pd.read_csv(path)
    data[name] = list_insert
    return data

def plat_comment(data_nodu_comment):
    # print (data_nodu_comment['情感短语'])#[[上市背景系车贷平台安全第一, 合规]]
    platforms = list(set(data_nodu_comment['平台名称']))
    phrases = []
    for i in range(len(platforms)):
        phrases.append(list(data_nodu_comment[data_nodu_comment['平台名称'].isin([platforms[i]])]['情感短语'].values))
    plat_com = {'平台':platforms,'情感短语':phrases}#comments:['',''],['']...
    plat_com_df = pd.DataFrame(plat_com)
    # plat_com_df.to_csv('plat_com_df.csv')
    return plat_com_df#[[[有点不放心]], [[就是标的信息不透明, 借钱]], [[还是蛮高, 希望贵平台越做]]]

def static_word(paragraphs):# ['上市背景系车贷平台安全第一', '合规'](platform comment phrase)
    adj = []
    noun = []
    for i in range(0, 5):
        adj_per = []
        for comment in paragraphs[i]:
            for sentence in comment:
                for phrase in sentence:
                    if len(phrase) != 0 :
                        words = ltp.ltp_segmentor(phrase)
                        # print (words)
                        words_list = list(words)
                        postags = ltp.ltp_postagger(words)
                        postags_list = list(postags)
                        for i in range(len(postags_list)):
                            if postags_list[i] == 'a':
                                adj.append(words_list[i])
                            if postags_list[i] == 'n':
                                noun.append(words_list[i])
    adjlist = list(set(adj))
    nounlist = list(set(noun))
    return adjlist,nounlist

def static_words(sentence):# ['上市背景系车贷平台安全第一', '合规'](platform comment phrase)
    adj = []
    noun = []
    for phrase in sentence:
        if len(phrase) != 0 :
            words = ltp.ltp_segmentor(phrase)
            # print (words)
            words_list = list(words)
            postags = ltp.ltp_postagger(words)
            postags_list = list(postags)
            for i in range(len(postags_list)):
                if postags_list[i] == 'a':
                    adj.append(words_list[i])
                if postags_list[i] == 'n':
                    noun.append(words_list[i])
    adjlist = list(set(adj))
    nounlist = list(set(noun))
    return adjlist,nounlist

def static_allwords(paragraphs):
    paragraphsadj = []
    paragraphsnoun = []
    for paragraph in paragraphs:
        # print (i)#[[['是来', '来了投资的好地方']]]
        commentsadj = []
        commentsnoun = []
        for comment in paragraph:
            # print (j)#[['有风投', '急需解决', '解决坏账问题']]
            pharsesadj = []
            pharsesnoun = []
            for phrase in comment:
                if len(phrase)>0:
                    # print (k)#['算比较满意', '觉得还是', '还是满适合', '适合做', '做长期投资']
                    phrasewords = static_words(phrase)#每个短语的形容词和名词元组
                    if len(phrasewords[0])!=0:
                        pharsesadj.append(phrasewords[0])
                    else:
                        if len(phrasewords[0]) == 0:
                            pharsesadj.append(['短语无形容词'])
                    if len(phrasewords[1])!=0:
                        pharsesnoun.append(phrasewords[1])
                    else:
                        if len(phrasewords[1]) == 0:
                            pharsesnoun.append(['短语无名词'])
            commentsadj.append(pharsesadj)
            commentsnoun.append(pharsesnoun)
        paragraphsadj.append(commentsadj)
        paragraphsnoun.append(commentsnoun)
    return paragraphsadj,paragraphsnoun

def static_frequency(paragraphslist):
    allfinal = []
    # print (len(paragraphslist))#262
    for paragraph in paragraphslist:
        pharselist = []
        # print (paragraph)#[[['好']], [['踏实', '最高']], [['小']], [['短语无形容词']], [['安全']], [['丰富']], [['短语无形容词']]]
        for comment in paragraph:
            for sentence in comment:
                for pharse in sentence:
                # if len(phrase)!=0:
                    pharselist.append(pharse)
        allfinal.append(pharselist)
    return allfinal

def static_frequency1(paragraphslist):
    finallist = []
    for phraselist in paragraphslist:
        mylist = list(set(phraselist))
        paragraph = []
        for i in mylist:
            num = str(phraselist.count(i))
            paragraph.append(i + 'p=' + num)
        finallist.append(paragraph)
    return finallist

def get_tuples_word(word_list1, n1, word_list2, n2):
    # 按照顺序，拼接词
    result = []
    for i, n1s, j, n2s in zip(word_list1, n1, word_list2, n2):
        if n1s < n2s:
            result.append(''.join([i, j]))
        else:  # n1s > n2s
            result.append(''.join([j, i]))
    return result

def Parser2dataframe(words, postags, arcs):
    '''
    把依存句法解构成dataframe
    '''
    word_dict = dict(enumerate(words))#给words中的每一个元素加索引，从0开始，形成字典
    match_word = []
    relation = []
    pos = []
    match_word_n = []
    # 解读
    for n, arc in enumerate(arcs):#arc:父节点和关系
        relation_word = 'root ' if arc.head - 1 < 0 else word_dict[arc.head - 1] #取出核心词，root，为空
        match_word.append(relation_word)
        relation.append(arc.relation)
        pos.append(postags[n])
        match_word_n.append(0 if arc.head - 1 < 0 else arc.head - 1)

    tuples_words = pd.DataFrame({'word': list(word_dict.values()), 'word_n': list(word_dict.keys()), \
                                 'match_word': match_word, 'relation': relation, 'pos': pos,
                                 'match_word_n': match_word_n})
    tuples_words['tuples_words'] = get_tuples_word(tuples_words['word'], tuples_words['word_n'], \
                                                   tuples_words['match_word'], tuples_words['match_word_n'])
    return tuples_words

def get_tuple(phrase):
    words = ltp.ltp_segmentor(phrase)
    postags = ltp.ltp_postagger(words)
    arcs = ltp.ltp_parser(words,postags)
    tuple = Parser2dataframe(words,postags,arcs)
    return tuple
# def get_n_a_list(phrase):
#     words = ltp.ltp_segmentor(phrase)
#     word_list = list(words)
#     postags = ltp.ltp_postagger(words)
#     postags_list = list(postags)
#     arcs = ltp.ltp_parser(words, postags)
#     for i in postags_list:
#         if i == 'a':

MODELDIR='D:\LTP3.4'   #  模型文件
ltp = ltp_api(MODELDIR)

all_comment_shortcut = extract(nodu())
data_nodu_comment = data_insert(all_comment_shortcut,'情感短语','data_nodu.csv')
plat_comment_df = plat_comment(data_nodu_comment)
paragraphs = plat_comment_df['情感短语']
plat_comment_df.to_csv('plat_com_adj_noun.csv')
impression = extract1(paragraphs)
plat_comment_df['用户印象'] = impression
plat_comment_df.to_csv('platform_impression.csv')
print ('done')
ltp.release()


