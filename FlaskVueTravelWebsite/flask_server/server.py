from flask import *
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa
import json
import logging

logging.basicConfig(filename='log.log', level=logging.INFO)
app = Flask(__name__)
app.secret_key = '84375r0hfuggwkjvgfjhvsjhgv'

# 数据库连接
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/travel'
# 动态追踪修改设置，如未设置只会提示警告
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# 查询时会显示原始SQL语句
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100), nullable=False, unique=True)
    pwd = db.Column(db.String(128), nullable=False)


class Member(db.Model):
    __tablename__ = 'member'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100), nullable=False, unique=True)
    pwd = db.Column(db.String(128), nullable=False)

    # def __init__(self, user, pwd):
    #     self.user = user
    #     self.pwd = pwd


class Place(db.Model):
    __tablename__ = 'place'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    place = db.Column(db.String(128), nullable=False)

    def __init__(self, name, place):
        self.name = name
        self.place = place


class Classify(db.Model):
    __tablename__ = 'classify'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    classify = db.Column(db.String(128), nullable=False)
    img_path = db.Column(db.String(1024), nullable=False)
    place = db.Column(db.Integer, sa.ForeignKey("place.id"), nullable=False)
    describe = db.Column(db.Text, nullable=False)

    def __init__(self, name, classify, place, img_path="", describe=''):
        self.name = name
        self.classify = classify
        self.place = place
        self.img_path = img_path
        self.describe = describe


class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    classify = db.Column(db.Integer, sa.ForeignKey("classify.id"), nullable=False)

    def __init__(self, title, content, classify):
        self.title = title
        self.content = content
        self.classify = classify


class Mark(db.Model):
    __tablename__ = 'mark'
    id = db.Column(db.Integer, primary_key=True)
    member = db.Column(db.Integer, sa.ForeignKey("member.id"), nullable=False)
    classify = db.Column(db.Integer, sa.ForeignKey("classify.id"), nullable=False)

    def __init__(self, member, classify):
        self.member = member
        self.classify = classify
        super(Mark, self).__init__()


# -------------------------------------------
# This is the index route where we are going to
# query on all our employee dat
# @app.route('/')
# def Index():
#     all_data = Data.query.all()

#     return render_template("index.html", employees = all_data)


@app.route('/init')
def init():
    db.create_all()
    return 'ok'


@app.route('/admin/register', methods=['GET', 'POST'])
def index_a():
    if request.method == 'POST':
        form = request.get_json()
        user = form.get('user')
        pwd1 = form.get('pwd')
        current = Admin.query.filter(Admin.user == user).first()
        if (current):
            return jsonify({"msg": "用户名已存在"}), 400
        # pwd2 = form.get('pwd2')
        a = Admin()
        a.user = user
        a.pwd = pwd1
        db.session.add(a)
        db.session.commit()
        flash('注册成功')
    return jsonify({"token": user})


# request 从请求里读内容


@app.route('/admin/login', methods=['GET', 'POST'])
def login_a():
    if request.method == 'POST':
        form = request.get_json()
        user = form.get('user')
        pwd = form.get('pwd')
        admin = {}
        if all([user, pwd]):
            a = Admin.query.filter(Admin.user == user).first()
            if a:
                # 如果用户存在，判断密码是否正确
                admin = a.__dict__
                admin.pop('_sa_instance_state', None)
                if a.pwd == pwd:
                    return jsonify({"token": user, "data": admin})
                else:
                    flash('密码错误')
            else:
                flash('用户名不存在')
        else:
            flash('用户名、密码不完整')
    return jsonify({"token": user, "data": admin}), 400


@app.route('/member/register', methods=['GET', 'POST'])
def index_m():
    if request.method == 'POST':
        form = request.get_json()
        user = form.get('user')
        pwd1 = form.get('pwd')
        # pwd2 = form.get('pwd2')
        current = Member.query.filter(Member.user == user).first()
        if (current):
            return jsonify({"msg": "用户名已存在"}), 400
        a = Member()
        a.user = user
        a.pwd = pwd1
        db.session.add(a)
        db.session.commit()

    return jsonify({"token": user})


# request 从请求里读内容


@app.route('/member/login', methods=['GET', 'POST'])
def login_m():
    if request.method == 'POST':
        form = request.get_json()
        print(form)
        user = form.get('user')
        pwd = form.get('pwd')
        member = {}
        if all([user, pwd]):
            a = Member.query.filter(Member.user == user).first()
            if a:
                # 如果用户存在，判断密码是否正确
                # member = a
                # print(member.id)
                member = a.__dict__
                member.pop('_sa_instance_state', None)
                print(member)
                if a.pwd == pwd:
                    # 登录成功后，session['admin_id']存入数据，
                    # 其他页面用来判断用户到登录状态
                    # session['member_id'] = a.id

                    return jsonify({"token": user, "data": member})
                else:
                    return jsonify(400), 401
            else:
                return jsonify({"message": "请先注册"}), 402
        else:
            return jsonify(400), 403
    return jsonify({"token": user, "data": member}), 404


# ----------------------------------------------------------------


@app.route('/member')
def ind_m():
    return 'ok'


@app.route('/member/list', methods=['GET', 'POST'])
def list_m():
    all_data = Member.query.all()
    result = []
    for data in all_data:
        data_dict = data.__dict__
        data_dict.pop('_sa_instance_state', None)
        result.append(data_dict)
    return jsonify(result)


@app.route('/member/<id>', methods=['GET', 'POST'])
def q_m(id):
    data = Member.query.get(id)
    data_dict = data.__dict__
    data_dict.pop('_sa_instance_state', None)
    return jsonify(data_dict)


# this route is for inserting data to mysql database via html forms
@app.route('/member/create', methods=['POST'])
def insert_m():
    if request.method == 'POST':
        form = request.get_json()
        user = form['user']
        pwd = form['pwd']

        my_data = Member(user, pwd)
        db.session.add(my_data)
        db.session.commit()

        # flash("Employee Inserted Successfully")
        print("place add successfull")
        return jsonify(200)


# this is our update route where we are going to update our employee
@app.route('/member/update', methods=['GET', 'POST'])
def update_m():
    if request.method == 'POST':
        form = request.get_json()
        my_data = Member.query.get(form.get('id'))
        my_data.user = form['user']
        my_data.pwd = form['pwd']
        db.session.commit()

        return jsonify(200)


# This route is for deleting our employee
@app.route('/member/delete/<id>', methods=['GET', 'POST'])
def delete_m(id):
    my_data = Member.query.get(id)
    db.session.delete(my_data)
    db.session.commit()

    return jsonify(200)


# ----------------------------------------------------------------


@app.route('/user')
def ind():
    return 'ok'


@app.route('/place/list', methods=['GET', 'POST'])
def list_p():
    all_data = Place.query.all()
    result = []
    for data in all_data:
        data_dict = data.__dict__
        data_dict.pop('_sa_instance_state', None)
        result.append(data_dict)
    return jsonify(result)


@app.route('/place/<id>', methods=['GET', 'POST'])
def q_p(id):
    data = Place.query.get(id)
    data_dict = data.__dict__
    data_dict.pop('_sa_instance_state', None)
    return jsonify(data_dict)


# this route is for inserting data to mysql database via html forms
@app.route('/place/create', methods=['POST'])
def insert_p():
    if request.method == 'POST':
        form = request.get_json()
        name = form['name']
        place = form['place']

        my_data = Place(name, place)
        db.session.add(my_data)
        db.session.commit()

        # flash("Employee Inserted Successfully")
        print("place add successfull")
        return jsonify(200)


# this is our update route where we are going to update our employee
@app.route('/place/update', methods=['GET', 'POST'])
def update_p():
    if request.method == 'POST':
        form = request.get_json()
        print('nnnnnnnnnnnnnnnnnn', form, type(form))
        my_data = Place.query.get(form.get('id'))
        my_data.name = form['name']
        my_data.place = form['place']
        db.session.commit()

        return jsonify(200)


# This route is for deleting our employee
@app.route('/place/delete/<id>', methods=['GET', 'POST'])
def delete_p(id):
    my_data = Place.query.get(id)
    db.session.delete(my_data)
    db.session.commit()

    return jsonify(200)


# # ----------------------------------------------------------------
# id = db.Column(db.Integer, primary_key = True)
# title = db.Column(db.String(100), nullable=False)
# content = db.Column(db.String(128), nullable=False)
# classify = db.Column(db.Integer, sa.ForeignKey("Classify.id"), nullable=False)
# this route is for inserting data to mysql database via html forms

@app.route('/article/list', methods=['GET', 'POST'])
def list_a():
    all_data = Article.query.all()
    result = []
    for data in all_data:
        data_dict = data.__dict__
        data_dict.pop('_sa_instance_state', None)
        result.append(data_dict)
    return jsonify(result)


@app.route('/article/<id>', methods=['GET', 'POST'])
def q_a(id):
    data = Article.query.get(id)
    data_dict = data.__dict__
    data_dict.pop('_sa_instance_state', None)
    return jsonify(data_dict)


@app.route('/article/article_by_classify/<id>', methods=['GET', 'POST'])
def qbyc_a(id):
    all_data = Article.query.filter(Article.classify == int(id))
    result = []
    for data in all_data:
        data_dict = data.__dict__
        data_dict.pop('_sa_instance_state', None)
        result.append(data_dict)

    return jsonify(result)


@app.route('/article/create', methods=['POST'])
def insert_a():
    if request.method == 'POST':
        form = request.get_json()
        title = form['title']
        content = form['content']
        classify = form['classify']

        my_data = Article(title, content, classify)
        db.session.add(my_data)
        db.session.commit()

        # flash("Employee Inserted Successfully")
        # print("place add successfull")
        return jsonify(200)


# this is our update route where we are going to update our employee
@app.route('/article/update', methods=['GET', 'POST'])
def update_a():
    if request.method == 'POST':
        form = request.get_json()
        my_data = Article.query.get(form.get('id'))
        my_data.title = form['title']
        my_data.content = form['content']
        my_data.classify = form['classify']
        db.session.commit()

        return jsonify(200)


# This route is for deleting our employee
@app.route('/article/delete/<id>', methods=['GET', 'POST'])
def delete_a(id):
    my_data = Article.query.get(id)
    db.session.delete(my_data)
    db.session.commit()

    return jsonify(200)


# # ----------------------------------------------------------------
#     name = db.Column(db.String(100), nullable=False)
#     classify = db.Column(db.String(128), nullable=False)
#     img_path = db.Column(db.String(1024), nullable=False)
#     place = db.Column(db.Integer,  sa.ForeignKey("place.id"), nullable=False)
# this route is for inserting data to mysql database via html forms

@app.route('/classify/list', methods=['GET', 'POST'])
def list_c():
    all_data = Classify.query.all()
    result = []
    for data in all_data:
        data_dict = data.__dict__
        data_dict.pop('_sa_instance_state', None)
        result.append(data_dict)
    return jsonify(result)


@app.route('/classify/<id>', methods=['GET', 'POST'])
def q_c(id):
    data = Classify.query.get(id)
    data_dict = data.__dict__
    data_dict.pop('_sa_instance_state', None)
    return jsonify(data_dict)


@app.route('/classify/classify_by_member/<id>', methods=['GET', 'POST'])
def qbym_c(id):
    all_data = Mark.query.filter(Mark.member == id)
    classify_ids = []
    for data in all_data:
        data_dict = data.__dict__
        classify_ids.append(data_dict['classify'])
    all_class = Classify.query.filter(Classify.id.in_(classify_ids))

    result = []
    for data in all_class:
        data_dict = data.__dict__
        data_dict.pop('_sa_instance_state', None)
        result.append(data_dict)
    return jsonify(result)


@app.route('/classify/classify_by_place/<id>', methods=['GET', 'POST'])
def qbp_c(id):
    all_data = Classify.query.filter(Classify.place == id)
    result = []
    for data in all_data:
        data_dict = data.__dict__
        data_dict.pop('_sa_instance_state', None)
        result.append(data_dict)

    return jsonify(result)


@app.route('/classify/create', methods=['POST'])
def insert_c():
    if request.method == 'POST':
        form = request.get_json()
        name = form['name']
        classify = form['classify']
        img_path = form['img_path']
        place = int(form['place'])

        my_data = Classify(name, classify, place, img_path)
        db.session.add(my_data)
        db.session.commit()

        return jsonify(200)


# this is our update route where we are going to update our employee
@app.route('/classify/update', methods=['GET', 'POST'])
def update_c():
    if request.method == 'POST':
        form = request.get_json()
        my_data = Classify.query.get(form.get('id'))
        my_data.name = form['name']
        my_data.classify = form['classify']
        my_data.img_path = form['img_path']
        my_data.place = int(form['place'])
        db.session.commit()

        return jsonify(200)


# This route is for deleting our employee
@app.route('/classify/delete/<id>', methods=['GET', 'POST'])
def delete_c(id):
    my_data = Classify.query.get(id)

    db.session.delete(my_data)
    db.session.commit()

    return jsonify(200)


# ---------------------------------

@app.route('/mark/create', methods=['POST'])
def insert_mark():
    if request.method == 'POST':
        form = request.get_json()
        name = form['id']
        classify = form['classify']

        my_data = Mark(name, classify)
        db.session.add(my_data)
        db.session.commit()

        return jsonify(200)


@app.route('/mark/delete/<classify_id>', methods=['POST'])
def delete_mark(classify_id):
    form = request.get_json()
    member_id = form['id']
    print(classify_id)
    # and_ = sa.and_(Mark.member == member_id, Mark.classify == int(classify_id))
    # mark = Mark(member_id, classify_id)
    my_data = Mark.query.filter(Mark.member == member_id).filter(Mark.classify == int(classify_id)).first()
    db.session.delete(my_data)
    db.session.commit()

    return jsonify(200)


if __name__ == '__main__':
    app.run(debug=True)
