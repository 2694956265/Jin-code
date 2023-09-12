# coding: utf-8
# standard import
import re
from refo import finditer, Predicate, Star, Any
import jieba.posseg as pseg
from jieba import suggest_freq
import jieba
from SPARQLWrapper import SPARQLWrapper, JSON
import io

import importlib, sys

importlib.reload(sys)

# 引入外部字典
jieba.load_userdict("E:/2023知识工程实践/teachers_name.txt")
sparql_base = SPARQLWrapper("http://localhost:3030/testds/query")

# SPARQL config
# SPARQL模板
SPARQL_PREAMBLE = u"""
PREFIX kg: <http://kg.course/informations/>
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
        m1 = self.token.match(word.token.decode('utf-8'))  # .decode('utf-8')
        m2 = self.pos.match(word.pos)
        return m1 and m2


class Rule(object):
    def __init__(self, condition=None, action=None):
        assert condition and action
        self.condition = condition
        self.action = action

    def apply(self, sentence):
        matches = []  # #finditer是要返回sentence中所有与self.condition相匹配的全部字串，返回形式为迭代器。 m为其中某个
        for m in finditer(self.condition, sentence):
            i, j = m.span()  # 以tuple的形式返回范围，m在sentence中的范围
            matches.extend(sentence[i:j])  # 将关键词依次放进matches中
        if __name__ == '__main__':
            print("----------applying %s----------" % self.action.__name__)
        return self.action(matches)  # 将关键词列表给action代表的函数
# 老师类型有哪些？   #正确
# def teacher_title_question(x):
#     select = "?x0"
#     sparql = None
#     for w in x:
#         if w.token.decode("utf-8") == "老师" or w.token.decode("utf-8") == "类型":
#             e = "?teacherid school:teacher_title ?x0."
#             sparql = SPARQL_TEM.format(preamble=SPARQL_PREAMBLE, select=select, expression=INDENT + e)
#             break
#     return sparql


# 教授类型有多少老师？   #正确
# def how_many_professor_question(x):
#     select = "?teacher"
#     count = "?x0"
#     sparql = None
#     for w in x:
#         if w.token.decode("utf-8") == "教授" or w.token.decode("utf-8") == "多少":
#             e = "?teacherid school:teacher_title \"教授\". ?teacherid school:teacher_name ?teacher."
#             sparql = SPARQL_TEM_count.format(preamble=SPARQL_PREAMBLE, select=select, count=count,
#                                              expression=INDENT + e)
#             break
#     return sparql


# 某导师类型有哪些老师?  #正确
def who_is_master_tutor_question(x):
    select = "?x0"
    sparql = None
    #print('-----------------------')
    for w in x:
        #print(w.token.decode("utf-8")+'导师')
        if w.token.decode("utf-8") == "硕士生" or w.token.decode("utf-8") == "博士生" or w.token.decode("utf-8") == "哪些":
            e = u"?x0 kg:teacher_type kg:{}".format(w.token.decode("utf-8")+'导师')
            # e = "?x school:teacher_type \"{type}导师\". ?x school:teacher_name ?x0.".format(
            #     type=w.token.decode("utf-8"))
            sparql = SPARQL_TEM.format(preamble=SPARQL_PREAMBLE, select=select, expression=INDENT + e)
           # print(sparql)
            break
    return sparql


# 某导师类型有多少老师?  #正确
# def how_many_teachers_are_master_tutor_question(x):
#     select = "?teachers"
#     count = "?x0"
#     sparql = None
#     for w in x:
#         if w.token.decode("utf-8") == "硕士生" or w.token.decode("utf-8") == "多少":
#             e = "?teachers school:teacher_type \"{type}导师\".".format(type=w.token.decode("utf-8"))
#             sparql = SPARQL_TEM_count.format(preamble=SPARQL_PREAMBLE, select=select, count=count,
#                                              expression=INDENT + e)
#             break
#     return sparql


# 某老师主讲了哪些课?
def what_courses_teacher_question(x):
    select = u"?x0"
    sparql = None
    for w in x:
        if w.pos == "nr" and w.token.decode("utf-8") != "博士生":
            #print("WWWWWW")
            e = u"kg:{} kg:teacher_courses ?x0".format(w.token.decode("utf-8"))
            # e = u"?teacherid school:teacher_name \"{person}\". " \
            #     u"?teacherid school:teacher_course ?x0.".format(person=w.token.decode("utf-8"))
            sparql = SPARQL_TEM.format(preamble=SPARQL_PREAMBLE, select=select, expression=INDENT + e)
            break
    return sparql


# 某老师主讲了几门课?
# def how_many_courses_teacher_question(x):
#     select = u"?courses"
#     count = u"?x0"
#     sparql = None
#     for w in x:
#         if w.pos == "nr":
#             e = u"?teacherid school:teacher_name \"{person}\". " \
#                 u"?teacherid school:teacher_course ?courses.".format(person=w.token.decode("utf-8"))
#             sparql = SPARQL_TEM_count.format(preamble=SPARQL_PREAMBLE, select=select, count=count,
#                                              expression=INDENT + e)
#             break
#     return sparql


# 某老师的研究方向是什么?
def what_direction_teacher_question(x):
    select = u"?x0"
    sparql = None
    for w in x:
        if w.pos == "nr":
            # e = u"?teacherid school:teacher_name \"{person}\". " \
            #     u"?teacherid school:teacher_direction ?x0.".format(person=w.token.decode("utf-8"))
            e = u"kg:{} kg:teacher_direction ?x0".format(w.token.decode("utf-8"))
            sparql = SPARQL_TEM.format(preamble=SPARQL_PREAMBLE, select=select, expression=INDENT + e)
            break
    return sparql


# 某老师是博士生导师吗?
# def teacher_is_PhD_tutor_question(x):
#     sparql = None
#     for w in x:
#         if w.pos == "nr":
#             e = u"?teacherid school:teacher_name \"{person}\". " \
#                 u"?teacherid school:teacher_type \"博导\".".format(person=w.token.decode("utf-8"))
#             sparql = SPARQL_ASK_TEM.format(preamble=SPARQL_PREAMBLE, expression=INDENT + e)
#             break
#     return sparql
# 某老师的导师类型是什么?
def what_type_teacher_question(x):
    select = u"?x0"
    sparql = None
    for w in x:
        if w.pos == "nr":
            # e = u"?teacherid kg:teacher_name \"{person}\". " \
            #     u"?teacherid kg:teacher_homepage ?x0.".format(person=w.token.decode("utf-8"))
            e = u"kg:{} kg:teacher_type ?x0".format(w.token.decode("utf-8"))
            sparql = SPARQL_TEM.format(preamble=SPARQL_PREAMBLE, select=select, expression=INDENT + e)
            break
    return sparql

# 某老师的个人主页是什么?
def what_homepage_teacher_question(x):
    select = u"?x0"
    sparql = None
    for w in x:
        if w.pos == "nr":
            # e = u"?teacherid kg:teacher_name \"{person}\". " \
            #     u"?teacherid kg:teacher_homepage ?x0.".format(person=w.token.decode("utf-8"))
            e = u"kg:{} kg:teacher_webpage ?x0".format(w.token.decode("utf-8"))
            sparql = SPARQL_TEM.format(preamble=SPARQL_PREAMBLE, select=select, expression=INDENT + e)
            break
    return sparql


def encode(s):
    return ' '.join([bin(ord(c)).replace('0b', '') for c in s])


if __name__ == "__main__":
    default_questions = [
        u"毕重科老师主讲了哪些课?",
        u"毕重科老师的导师类型是什么?",
        u"硕士生导师的老师有哪些？",
        u"博士生导师的老师有哪些？",
        u"宫秀军老师的研究方向是什么？",
        u"宫秀军老师的个人主页是什么？"
    ]
    questions = default_questions[0:]
    seg_lists = []
    # tokenizing questions
    for question in questions:
        words = pseg.cut(question)  # 分词 词性标注
        seg_list = [Word(word.encode("utf-8"), flag) for word, flag in words]  # 分词后用Word类初始化，把words看成objects
        seg_lists.append(seg_list)

        # some rules for matching
    # TODO: customize your own rules here
    # 正则匹配关键词设置
    tutor_type_master = (W("硕士生导师") | W("硕导") | W("硕士导师") | W("硕士生"))
    tutor_type_PhD = (W("博士生导师") | W("博导") | W("博士导师") | W("博士生"))
    teacher = (W(pos="nr") | W(pos="x"))
    whose = (W("谁") | W("哪些"))
    quantity = (W("多少") | W("几") | W("几门"))

    institution = (W("学院") | W("职能部门"))
    college = (W(pos="nr"))
    attribute = (W("简介") | W("电话") | W("网址") | W("介绍"))

    teacher_title = (W("老师"))
    class_1 = (W('类型'))
    teacher_title_name = (W("教授"))
    college_1 = (W("智算学部"))
    major = (W('计算机专业') | W('动画专业') | W('软件工程专业'))
    development = (W('培养'))
    work = (W('考研') | W('就业'))

    direction = (W("方向") | W("研究方向"))
    page = (W("个人主页") | W("主页"))

    # 正则匹配规则编写
    rules = [
        # 某老师主讲了哪些课?
        Rule(condition=teacher + Star(Any(), greedy=False) + whose, action=what_courses_teacher_question),
        # 某老师主讲了几门课?
        #Rule(condition=teacher + Star(Any(), greedy=False) + quantity, action=how_many_courses_teacher_question),
        # 某老师的研究方向是什么?
        Rule(condition=teacher + Star(Any(), greedy=False) + direction, action=what_direction_teacher_question),
        # 某老师的导师类型是什么?
        Rule(condition=teacher + Star(Any(), greedy=False) + class_1, action=what_type_teacher_question),
        # 某老师的个人主页是什么?
        Rule(condition=teacher + Star(Any(), greedy=False) + page, action=what_homepage_teacher_question),
        # 硕士生导师类型的老师有哪些
        Rule(condition=tutor_type_master + Star(Any(), greedy=False) + teacher,action=who_is_master_tutor_question),
        # 博士生导师类型的老师有哪些
        Rule(condition=tutor_type_PhD + Star(Any(), greedy=False) + teacher, action=who_is_master_tutor_question)
    ]

    file_3 = open('result.txt', 'w', encoding='UTF-8')

    # matching and querying
    for seg in seg_lists:  # 提取问题
        # display question each
        question = []
        for s in seg:
            print(str(s.token, encoding='utf-8'))  # 输出问题，分词后的版本
            question.append(s.token)

        for q in question:
            file_3.write(str(q, encoding='utf-8'))  # file_3.write(u','.join(question))
        print()

        for rule in rules:  # 提取一个rule
            query = rule.apply(seg)

            if query is None:
                continue
            print(query)
            file_3.write(query + '\n')

            if query:
                sparql_base.setQuery(query)
                sparql_base.setReturnFormat(JSON)
                results = sparql_base.query().convert()
                print(results)

                if "results" in results.keys():
                    if not results["results"]["bindings"]:
                        print("No answer found :(")
                        print('\n')
                        continue
                    for result in results["results"]["bindings"]:
                        print("Result: ", result["x0"]["value"])
                        file_3.write("Result: " + result["x0"]["value"] + '\n')
                        print('\n')
                    file_3.write('\n')  # add
                else:
                    print("Result: ", results["boolean"])
                    boo = str(results["boolean"])
                    if boo == "True":
                        file_3.write(u"Result: " + "True" + '\n')
                    else:
                        file_3.write(u"Result: " + "False" + '\n')

