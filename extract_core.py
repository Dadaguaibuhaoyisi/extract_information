#!/usr/bin/python
# -*- coding:utf-8 -*-
# import sys, os
# from pyltp import SentenceSplitter, Segmentor, Postagger, Parser, NamedEntityRecognizer, SementicRoleLabeller
# import pandas as pd
# LTP_DATA_DIR = 'E:\LTP\ltp_data_v3.4.0'  # ltp模型目录的路径
# cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
# pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`
# ner_model_path = os.path.join(LTP_DATA_DIR, 'ner.model')  # 命名实体识别模型路径，模型名称为`pos.model`
# par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')  # 依存句法分析模型路径，模型名称为`parser.model`
# srl_model_path = os.path.join(LTP_DATA_DIR, 'pisrl_win.model')  # 语义角色标注模型目录路径，模型目录为`srl`。注意该模型路径是一个目录，而不是一个文件。
#
# from pyltp import SentenceSplitter
# from pyltp import Segmentor
# from pyltp import Postagger
# from pyltp import NamedEntityRecognizer
# from pyltp import Parser
# from pyltp import SementicRoleLabeller
#
# #分句，也就是将一片文本分割为独立的句子
# def sentence_splitter(paragraph):
#     sentence = SentenceSplitter.split(paragraph)  # 分句的列表
#     # print ('\n'.join(sentence))
#     return sentence
#
# #分词
# def segmentor(sentence):
#     segmentor = Segmentor()  # 初始化实例
#     segmentor.load(cws_model_path)  # 加载模型
#     words = segmentor.segment(sentence)  # 分词
#     #默认可以这样输出
#     # print ('\t'.join(words))
#     # 可以转换成List 输出
#     words_list = list(words)
#     segmentor.release()  # 释放模型
#     return words#_list#输入句子，输出分词#type是字符串，打印的时候要list（）之后才可以
# # 词性标注
# def posttagger(words):
#     postagger = Postagger() # 初始化实例
#     postagger.load(pos_model_path)  # 加载模型
#     postags = postagger.postag(words)  # 词性标注
#     # for word,tag in zip(words,postags):
#     #     print (word+'/'+tag)
#     postagger.release()  # 释放模型
#     return postags#输入分词的字符串，输出词性type是字符串，打印的时候要list（）之后才可以
#
# # 命名实体识别
# def ner(words, postags):
#     recognizer = NamedEntityRecognizer() # 初始化实例
#     recognizer.load(ner_model_path)  # 加载模型
#     netags = recognizer.recognize(words, postags)  # 命名实体识别
#     # for word, ntag in zip(words, netags):
#     #     print (word + '/' + ntag)
#     recognizer.release()  # 释放模型
#     return netags#输入分词和词性的字符串，输出命名实体type是字符串，打印的时候要list（）之后才可以
# #['S-Ni', 'O', 'S-Nh', 'O', 'B-Ns', 'E-Ns', 'O', 'O', 'O', 'O', 'S-Ns', 'O', 'O', 'O', 'O', 'O']
#
# # 依存语义分析
# def parse(words, postags):
#     parser = Parser() # 初始化实例
#     parser.load(par_model_path)  # 加载模型
#     arcs = parser.parse(words, postags)  # 句法分析
#     # print ("\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs))
#     parser.release()  # 释放模型
#     return arcs#输入分词和词性，输出依存语义字符串，包含头和关系
# #2:ATT	3:ATT	4:SBV	7:ATT	6:ATT	4:VOB	8:ADV	0:HED	8:WP	8:COO	13:SBV	13:ADV	10:VOB	15:ATT	13:VOB	8:WP
# # 角色标注
# def role_label(words, postags, arcs):
#     labeller = SementicRoleLabeller() # 初始化实例
#     labeller.load(srl_model_path)  # 加载模型
#     roles = labeller.label(words, postags,  arcs)  # 语义角色标注
#     # for role in roles:
#     #     print (role.index, "".join(
#     #         ["%s:(%d,%d)" % (arg.name, arg.range.start, arg.range.end) for arg in role.arguments]))
#     labeller.release()  # 释放模型
#     return roles#输入分词，词性，依存语义，输出角色
# #7 TMP:(0,6)A1:(9,14)
# # 9 A1:(10,10)
# # #role.index 代表谓词的索引，role.arguments 代表关于该谓词的若干语义角色。
# # arg.name 表示语义角色类型，arg.range.start 表示该语义角色起始词位置的索引，arg.range.end 表示该语义角色结束词位置的索引。
#
# # 语义角色识别
# def ltp_labeller(roles):
#     output = []
#     for role in roles:
#         output.append([(role.index,arg.name, arg.range.start, arg.range.end) for arg in role.arguments])
#     return output
#
# paragraph = '逾期标是怎么处理的，2%的费用是强制收取吗? 网站及App里面信息披露未更新，还有就是审计报告到现在都没有上传。是不是没有维护人员？'
# # paragraph = '刚接触这家平台，投了一两次，就这两次的经验来看，还不错，两次收款提现都很及时，还行吧！'
# sentence = sentence_splitter(paragraph)
# # print(list(sentence))
# # words = []
# # postags = []
# # arcs = []
# # recognizers = []
# def get_tuples_word(word_list1, n1, word_list2, n2):
#     # 按照顺序，拼接词，形成元组
#     result = []
#     for i, n1s, j, n2s in zip(word_list1, n1, word_list2, n2):
#         if n1s < n2s:
#             result.append(''.join([i, j]))
#         else:  # n1s > n2s
#             result.append(''.join([j, i]))
#     return result
#
# for i in sentence:
#     word = segmentor(i)
#     postag = posttagger(word)
#     arc = parse(word, postag)#输入分词和词性，输出依存语义字符串，包含头和关系 37:VOB	40:ATT	38:VOB	3:WP
#     word_dict = dict(enumerate(word))
#     # print(word_dict)
#     match_word = []
#     relation = []
#     pos = []
#     match_word_n = []
#     for n, arc in enumerate(arc):  # n:enumerate生成的索引 arc:父节点,关系
#         relation_word = 'root' if arc.head - 1 < 0 else word_dict[arc.head - 1]  # 取出核心词，root，为空
#         match_word.append(relation_word)#核心词添加
#         relation.append(arc.relation)#核心关系添加
#         pos.append(postag[n])#核心词词性添加
#         match_word_n.append(0 if arc.head - 1 < 0 else arc.head - 1)
#
#     tuples_words = pd.DataFrame({'word': list(word_dict.values()), 'word_n': list(word_dict.keys()), \
#                                  'match_word': match_word, 'relation': relation, 'pos': pos,
#                                  'match_word_n': match_word_n})
#     tuples_words['tuples_words'] = get_tuples_word(tuples_words['word'], tuples_words['word_n'], \
#                                                    tuples_words['match_word'], tuples_words['match_word_n'])
#     print(tuples_words)

# -*- coding: gb2312 -*-
import re
import sys, os
from pyltp import SentenceSplitter, Segmentor, Postagger, Parser, NamedEntityRecognizer, SementicRoleLabeller
import pandas as pd
class LtpParser:
    def __init__(self):
        LTP_DIR = "E:\LTP\ltp_data_v3.4.0"
        self.segmentor = Segmentor()
        self.segmentor.load(os.path.join(LTP_DIR, "cws.model"))

        self.postagger = Postagger()
        self.postagger.load(os.path.join(LTP_DIR, "pos.model"))

        self.parser = Parser()
        self.parser.load(os.path.join(LTP_DIR, "parser.model"))

        self.recognizer = NamedEntityRecognizer()
        self.recognizer.load(os.path.join(LTP_DIR, "ner.model"))

        self.labeller = SementicRoleLabeller()
        self.labeller.load(os.path.join(LTP_DIR, 'pisrl_win.model'))

    '''语义角色标注'''
    def format_labelrole(self, words, postags):
        arcs = self.parser.parse(words, postags)
        roles = self.labeller.label(words, postags, arcs)
        roles_dict = {}
        for role in roles:
            roles_dict[role.index] = {arg.name:[arg.name,arg.range.start, arg.range.end] for arg in role.arguments}
        return roles_dict

    '''句法分析---为句子中的每个词语维护一个保存句法依存儿子节点的字典'''
    def build_parse_child_dict(self, words, postags, arcs):
        child_dict_list = []
        format_parse_list = []
        for index in range(len(words)):
            child_dict = dict()
            for arc_index in range(len(arcs)):
                if arcs[arc_index].head == index+1:   #arcs的索引从1开始
                    if arcs[arc_index].relation in child_dict:
                        child_dict[arcs[arc_index].relation].append(arc_index)
                    else:
                        child_dict[arcs[arc_index].relation] = []
                        child_dict[arcs[arc_index].relation].append(arc_index)
            child_dict_list.append(child_dict)
        rely_id = [arc.head for arc in arcs]  # 提取依存父节点id
        relation = [arc.relation for arc in arcs]  # 提取依存关系
        heads = ['Root' if id == 0 else words[id - 1] for id in rely_id]  # 匹配依存父节点词语
        for i in range(len(words)):
            # ['ATT', '李克强', 0, 'nh', '总理', 1, 'n']
            a = [relation[i], words[i], i, postags[i], heads[i], rely_id[i]-1, postags[rely_id[i]-1]]
            format_parse_list.append(a)

        return child_dict_list, format_parse_list

    '''parser主函数'''
    def parser_main(self, sentence):
        words = list(self.segmentor.segment(sentence))
        postags = list(self.postagger.postag(words))
        arcs = self.parser.parse(words, postags)
        child_dict_list, format_parse_list = self.build_parse_child_dict(words, postags, arcs)
        roles_dict = self.format_labelrole(words, postags)
        return words, postags, child_dict_list, roles_dict, format_parse_list


class TripleExtractor:
    def __init__(self):
        self.parser = LtpParser()

    '''文章分句处理, 切分长句，冒号，分号，感叹号等做切分标识'''
    def split_sents(self, content):
        return [sentence for sentence in re.split(r'[？?！!。；;：:\n\r]', content) if sentence]

    '''利用语义角色标注,直接获取主谓宾三元组,基于A0,A1,A2'''
    def ruler1(self, words, postags, roles_dict, role_index):
        v = words[role_index]
        role_info = roles_dict[role_index]
        if 'A0' in role_info.keys() and 'A1' in role_info.keys():
            s = ''.join([words[word_index] for word_index in range(role_info['A0'][1], role_info['A0'][2]+1) if
                         postags[word_index][0] not in ['w', 'u', 'x'] and words[word_index]])
            o = ''.join([words[word_index] for word_index in range(role_info['A1'][1], role_info['A1'][2]+1) if
                         postags[word_index][0] not in ['w', 'u', 'x'] and words[word_index]])
            if s  and o:
                return '1', [s, v, o]
        # elif 'A0' in role_info:
        #     s = ''.join([words[word_index] for word_index in range(role_info['A0'][1], role_info['A0'][2] + 1) if
        #                  postags[word_index][0] not in ['w', 'u', 'x']])
        #     if s:
        #         return '2', [s, v]
        # elif 'A1' in role_info:
        #     o = ''.join([words[word_index] for word_index in range(role_info['A1'][1], role_info['A1'][2]+1) if
        #                  postags[word_index][0] not in ['w', 'u', 'x']])
        #     return '3', [v, o]
        return '4', []

    '''三元组抽取主函数'''
    def ruler2(self, words, postags, child_dict_list, arcs, roles_dict):
        svos = []
        for index in range(len(postags)):
            tmp = 1
            # 先借助语义角色标注的结果，进行三元组抽取
            if index in roles_dict:
                flag, triple = self.ruler1(words, postags, roles_dict, index)
                if flag == '1':
                    svos.append(triple)
                    tmp = 0
            if tmp == 1:
                # 如果语义角色标记为空，则使用依存句法进行抽取
                # if postags[index] == 'v':
                if postags[index]:
                # 抽取以谓词为中心的事实三元组
                    child_dict = child_dict_list[index]
                    # 主谓宾
                    if 'SBV' in child_dict and 'VOB' in child_dict:
                        r = words[index]
                        e1 = self.complete_e(words, postags, child_dict_list, child_dict['SBV'][0])
                        e2 = self.complete_e(words, postags, child_dict_list, child_dict['VOB'][0])
                        svos.append([e1, r, e2])

                    # 定语后置，动宾关系
                    relation = arcs[index][0]
                    head = arcs[index][2]
                    if relation == 'ATT':
                        if 'VOB' in child_dict:
                            e1 = self.complete_e(words, postags, child_dict_list, head - 1)
                            r = words[index]
                            e2 = self.complete_e(words, postags, child_dict_list, child_dict['VOB'][0])
                            temp_string = r + e2
                            if temp_string == e1[:len(temp_string)]:
                                e1 = e1[len(temp_string):]
                            if temp_string not in e1:
                                svos.append([e1, r, e2])
                    # 含有介宾关系的主谓动补关系
                    if 'SBV' in child_dict and 'CMP' in child_dict:
                        e1 = self.complete_e(words, postags, child_dict_list, child_dict['SBV'][0])
                        cmp_index = child_dict['CMP'][0]
                        r = words[index] + words[cmp_index]
                        if 'POB' in child_dict_list[cmp_index]:
                            e2 = self.complete_e(words, postags, child_dict_list, child_dict_list[cmp_index]['POB'][0])
                            svos.append([e1, r, e2])
        return svos

    '''对找出的主语或者宾语进行扩展'''
    def complete_e(self, words, postags, child_dict_list, word_index):
        child_dict = child_dict_list[word_index]
        prefix = ''
        if 'ATT' in child_dict:
            for i in range(len(child_dict['ATT'])):
                prefix += self.complete_e(words, postags, child_dict_list, child_dict['ATT'][i])
        postfix = ''
        if postags[word_index] == 'v':
            if 'VOB' in child_dict:
                postfix += self.complete_e(words, postags, child_dict_list, child_dict['VOB'][0])
            if 'SBV' in child_dict:
                prefix = self.complete_e(words, postags, child_dict_list, child_dict['SBV'][0]) + prefix

        return prefix + words[word_index] + postfix

    '''程序主控函数'''
    def triples_main(self, content):
        sentences = self.split_sents(content)
        svos = []
        for sentence in sentences:
            words, postags, child_dict_list, roles_dict, arcs = self.parser.parser_main(sentence)
            svo = self.ruler2(words, postags, child_dict_list, arcs, roles_dict)
            svos += svo

        return svos

def extract_core(content):#输入新闻内容，返回新闻关键事件列表
    extractor = TripleExtractor()
    result = extractor.triples_main(content=content)
    return result
