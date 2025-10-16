"""
ユーザーモデル
"""
from app.extensions import db


class User(db.Model):
    """ユーザー情報テーブル"""
    __tablename__ = 'USER'

    USER_NO = db.Column(db.String(8), primary_key=True, nullable=False)
    EMAIL = db.Column(db.String(50), nullable=False, unique=True)
    PW = db.Column(db.String(255), nullable=False)
    COUNTRY_Code = db.Column(db.String(3), nullable=False)
    PASSPORTEXPIRY = db.Column(db.Date)
    LANGUAGE_NO = db.Column(db.String(10), nullable=False)

    @staticmethod
    def generate_user_no():
        """ユーザー番号を自動生成"""
        count = db.session.query(db.func.count(User.USER_NO)).scalar()
        next_id = count + 1
        return f'U{next_id:07d}'  # U0000001 の形式で返す

    def to_dict(self):
        """辞書形式に変換"""
        return {
            'user_no': self.USER_NO,
            'email': self.EMAIL,
            'country_code': self.COUNTRY_Code,
            'passport_expiry': self.PASSPORTEXPIRY.isoformat() if self.PASSPORTEXPIRY else None,
            'language_no': self.LANGUAGE_NO
        }
