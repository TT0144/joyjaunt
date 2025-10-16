"""
認証関連のルート
"""
from datetime import datetime
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db, bcrypt
from app.models import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """ユーザー登録"""
    try:
        data = request.json

        # 必須フィールドの取得
        email = data.get('email')
        password = data.get('password')
        country_code = data.get('country_code')
        passport_expiry_str = data.get('passport_expiry')
        language_no = data.get('language_no', 'ja')

        # バリデーション
        if not all([email, password, country_code, passport_expiry_str]):
            return jsonify({"error": "Missing required fields"}), 400

        # 既存ユーザーチェック
        existing_user = User.query.filter_by(EMAIL=email).first()
        if existing_user:
            return jsonify({"error": "Email already registered"}), 409

        # 日付の変換
        if passport_expiry_str.endswith("Z"):
            passport_expiry_str = passport_expiry_str.replace("Z", "+00:00")
        passport_expiry = datetime.fromisoformat(passport_expiry_str)

        # パスワードをハッシュ化
        hashed_password = bcrypt.generate_password_hash(
            password).decode('utf-8')

        # ユーザー番号を生成
        user_no = User.generate_user_no()

        # 新しいユーザーを作成
        new_user = User(
            USER_NO=user_no,
            EMAIL=email,
            PW=hashed_password,
            COUNTRY_Code=country_code,
            PASSPORTEXPIRY=passport_expiry,
            LANGUAGE_NO=language_no
        )

        # データベースに保存
        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            "message": "Registration successful",
            "user_no": user_no
        }), 201

    except ValueError as e:
        return jsonify({"error": "Invalid data", "details": str(e)}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Unexpected error", "details": str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """ユーザーログイン"""
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"error": "Email and password required"}), 400

        # ユーザー情報をデータベースから取得
        user = User.query.filter_by(EMAIL=email).first()

        if not user:
            return jsonify({"error": "User not found"}), 404

        if not bcrypt.check_password_hash(user.PW, password):
            return jsonify({"error": "Invalid password"}), 401

        # JWTトークンを作成
        access_token = create_access_token(identity=user.USER_NO)

        # パスポート有効期限をフォーマット
        passport_expiry = user.PASSPORTEXPIRY.strftime(
            '%Y-%m-%d') if user.PASSPORTEXPIRY else None

        return jsonify({
            "access_token": access_token,
            "passportExpiry": passport_expiry,
            "country": user.COUNTRY_Code,
            "user_no": user.USER_NO
        }), 200

    except Exception as e:
        return jsonify({"error": "Login failed", "details": str(e)}), 500


@auth_bp.route('/user-info', methods=['GET'])
@jwt_required()
def get_user_info():
    """ユーザー情報取得(要認証)"""
    try:
        current_user_no = get_jwt_identity()
        user = User.query.filter_by(USER_NO=current_user_no).first()

        if not user:
            return jsonify({"error": "User not found"}), 404

        return jsonify(user.to_dict()), 200

    except Exception as e:
        return jsonify({"error": "Failed to get user info", "details": str(e)}), 500


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    """トークンリフレッシュ"""
    try:
        current_user_no = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user_no)

        return jsonify({"access_token": new_access_token}), 200

    except Exception as e:
        return jsonify({"error": "Token refresh failed", "details": str(e)}), 500
