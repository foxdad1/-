# -基于文心一言的学生课程知识问答系统-
使用bootstrap框架搭建静态页面，涉及flask和mysql设计项目，项目拆分成学生端和管理端。
本系统主要专注于为学生提供知识问答服务，通过该系统可以实现课程学习、知识测评、成绩统计等功能，提前发现并解决学生学习中的问题，主要包括如下功能：
1)课程知识问答：基于学生的提问，系统能够理解并提供相应的答案。
2)学习管理：根据学生的问题情况，老师可以深入了解学生对于某课程的薄弱点，有针对性地进行教学。
3)历史问答记录：提供学生历史提问功能，帮助学生巩固学习内容。
4)成绩统计：对学生的课程学习情况进行记录。



# -1.1总体框架
学生课程知识问答系统（P）作为学生（C）和教师（T）之间的知识互动平台。
![image](https://github.com/user-attachments/assets/7784c3e4-aac5-410b-8e23-8a6c17f2ede4)

# -1.2模块描述
资源服务模块主要功能是为学生提供知识问答服务，学生可以通过调用这一层次获取知识问答、历史聊天等资源。
知识问答模块是系统的核心，主要实现以下功能：
基于学生提问提供答案：利用文心一言的自然语言处理能力，理解学生的提问并提供相应的答案。
历史问答：学生可以访问以前的提问和学习记录。
管理模块主要功能是为管理员提供系统管理功能，包括：
课程管理：课程录入和学生选课信息管理。
学生管理：学生信息录入、学生信息修改、学生成绩录入和学生成绩查询。
用户管理：管理员的添加、删除、查询和修改。



# -2.1业务流程说明

![image](https://github.com/user-attachments/assets/bf52b052-c28b-40f6-a755-6ec5cc11a17d)

1) 学生端用户登录后进入index.html页面，可以对GPT进行提问，提问记录会被记录到历史聊天。
2)  学生点击页面左侧边栏可以浏览历史聊天或删除历史记录。
3)  管理端用户登录后进入index.html页面，有课程管理、学生管理、用户管理模块。
4) 课程管理包含课程录入和学生选课信息。
5) 学生管理包括学生信息录入、学生信息修改、学生成绩录入和学生成绩查询。
6) 用户管理包含管理员变动，可以添加、删除、查询、修改管理员。

# -3.1系统说明
# -3.1.1学生端界面
学生端登录后进入index.html页面，可以进行提问，查看和删除历史聊天记录。界面如下所示。

![image](https://github.com/user-attachments/assets/74feb26f-100c-49ce-86b8-1930611daede)


登录后进入index界面，可以在这里将自己的问题输入在下方，点击发送会提交给后端，后端调用文心一言的api进行回答。

![image](https://github.com/user-attachments/assets/ae12f9ca-405f-4ee2-b8b9-b82ed359d5c0)


点击左上角的按钮可以看到登陆的用户历史聊天，点击新聊天会清空聊天并重新加载空白聊天背景，在下方的历史聊天记录的右下角有查看和删除按钮，点击删除会删除该聊天记录。点击查看会显示一个表单，里面时历史问答的详细记录。

![image](https://github.com/user-attachments/assets/202586fc-5dca-4b18-9837-5364054613af)





# -3.1.2 管理端界面

![image](https://github.com/user-attachments/assets/ebea06e2-855b-4dc1-a651-ac569b29bf2c)

管理端登录后进入index.html页面，包含课程管理、学生管理、用户管理三个模块。

![image](https://github.com/user-attachments/assets/d4713b93-c273-4377-9a00-f04547a436a3)

课程管理包含课程录入和学生选课信息。

![image](https://github.com/user-attachments/assets/03db7c13-af10-41e1-b992-fcc24d84e3ac)

课程录入可以让一个老师对应多门课程，当需要录入课程时，在iframe的中间录入基本信息后提交表单可以在下面表格里看到录入信息。
选课信息使用学生学号匹配课程。

![image](https://github.com/user-attachments/assets/8011aee9-7880-4796-b139-143dd296679c)

学生管理包含学生信息录入，学生信息修改，学生成绩录入，学生成绩查询。
学生信息录入可以录入老师班级的学生信息。

![image](https://github.com/user-attachments/assets/5c85fd1f-64fa-40dd-a341-49700654b91c)


学生信息修改可以修改一个学生的学号，班级，姓名。

![image](https://github.com/user-attachments/assets/217ab870-d01c-4ba4-85bb-1bf364fea932)


学生成绩录入可以录入该教师班级学生的成绩，包含一个学生的学号，所选课程号，课程对应的成绩。

![image](https://github.com/user-attachments/assets/0a6755c0-4207-4e7a-a8e2-ae30283d67e0)


学生成绩查询可以根据查询的学生学号/姓名/课程名称/所在班级匹配数据库的学生信息，查询该学生的课程成绩。

![image](https://github.com/user-attachments/assets/be5e9277-4c6c-451b-8bca-e8e7f1facb9d)


用户管理包含管理变动，在这里可以看到所有管理员的信息，并且可以更改管理员的信息。

![image](https://github.com/user-attachments/assets/1a2633a2-6215-46ce-9815-59e87f9c5e85)

