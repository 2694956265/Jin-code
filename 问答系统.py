
# -*- coding: utf-8 -*-


import re
import importlib,sys
from importlib import reload
# third-party import
from refo import finditer, Predicate, Star, Any
import jieba.posseg as pseg
from jieba import suggest_freq
import jieba
from SPARQLWrapper import SPARQLWrapper, JSON
import io


# import sys
# reload(sys)
#sys.setdefaultencoding("utf-8")
importlib.reload(sys)



# 引入外部字典
# jieba.load_userdict("D:/app/teachers_name.txt")
jieba.load_userdict("E:/2023知识工程实践/teachers_name.txt")

sparql_base = SPARQLWrapper("http://localhost:3030/testds")

# SPARQL config
# SPARQL模板
SPARQL_PREAMBLE = u"""
PREFIX school: <http://kg.course/informations/>
"""

SPARQL_TEM = u"{preamble}\n" + \
             u"SELECT DISTINCT {select} WHERE {{\n" + \
             u"{expression}\n" + \
             u"}}\n"

SPARQL_TEM_count = u"{preamble}\n" + \
                    u"SELECT (COUNT({select}) AS {count}) WHERE {{\n" + \
                    u"{expression}\n" + \
                    u"}}\n"

SPARQL_ASK_TEM = u"{preamble}\n" + \
                u"ASK WHERE{{\n" + \
                u"{expression}\n" + \
                u"}}\n"

INDENT = "    "

class Word(object):
    """treated words as objects"""
    def __init__(self, token, pos):
        self.token = token
        self.pos = pos


class W(Predicate):
    """object-oriented regex for words"""
    def __init__(self, token=".*", pos=".*"):
        self.token = re.compile(token + "$")
        self.pos = re.compile(pos + "$")
        super(W, self).__init__(self.match)

    def match(self, word):
        m1 = self.token.match(word.token)
        m2 = self.pos.match(word.pos)
        return m1 and m2


class Rule(object):
    def __init__(self, condition=None, action=None):
        assert condition and action
        self.condition = condition
        self.action = action

    def apply(self, sentence):
        matches = []
        for m in finditer(self.condition, sentence):
            i, j = m.span()
            matches.extend(sentence[i:j])#将关键词依次放进matches中
        if __name__ == '__main__':
            print("----------applying %s----------" % self.action.__name__)
        return self.action(matches)#将关键词列表给action代表的函数

#某导师类型有哪些老师?
def who_is_master_tutor_question(x):
    select = u"?x0"
    sparql = None
    for w in x:
        if w.token == "硕士生" or w.token == "哪些":
            e = u"?x school:teacher_type school:{type}导师. ?x school:teacher_name ?x0.".format(type = w.token.decode("utf-8").encode("utf-8"))
            sparql = SPARQL_TEM.format(preamble = SPARQL_PREAMBLE, select = select, expression = INDENT + e)
            break
    return sparql

#某导师类型有多少老师?
def how_many_teachers_are_master_tutor_question(x):
    select = u"?teachers"
    count = u"?x0"
    sparql = None
    for w in x:
        if w.token.decode("utf-8") == "硕士生" or w.token.decode("utf-8") == "多少":
            e = u"?teachers school:teacher_type school:{type}导师.".format(type = w.token.decode("utf-8").encode("utf-8"))
            sparql = SPARQL_TEM_count.format(preamble = SPARQL_PREAMBLE, select = select, count = count, expression = INDENT + e)
            break
    return sparql

#某老师主讲了哪些课?
def what_courses_teacher_question(x):
    select = u"?x0"
    sparql = None
    for w in x:
        if w.pos == "nr":
            e = u"school:{person} school:teacher_courses ?x0.".format(person = w.token.decode("utf-8").encode("utf-8"))
            sparql = SPARQL_TEM.format(preamble = SPARQL_PREAMBLE, select = select, expression = INDENT + e)
            break
    return sparql

#某老师主讲了几门课?
def how_many_courses_teacher_question(x):
    select = u"?courses"
    count = u"?x0"
    sparql = None
    for w in x:
        if w.pos == "nr":
            e = u"school:{person} school:teacher_courses ?courses.".format(person = w.token.decode("utf-8").encode("utf-8"))
            sparql = SPARQL_TEM_count.format(preamble = SPARQL_PREAMBLE, select = select, count = count, expression = INDENT + e)
            break
    return sparql

#某老师是博士生导师吗?
def teacher_is_PhD_tutor_question(x):
    sparql = None
    for w in x:
        if w.pos == "nr":
            e = u"school:{person} school:teacher_type school:博士生导师.".format(person = w.token.decode("utf-8").encode("utf-8"))
            sparql = SPARQL_ASK_TEM.format(preamble = SPARQL_PREAMBLE, expression = INDENT + e)
            break
    return sparql

def encode(s):
    return ' '.join([bin(ord(c)).replace('0b', '') for c in s])

if __name__ == "__main__":
    default_questions = [
        u"硕士生导师类型有哪些老师?",
        u"硕士生导师类型有多少老师?",
        u"张小旺老师主讲了哪些课?",
        u"张小旺老师主讲了几门课?",
        u"张小旺老师是博士生导师吗?",
        u"李坤老师主讲了哪些课?",
        u"李坤老师主讲了几门课?",
        u"李坤老师是博士生导师吗?",
        u"毕重科老师主讲了哪些课?",
        u"毕重科老师主讲了几门课?",
        u"毕重科老师是博士生导师吗?",
    ]


    questions = default_questions[0:]

    seg_lists = []

    # tokenizing questions
    for question in questions:
        words = pseg.cut(question)
        seg_list = [Word(word.encode("utf-8"), flag) for word, flag in words]
        seg_lists.append(seg_list)

    # some rules for matching
    # TODO: customize your own rules here
    # 正则匹配关键词设置
    tutor_type_master = (W("硕士生导师") | W("硕导")| W("硕士导师")| W("硕士生"))
    tutor_type_PhD = (W("博士生导师") | W("博导")| W("博士导师")| W("博士生"))
    teacher = (W(pos = "nr") | W(pos = "x"))
    whose = (W("谁") | W("哪些"))
    quantity = (W("多少") | W("几") | W("几门"))
    
    # 正则匹配规则编写
    rules = [

        #某导师类型有哪些老师?
        Rule(condition = tutor_type_master + Star(Any(), greedy = False) + whose, action = who_is_master_tutor_question),

        #某导师类型有多少老师?
        Rule(condition = tutor_type_master + Star(Any(), greedy = False) + quantity, action = how_many_teachers_are_master_tutor_question),

        #某老师主讲了哪些课?
        Rule(condition = teacher + Star(Any(), greedy = False) + whose, action = what_courses_teacher_question),

        #某老师主讲了几门课?
        Rule(condition = teacher + Star(Any(), greedy = False) + quantity, action = how_many_courses_teacher_question),

        #某老师是博士生导师吗?
        Rule(condition = teacher + Star(Any(), greedy = False) + tutor_type_PhD, action = teacher_is_PhD_tutor_question)

    ]

    file_3 = io.open('result.txt', 'w', encoding='UTF-8')

    # matching and querying
    for seg in seg_lists:#提取问题
        # display question each
        question = []
        for s in seg:
            print(s.token)#输出问题，分词后的版本
            question.append(s.token)
        file_3.write(u','.join(question))
        print("123")

        for rule in rules:#提取一个rule
            query = rule.apply(seg)

            if query is None:
                continue
            print(query)
            file_3.write(query + '\n')

            if query:
                sparql_base.setQuery(query)
                sparql_base.setReturnFormat(JSON)
                results = sparql_base.query().convert()

                if "results" in results.keys():
                    if not results["results"]["bindings"]:
                        print( "No answer found :(")
                        print("ddddddd123")
                        continue
                    for result in results["results"]["bindings"]:
                        print("Result: ", result["x0"]["value"])
                        file_3.write("Result: " + result["x0"]["value"] + '\n')
                        print
                else:
                    print("Result: ", results["boolean"])
                    boo = str(results["boolean"])
                    if boo == "True":
                        file_3.write(u"Result: " + "True" + '\n')
                    else:
                        file_3.write(u"Result: " + "False" + '\n')
