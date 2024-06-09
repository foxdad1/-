import re  # 引入正则表达式对用户输入进行限制
import flask
import pymysql  # 连接数据库
from flask import request, session
from flask import jsonify
# 初始化
app = flask.Flask(__name__)
# 使用pymysql.connect方法连接本地mysql数据库
db = pymysql.connect(host='localhost', port=3306, user='root',
                     password='123456', database='student', charset='utf8')
# 操作数据库，获取db下的cursor对象
cursor = db.cursor()
# 存储登陆用户的名字用户其它网页的显示
users = []


@app.route("/", methods=["GET", "POST"])
def login():
    # 增加会话保护机制(未登陆前login的session值为空)
    flask.session['login'] = ''
    msg = ''

    if flask.request.method == 'POST':
        user = flask.request.values.get("user", "")
        pwd = flask.request.values.get("pwd", "")

        sql1 = "select * from admins where admin_name=%s and admin_password=%s;"
        cursor.execute(sql1, (user, pwd))
        result = cursor.fetchone()

        # 匹配得到结果即管理员数据库中存在此管理员
        if result:
            # 登陆成功
            flask.session['login'] = 'OK'
            users.append(user)  # 存储登陆成功的用户名用于显示
            return flask.redirect(flask.url_for('index'))
        else:
            # 用户名或密码错误
            msg = '用户名或密码错误'

    return flask.render_template('login.html', msg=msg)


@app.route('/index')
def index():
    # login session值
    if flask.session.get("login", "") == '':
        # 用户没有登陆
        print('用户还没有登陆!即将重定向!')
        return flask.redirect('/')
    insert_result = ''
    # 当用户登陆有存储信息时显示用户名,否则为空
    if users:
        for user in users:
            user_info = user
    else:
        user_info = ''
    # 获取显示管理员数据信息(GET方法的时候显示数据)
    if flask.request.method == 'GET':
        sql_list = "select * from students_infos"
        cursor.execute(sql_list)
        results = cursor.fetchall()
    return flask.render_template('index.html', user_info=user_info, results=results)

@app.route('/student', methods=['GET', 'POST'])
def student():
    # login session值
    if flask.session.get("login", "") == '':
        # 用户没有登陆
        print('用户还没有登陆!即将重定向!')
        return flask.redirect('/')
    insert_result = ''
    # 当用户登陆有存储信息时显示用户名,否则为空
    if users:
        for user in users:
            user_info = user
    else:
        user_info = ''
    # 获取显示管理员数据信息(GET方法的时候显示数据)
    if flask.request.method == 'GET':
        sql_list = "select * from students_infos"
        cursor.execute(sql_list)
        results = cursor.fetchall()
    if flask.request.method == 'POST':
        # 获取输入的学生信息
        student_id = flask.request.values.get("student_id", "")
        student_class = flask.request.values.get("student_class", "")
        student_name = flask.request.values.get("student_name", "")
        student_sex = flask.request.values.get("student_sex", "")

        # 检查输入是否为空
        if not all([student_id, student_class, student_name, student_sex]):
            insert_result = "输入的学生信息不能为空"
        else:
            try:
                # 信息存入数据库
                sql = "create table if not exists students_infos(student_id varchar(10) primary key,student_class varchar(100),student_name varchar(32),student_sex VARCHAR(4));"
                cursor.execute(sql)
                sql_1 = "insert into students_infos(student_id, student_class, student_name, student_sex) values(%s, %s, %s, %s)"
                cursor.execute(sql_1, (student_id, student_class, student_name, student_sex))
                insert_result = "成功存入一条学生信息"
                print(insert_result)
            except Exception as err:
                print(err)
                insert_result = "学生信息插入失败"
                print(insert_result)
                pass
            db.commit()

        # POST方法时显示数据
        sql_list = "select * from students_infos"
        cursor.execute(sql_list)
        results = cursor.fetchall()

    return flask.render_template('student.html', insert_result=insert_result, user_info=user_info, results=results)


@app.route('/teacher_class', methods=['GET', "POST"])
def teacher_class():
    # login session值
    if flask.session.get("login", "") == '':
        # 用户没有登陆
        print('用户还没有登陆!即将重定向!')
        return flask.redirect('/')
    insert_result = ''
    # 当用户登陆有存储信息时显示用户名,否则为空
    if users:
        for user in users:
            user_info = user
    else:
        user_info = ''
    # 获取显示管理员数据信息(GET方法的时候显示数据)
    if flask.request.method == 'GET':
        sql_list = "select * from techer_class_infos"
        cursor.execute(sql_list)
        results = cursor.fetchall()
    if flask.request.method == 'POST':
        # 获取输入的课程信息
        teacher_id = flask.request.values.get("teacher_id", "")
        teacher_class_id1 = flask.request.values.get("teacher_class_id1", "")
        teacher_class_id2 = flask.request.values.get("teacher_class_id2", "")
        teacher_class_id3 = flask.request.values.get("teacher_class_id3")

        print(teacher_id, teacher_class_id1, teacher_class_id2, teacher_class_id3)

        try:
            # 信息存入数据库
            sql = "create table if not exists techer_class_infos(teacher_id varchar(10) primary key,teacher_class_id1 varchar(100),teacher_class_id2 varchar(32),teacher_class_id3 VARCHAR(4));"
            cursor.execute(sql)
            sql_1 = "insert into techer_class_infos(teacher_id, teacher_class_id1, teacher_class_id2, teacher_class_id3 )values(%s,%s,%s,%s)"
            cursor.execute(sql_1, (teacher_id, teacher_class_id1, teacher_class_id2, teacher_class_id3))
            # result = cursor.fetchone()
            insert_result = "成功存入一条信息"
            print(insert_result)
        except Exception as err:
            print(err)
            insert_result = "信息插入失败"
            print(insert_result)
            pass
        db.commit()
        # POST方法时显示数据
        sql_list = "select * from techer_class_infos"
        cursor.execute(sql_list)
        results = cursor.fetchall()
    return flask.render_template('teacher_class.html', insert_result=insert_result, user_info=user_info,
                                 results=results)


@app.route('/teacher', methods=['GET', "POST"])
def teacher():
    # login session值
    if flask.session.get("login", "") == '':
        # 用户没有登陆
        print('用户还没有登陆!即将重定向!')
        return flask.redirect('/')
    insert_result = ''
    # 当用户登陆有存储信息时显示用户名,否则为空
    if users:
        for user in users:
            user_info = user
    else:
        user_info = ''
    # 获取显示管理员数据信息(GET方法的时候显示数据)
    if flask.request.method == 'GET':
        sql_list = "select * from students_decision_infos"
        cursor.execute(sql_list)
        results = cursor.fetchall()
    if flask.request.method == 'POST':
        # 获取输入的学生选课信息
        student_id = flask.request.values.get("student_id", "")
        student_class_id = flask.request.values.get("student_class_id", "")
        student_class_id2 = flask.request.values.get("student_class_id2", "")
        student_class_id3 = flask.request.values.get("student_class_id3", "")

        print(student_id, student_class_id, student_class_id2, student_class_id3)
        try:
            # 信息存入数据库
            sql = "create table if not exists students_decision_infos(student_id varchar(15) primary key,student_class_id varchar(20),student_class_id2 varchar(15),student_class_id3 varchar(15),foreign key(student_id) references students_infos(student_id));"
            cursor.execute(sql)
            sql_1 = "insert into students_decision_infos(student_id, student_class_id, student_class_id2, student_class_id3)values(%s,%s,%s,%s)"
            cursor.execute(sql_1, (student_id, student_class_id, student_class_id2, student_class_id3))
            # result = cursor.fetchone()
            insert_result = "成功存入一条选课信息"
            print(insert_result)
        except Exception as err:
            print(err)
            insert_result = "选课信息插入失败"
            print(insert_result)
            pass
        db.commit()
        # POST显示数据
        sql_list = "select * from students_decision_infos"
        cursor.execute(sql_list)
        results = cursor.fetchall()
    return flask.render_template('teacher.html', insert_result=insert_result, user_info=user_info, results=results)


@app.route('/grade', methods=['GET', "POST"])
def grade():
    # login session值
    if flask.session.get("login", "") == '':
        # 用户没有登陆
        print('用户还没有登陆!即将重定向!')
        return flask.redirect('/')
    insert_result = ''
    # 当用户登陆有存储信息时显示用户名,否则为空
    if users:
        for user in users:
            user_info = user
    else:
        user_info = ''
    # 获取显示管理员数据信息(GET方法的时候显示数据)
    if flask.request.method == 'GET':
        sql_list = "select * from grade_infos"
        cursor.execute(sql_list)
        results = cursor.fetchall()
    if flask.request.method == 'POST':
        # 获取输入的学生成绩信息
        student_id = flask.request.values.get("student_id", "")
        student_class_id = flask.request.values.get("student_class_id", "")
        grade = flask.request.values.get("grade", "")
        print(student_id, student_class_id, grade)
        # 信息存入数据库
        try:
            sql = "create table if not exists grade_infos(student_id varchar(15) primary key,student_class_id varchar(20),grade tinyint unsigned,foreign key(student_id) references students_decision_infos(student_id));"
            cursor.execute(sql)
            sql_1 = "insert into grade_infos(student_id, student_class_id,grade)values(%s,%s,%s)"
            cursor.execute(sql_1, (student_id, student_class_id, grade))
            insert_result = "成功存入一条学生成绩信息"
            print(insert_result)
        except Exception as err:
            print(err)
            insert_result = "学生成绩信息插入失败"
            print(insert_result)
            pass
        db.commit()
        # POST获取数据
        sql_list = "select * from grade_infos"
        cursor.execute(sql_list)
        results = cursor.fetchall()
    return flask.render_template('grade.html', insert_result=insert_result, user_info=user_info, results=results)

@app.route('/grade_infos', methods=['GET', 'POST'])
def grade_infos():
    # login session值
    if flask.session.get("login", "") == '':
        # 用户没有登陆
        print('用户还没有登陆!即将重定向!')
        return flask.redirect('/')
    query_result = ''
    results = ''
    # 当用户登陆有存储信息时显示用户名,否则为空
    if users:
        for user in users:
            user_info = user
    else:
        user_info = ''
    # 获取下拉框的数据
    if flask.request.method == 'POST':
        select = flask.request.form.get('selected_one')
        query = flask.request.values.get('query')
        print(select, query)
        # 判断不同输入对数据表进行不同的处理
        if select == '学号':
            try:
                sql = "select * from grade_infos where student_id = %s; "
                cursor.execute(sql, query)
                results = cursor.fetchall()
                if results:
                    query_result = '查询成功!'
                else:
                    query_result = '查询失败!'
            except Exception as err:
                print(err)
                pass
        if select == '姓名':
            try:
                sql = "select * from grade_infos where student_id in(select student_id from students_infos where student_name=%s);"
                cursor.execute(sql, query)
                results = cursor.fetchall()
                if results:
                    query_result = '查询成功!'
                else:
                    query_result = '查询失败!'
            except Exception as err:
                print(err)
                pass

        if select == '课程名称':
            try:
                sql = "select * from grade_infos where student_class_id in(select student_class_id from students_infos where student_class_id=%s);"
                cursor.execute(sql, query)
                results = cursor.fetchall()
                if results:
                    query_result = '查询成功!'
                else:
                    query_result = '查询失败!'
            except Exception as err:
                print(err)
                pass

        if select == "所在班级":
            try:
                sql = "select * from grade_infos where student_class_id in(select student_class_id from students_infos where student_class=%s);"
                cursor.execute(sql, query)
                results = cursor.fetchall()
                if results:
                    query_result = '查询成功!'
                else:
                    query_result = '查询失败!'
            except Exception as err:
                print(err)
                pass
    return flask.render_template('grade_infos.html', query_result=query_result, user_info=user_info, results=results)


@app.route('/administrator', methods=['GET', 'POST'])
def administrator():
    if flask.session.get("login", "") == '':
        return flask.redirect('/')

    insert_result = ''
    user_info = session.get('user_info', '')

    if request.method == 'POST':
        action = request.form.get("action", "")
        admin_name = request.form.get("admin_name", "")
        admin_password = request.form.get("admin_password", "")

        try:
            if action == 'add':
                sql = "INSERT INTO admins (admin_name, admin_password) VALUES (%s, %s)"
                cursor.execute(sql, (admin_name, admin_password))
                insert_result = "成功增加了一名管理员"
            elif action == 'update':
                sql = "UPDATE admins SET admin_password=%s WHERE admin_name=%s;"
                cursor.execute(sql, (admin_password, admin_name))
                insert_result = "管理员" + admin_name + "的密码修改成功!"
            elif action == 'delete':
                selected_admins = request.form.getlist('selected_admins')
                for admin in selected_admins:
                    sql_delete = "DELETE FROM admins WHERE admin_name=%s;"
                    cursor.execute(sql_delete, (admin,))
                insert_result = "成功删除选中的管理员"
            elif action == 'search':
                admin_name = request.form.get('admin_name', '')
                sql_query = "SELECT * FROM admins WHERE admin_name LIKE %s"
                cursor.execute(sql_query, ('%' + admin_name + '%',))
                results = cursor.fetchall()
                return jsonify({"insert_result": insert_result, "results": results})
            db.commit()
        except Exception as err:
            print(err)
            insert_result = "操作失败"
            db.rollback()

    # 获取所有管理员数据
    sql_list = "SELECT * FROM admins"
    cursor.execute(sql_list)
    results = cursor.fetchall()

    return flask.render_template('administrator.html', user_info=user_info, insert_result=insert_result, results=results)

@app.route('/update_student', methods=['GET', "POST"])
def update_student():
    # login session值
    if flask.session.get("login", "") == '':
        # 用户没有登陆
        print('用户还没有登陆!即将重定向!')
        return flask.redirect('/')
    insert_result = ''

    # 获取显示学生数据信息(GET方法的时候显示数据)
    if flask.request.method == 'GET':
        sql_list = "select * from students_infos"
        cursor.execute(sql_list)
        results = cursor.fetchall()

    # 当用户登陆有存储信息时显示用户名,否则为空
    if users:
        for user in users:
            user_info = user
    else:
        user_info = ''
    if flask.request.method == 'POST':
        # 获取输入的学生信息
        student_id = flask.request.values.get("student_id", "")
        student_class = flask.request.values.get("student_class", "")
        student_name = flask.request.values.get("student_name", "")
        student_id_result = re.search(r"^\d{8,}$", student_id)  # 限制用户名为全字母
        if student_id_result != None:  # 验证通过
            # 获取下拉框的数据
            select = flask.request.form.get('selected_one')
            if select == '修改学生班级':
                try:
                    sql = "update students_infos set student_class=%s where student_id=%s;"
                    cursor.execute(sql, (student_class, student_id))
                    insert_result = "学生" + student_id + "的班级修改成功!"
                except Exception as err:
                    print(err)
                    insert_result = "修改学生班级失败!"
                    pass
                db.commit()

            if select == '修改学生姓名':
                try:
                    sql = "update students_infos set student_name=%s where student_id=%s;"
                    cursor.execute(sql, (student_name, student_id))
                    insert_result = "学生" + student_name + "的姓名修改成功!"
                except Exception as err:
                    print(err)
                    insert_result = "修改学生姓名失败!"
                    pass
                db.commit()

            if select == '删除学生':
                try:
                    sql_delete = "DELETE FROM students_infos where student_id='" + student_id + "';"
                    cursor.execute(sql_delete, student_id)
                    insert_result = "成功删除学生" + student_id
                except Exception as err:
                    print(err)
                    insert_result = "删除失败"
                db.commit()

        else:  # 输入验证不通过
            insert_result = "输入的格式不符合要求!"
        # POST方法时显示数据
        sql_list = "select * from students_infos"
        cursor.execute(sql_list)
        results = cursor.fetchall()
    return flask.render_template('update_student.html', user_info=user_info, insert_result=insert_result,
                                 results=results)



# 启动服务器
app.debug = True
# 增加session会话保护(任意字符串,用来对session进行加密)
app.secret_key = 'carson'
try:
    app.run()
except Exception as err:
    print(err)
    db.close()  # 关闭数据库连接
