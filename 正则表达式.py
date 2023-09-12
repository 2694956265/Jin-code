import re
s = "python abdf"
s1 ="faosdpfhaodshf[adsf[sdfdfaspfdpopythondkahsfafdaf"
#re.match(匹配规则，想要匹配的字符串) 这是从头开始匹配
result = re.match("python",s)
print(result)
print(result.group())
print(result.span())
result1 = re.search("python",s1)
print(result1)
print(result1.group())
print(result1.span())

result2 = re.findall("s",s1)
print(result2)

stre = "itheima1 @@python2 !!666 ##itcast3"
res=re.findall(r'[\da-f]',stre)
res1=re.findall(r'[\W]',stre)
print(res)
print(res1)

#匹配账号，6-10位 由字母或者数字构成
res2 = re.match(r'^\w{6,10}$',"lijin119")
print(res2.group())
#匹配邮箱{内容}.{内容}@{内容}.{内容}。{内容}.{内容}。{内容}.{内容}
rule = r"^([\w-]+\.?)+@(qq|163|tju\.)(\w*\.?)+$"
s4 = "2694956265@qq.com"
res4 = re.match(rule,s4)
print(res4.group())

#测试
#意思就是说\b就是说\b左右只有一边是字符，另一边不是字符；\B则是左右两边都不是字符
s = "123 !abc"
rule = r'\b123 \B'
print(re.match(rule,s).group())
print(re.search(rule,s).group())
print(re.findall(rule,s))

s ="12356464dfhajhd;of;d"
rules = r'\d{9}'
print(re.match(rules,s))