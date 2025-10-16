"""
国・都市モデル
"""
from app.extensions import db


class Country(db.Model):
    """国情報テーブル"""
    __tablename__ = 'country'

    Code = db.Column(db.String(3), primary_key=True)
    Name = db.Column(db.String(52), nullable=False)
    Continent = db.Column(
        db.Enum('Asia', 'Europe', 'North America', 'Africa',
                'Oceania', 'Antarctica', 'South America'),
        nullable=False
    )

    # リレーションシップ
    cities = db.relationship('City', backref='country', lazy=True)

    def to_dict(self):
        """辞書形式に変換"""
        return {
            'code': self.Code,
            'name': self.Name,
            'continent': self.Continent
        }


class City(db.Model):
    """都市情報テーブル"""
    __tablename__ = 'city'

    ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(35), nullable=False)
    CountryCode = db.Column(
        db.String(3),
        db.ForeignKey('country.Code'),
        nullable=False
    )

    def to_dict(self):
        """辞書形式に変換"""
        return {
            'id': self.ID,
            'name': self.Name,
            'country_code': self.CountryCode
        }
