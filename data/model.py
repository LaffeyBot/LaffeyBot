from flask_sqlalchemy import SQLAlchemy
import quart.flask_patch
import os

basedir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    # 用户名，不可修改，唯一
    username = db.Column(db.VARCHAR(255), nullable=False, unique=True)
    # 显示名，应该与游戏名相符，可修改，不唯一
    nickname = db.Column(db.Text, nullable=False)
    # 身份，0为普通成员，1为管理员，2为会长
    role = db.Column(db.Integer, nullable=False)
    # 密码，hashed using bcrypt
    password = db.Column(db.Text, nullable=False)
    # 创建时间，自动生成
    created_at = db.Column(db.Date, nullable=False)
    # 绑定的邮箱，可空
    email = db.Column(db.Text)
    # 邮箱已验证
    email_verified = db.Column(db.Boolean, nullable=False)
    # 绑定的手机号，可空
    phone = db.Column(db.Text)
    # 手机号已验证
    phone_verified = db.Column(db.Boolean, nullable=False)
    # 在此日期之前的 token 都会失效（比如更改密码时之类的）
    valid_since = db.Column(db.Date, nullable=False)
    # 外键关联Groups
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=True)
    # 查询挂树信息
    hang_on_trees = db.relationship('HangOnTree', backref=db.backref('user'), lazy='dynamic')

    # 查询个人出刀记录
    personal_records = db.relationship('PersonalRecord', backref=db.backref('user'), lazy='dynamic')

    def __repr__(self):
        return '<users %r' % self.id


class Group(db.Model):
    __tablename__ = 'group'
    id = db.Column(db.Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    # 群聊号，可以通过群聊号找到公会，也可以在公会找到群号，会长可修改
    group_chat_id = db.Column(db.Text, nullable=True)
    # 公会名，会长可修改
    name = db.Column(db.Text, nullable=False)
    # 公会介绍，会长/管理员可修改
    description = db.Column(db.Text, nullable=False)
    # 必须申请出刀
    must_request = db.Column(db.Boolean, nullable=False)
    # 会长id区分重名公会
    leader_id = db.Column(db.String(25), nullable=False, unique=True)
    # 查询挂树信息
    hang_on_trees = db.relationship('HangOnTree', backref=db.backref('group'), lazy='dynamic')
    # 查询小组个人出刀记录
    personal_records = db.relationship('PersonalRecord', backref=db.backref('group'), lazy='dynamic')
    # 查询小组成员
    users = db.relationship('User', backref=db.backref('group'), lazy='dynamic')
    # 查询公会排名信息
    team_records = db.relationship('TeamRecord', backref=db.backref('group'), lazy='dynamic')

    def __repr__(self):
        return '<group %r' % self.id


class TeamRecord(db.Model):
    __tablename__ = 'team_record'
    id = db.Column(db.Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    record = db.Column(db.Integer)
    detail_date = db.Column(db.DateTime, nullable=False)
    # 公会代数ID
    epoch_id = db.Column(db.Integer, db.ForeignKey('team_battle_epoch.id'))
    # 对应的 Epoch Object
    # epoch = db.relationship('TeamBattleEpoch', backref=db.backref('team_records', lazy='dynamic'),lazy='dynamic')
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=True)
    # 方便关联查询
    # group = db.relationship('Group', backref=db.backref('team_records', lazy='dynamic'),lazy='dynamic')
    current_boss_gen = db.Column(db.Integer, nullable=False)
    current_boss_order = db.Column(db.Integer, nullable=False)
    boss_remaining_health = db.Column(db.Integer, nullable=False)
    # 最后更新时间
    last_modified = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<team_record %r' % self.id


class DeletionHistory(db.Model):
    __tablename__ = 'deletion_history'
    id = db.Column(db.Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    deleted_date = db.Column(db.DateTime, nullable=False)
    from_table = db.Column(db.Text, nullable=False)
    deleted_id = db.Column(db.Integer, nullable=False)


class TeamBattleEpoch(db.Model):
    __tablename__ = 'team_battle_epoch'
    id = db.Column(db.Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    name = db.Column(db.VARCHAR(255))
    from_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    # 查询多类team_record记录
    team_records = db.relationship('TeamRecord', backref=db.backref('team_battle_epoch'), lazy='dynamic')


class PersonalRecord(db.Model):
    __tablename__ = 'personal_record'
    id = db.Column(db.Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    # 对应的 Group ID
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    # 这是 # 代目
    boss_gen = db.Column(db.Integer, nullable=False)
    # 这是 # 王
    boss_order = db.Column(db.Integer, nullable=False)
    # 伤害
    damage = db.Column(db.Integer, nullable=False)
    # 积分，根据以上信息自动生成
    score = db.Column(db.Integer, nullable=False)
    # 用户ID
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # 游戏名，用于显示
    nickname = db.Column(db.Text, nullable=False)
    # 出刀时间
    detail_date = db.Column(db.DateTime, nullable=False)
    # 出刀类型，normal：普通刀，last：尾刀，compensation：尾刀
    type = db.Column(db.Text, nullable=False)
    # 公会代数ID
    epoch_id = db.Column(db.Integer, db.ForeignKey('team_battle_epoch.id'), nullable=False)
    # 最后更新时间
    last_modified = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<personal_record %r' % self.id


# 存放入会申请和邀请的地方
class RequestsAndInvites(db.Model):
    __tablename__ = 'requests_and_invites'
    id = db.Column(db.Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    # 公会ID
    group_id = db.Column(db.Integer, nullable=False)
    # 玩家ID
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # 类型：request=玩家申请加入某公会，invite=公会管理邀请玩家加入某公会
    type = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<requests_and_invites %r' % self.id


class HangOnTree(db.Model):
    '''记录挂树的信息'''
    __tablename__ = 'hang_on_Tree'
    id = db.Column(db.Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    # 说明信息，可空
    info = db.Column(db.Text, nullable=True)
    # 开始挂树时间信息
    start_time = db.Column(db.DateTime, nullable=False)
    # 状态（是否挂树）
    status = db.Column(db.Boolean, nullable=False)
    # 关联公会
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    # 关联用户
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'{self.id} is hanging on the tree'
