import io
import sys
import random

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='UTF-8') # 设定输出编码
file_1 = open('智算学部部分信息.txt', encoding='UTF-8')
file_2 = open('teachers_information.nt', 'w', encoding='UTF-8')
file_3 = open('teachers_name.txt', 'w', encoding='UTF-8')

# 定义三元组模板
teacher_name = "<http://kg.course/informations/%s> <http://kg.course/informations/teacher_name> \"%s\" ."

teacher_professional_title = "<http://kg.course/informations/%s> <http://kg.course/informations/teacher_professional_title> <http://kg.course/informations/%s> ."
professional_title_name = "<http://kg.course/informations/%s> <http://kg.course/informations/professional_title_name> \"%s\" ."

teacher_department = "<http://kg.course/informations/%s> <http://kg.course/informations/teacher_department> <http://kg.course/informations/%s> ."
department_name = "<http://kg.course/informations/%s> <http://kg.course/informations/department_name> \"%s\" ."

teacher_courses = "<http://kg.course/informations/%s> <http://kg.course/informations/teacher_courses> <http://kg.course/informations/%s> ."
courses_name = "<http://kg.course/informations/%s> <http://kg.course/informations/courses_name> \"%s\" ."

teacher_type = "<http://kg.course/informations/%s> <http://kg.course/informations/teacher_type> <http://kg.course/informations/%s> ."
type_name = "<http://kg.course/informations/%s> <http://kg.course/informations/type_name> \"%s\" ."

teacher_email = "<http://kg.course/informations/%s> <http://kg.course/informations/teacher_email> <http://kg.course/informations/%s> ."
email_name = "<http://kg.course/informations/%s> <http://kg.course/informations/email_name> \"%s\" ."

teacher_field = "<http://kg.course/informations/%s> <http://kg.course/informations/teacher_field> <http://kg.course/informations/%s> ."
field_name = "<http://kg.course/informations/%s> <http://kg.course/informations/field_name> \"%s\" ."

teacher_direction = "<http://kg.course/informations/%s> <http://kg.course/informations/teacher_direction> <http://kg.course/informations/%s> ."
direction_name = "<http://kg.course/informations/%s> <http://kg.course/informations/direction_name> \"%s\" ."

teacher_webpage = "<http://kg.course/informations/%s> <http://kg.course/informations/teacher_webpage> <http://kg.course/informations/%s> ."
webpage_name = "<http://kg.course/informations/%s> <http://kg.course/informations/webpage_name> \"%s\" ."

triples = []

for line in file_1:
	list_teacher = line.strip().split(' ') # 将每行数据解析为一个字典，每行字段之间用空格分隔
	dict_teacher = {}
	for list_elm in list_teacher:
		list_to_dict = []
		list_to_dict = list_elm.split('：')
		char = '；'
		if char in list_to_dict[1]:
			subvalue = list_to_dict[1].split('；') # 如果字段值包含分号，拆分为列表
			dict_teacher[list_to_dict[0]] = subvalue
		else:
			dict_teacher[list_to_dict[0]] = [list_to_dict[1]]
	print(dict_teacher)
	file_3.write(dict_teacher['姓名'][0] + ' ' + 'nr'+'\n') # 将教师姓名写入外部字典
	file_3.flush()

	# 构建三元组
	teacher_name_str = teacher_name % (dict_teacher['姓名'][0], dict_teacher['姓名'][0])
	triples.append(teacher_name_str)

	teacher_professional_title_str = teacher_professional_title % (dict_teacher['姓名'][0], dict_teacher['职称'][0])
	professional_title_name_str = professional_title_name % (dict_teacher['职称'][0], dict_teacher['职称'][0])
	triples.append(teacher_professional_title_str)
	triples.append(professional_title_name_str)

	teacher_department_str = teacher_department % (dict_teacher['姓名'][0], dict_teacher['所在系别'][0])
	department_name_str = department_name % (dict_teacher['所在系别'][0], dict_teacher['所在系别'][0])
	triples.append(teacher_department_str)
	triples.append(department_name_str)

	if (len(dict_teacher['主讲课程']) > 1):
		for num_1 in range(len(dict_teacher['主讲课程'])):
			teacher_courses_str = teacher_courses % (dict_teacher['姓名'][0], dict_teacher['主讲课程'][num_1])
			courses_name_str = courses_name % (dict_teacher['主讲课程'][num_1], dict_teacher['主讲课程'][num_1])
			triples.append(teacher_courses_str)
			triples.append(courses_name_str)

	if (len(dict_teacher['主讲课程']) == 1):
		teacher_courses_str = teacher_courses % (dict_teacher['姓名'][0], dict_teacher['主讲课程'][0])
		courses_name_str = courses_name % (dict_teacher['主讲课程'][0], dict_teacher['主讲课程'][0])
		triples.append(teacher_courses_str)
		triples.append(courses_name_str)

	if (len(dict_teacher['导师类型']) > 1):
		for num_2 in range(len(dict_teacher['导师类型'])):
			teacher_type_str = teacher_type % (dict_teacher['姓名'][0], dict_teacher['导师类型'][num_2])
			type_name_str = type_name % (dict_teacher['导师类型'][num_2], dict_teacher['导师类型'][num_2])
			triples.append(teacher_type_str)
			triples.append(type_name_str)

	if (len(dict_teacher['导师类型']) == 1):
		teacher_type_str = teacher_type % (dict_teacher['姓名'][0], dict_teacher['导师类型'][0])
		type_name_str = type_name % (dict_teacher['导师类型'][0], dict_teacher['导师类型'][0])
		triples.append(teacher_type_str)
		triples.append(type_name_str)

	teacher_email_str = teacher_email % (dict_teacher['姓名'][0], dict_teacher['电子邮件'][0])
	email_name_str = email_name % (dict_teacher['电子邮件'][0], dict_teacher['电子邮件'][0])
	triples.append(teacher_email_str)
	triples.append(email_name_str)

	teacher_field_str = teacher_field % (dict_teacher['姓名'][0], dict_teacher['研究领域'][0])
	field_name_str = field_name % (dict_teacher['研究领域'][0], dict_teacher['研究领域'][0])
	triples.append(teacher_field_str)
	triples.append(field_name_str)

	teacher_direction_str = teacher_direction % (dict_teacher['姓名'][0], dict_teacher['研究方向'][0])
	direction_name_str = direction_name % (dict_teacher['研究方向'][0], dict_teacher['研究方向'][0])
	triples.append(teacher_direction_str)
	triples.append(direction_name_str)

	teacher_webpage_str = teacher_webpage % (dict_teacher['姓名'][0], dict_teacher['个人主页'][0])
	webpage_name_str = webpage_name % (dict_teacher['个人主页'][0], dict_teacher['个人主页'][0])
	triples.append(teacher_webpage_str)
	triples.append(webpage_name_str)

	file_2.write("\n".join(triples)) # 写入nt文件
