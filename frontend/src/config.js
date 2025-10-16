// API設定ファイル
// 環境変数からAPIのベースURLを取得

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

export default API_URL;
