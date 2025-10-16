# JoyJaunt Frontend - フォルダ構造

整理されたフォルダ構造で、コードの可読性と保守性が向上しました。

## 📁 プロジェクト構造

```
frontend/src/
├── components/              # 再利用可能なコンポーネント
│   └── common/             # 共通コンポーネント
│       ├── ErrorMessage/   # エラー表示コンポーネント
│       │   ├── ErrorMessage.js
│       │   ├── ErrorMessage.css
│       │   └── index.js
│       ├── Loading/        # ローディングコンポーネント
│       │   ├── Loading.js
│       │   ├── Loading.css
│       │   └── index.js
│       └── Navigation/     # ナビゲーションコンポーネント
│           ├── Navigation.js
│           ├── Navigation.css
│           └── index.js
│
├── pages/                  # ページコンポーネント
│   ├── Home/              # ホームページ
│   │   ├── Home.js
│   │   ├── home.css
│   │   └── index.js
│   ├── Tour/              # ツアープランページ
│   │   ├── tour.jsx
│   │   ├── tour.css
│   │   └── index.js
│   ├── Weather/           # 天気予報ページ
│   │   ├── Weather.js
│   │   ├── Weather.css
│   │   └── index.js
│   ├── Auth/              # 認証ページ
│   │   ├── LoginSignup.jsx
│   │   ├── LoginSignup.css
│   │   └── index.js
│   ├── Account/           # アカウント概要ページ
│   │   ├── AccountSummary.jsx
│   │   ├── AccountSummary.css
│   │   └── index.js
│   ├── Safe/              # 安全情報ページ
│   │   ├── Safe.js
│   │   └── index.js
│   ├── Warning/           # 警告ページ
│   │   ├── Warning.js
│   │   └── index.js
│   ├── Danger/            # 危険情報ページ
│   │   ├── Dang.js
│   │   └── index.js
│   └── NotFound/          # 404エラーページ
│       ├── NotFound.js
│       ├── NotFound.css
│       └── index.js
│
├── hooks/                  # カスタムReactフック
│   └── useApi.js          # API呼び出し用フック
│
├── services/               # APIサービス層
│   └── api.js             # すべてのAPI関数
│
├── assets/                 # 静的ファイル
│   └── images/            # 画像ファイル
│       ├── clear.png
│       ├── cloud.png
│       ├── rain.png
│       ├── snow.png
│       ├── mist.png
│       ├── globe.svg
│       ├── calendar.svg
│       ├── email.png
│       ├── password.png
│       └── ...
│
├── styles/                 # グローバルスタイル
│   ├── index.css          # メインスタイル
│   ├── App.css            # Appコンポーネントスタイル
│   └── style.css          # 共通スタイル
│
├── utils/                  # ユーティリティ関数
│   └── (将来の拡張用)
│
├── App.js                  # メインアプリコンポーネント
├── index.js               # エントリーポイント
├── config.js              # 設定ファイル
├── Setting.js             # 設定ページ
└── reportWebVitals.js     # パフォーマンス測定
```

## 🎯 設計原則

### 1. **コンポーネント分離**
- **Pages**: ページレベルのコンポーネント（ルートに対応）
- **Components**: 再利用可能なUIコンポーネント
- **Common**: 複数のページで使用される共通コンポーネント

### 2. **インポートパスの簡潔化**
各コンポーネントフォルダに`index.js`を配置することで、インポートが簡潔に:
```javascript
// Before
import ErrorMessage from './components/ErrorMessage/ErrorMessage';

// After
import ErrorMessage from '../../components/common/ErrorMessage';
```

### 3. **責任の分離**
- **Services**: API通信ロジック
- **Hooks**: 状態管理ロジック
- **Components**: UI表示ロジック
- **Pages**: ページ構成ロジック

### 4. **ファイル命名規則**
- コンポーネントファイル: `ComponentName.js` または `ComponentName.jsx`
- スタイルファイル: `ComponentName.css`
- インデックスファイル: `index.js`

## 📦 各フォルダの役割

### `components/common/`
すべてのページで使用できる汎用的なUIコンポーネント:
- `ErrorMessage`: エラー、警告、情報、成功メッセージの表示
- `Loading`: ローディングスピナー
- `Navigation`: アプリケーション全体のナビゲーション

### `pages/`
各ルートに対応するページコンポーネント:
- 各ページは独自のフォルダを持つ
- ページ専用のスタイルとロジックを含む
- `index.js`でデフォルトエクスポート

### `services/`
バックエンドAPIとの通信を担当:
- すべてのAPI呼び出しを一元管理
- エラーハンドリングを統一
- APIエンドポイントの変更を容易に

### `hooks/`
カスタムReactフック:
- `useApi`: API呼び出しの状態管理
- ローディング、エラー、データ状態を自動管理

### `assets/`
静的ファイル（画像、アイコンなど）:
- 一元管理で見つけやすい
- インポートパスの一貫性

### `styles/`
グローバルなスタイル定義:
- アプリケーション全体のスタイル
- 共通のCSS変数や定義

## 🚀 使い方

### コンポーネントのインポート
```javascript
// 共通コンポーネント
import ErrorMessage from '../../components/common/ErrorMessage';
import Loading from '../../components/common/Loading';
import Navigation from '../../components/common/Navigation';

// ページコンポーネント
import Home from '../../pages/Home';
import Tour from '../../pages/Tour';

// サービス
import { login, getCountries } from '../../services/api';

// フック
import { useApi } from '../../hooks/useApi';

// アセット
import logo from '../../assets/images/logo.png';
```

## 🔧 今後の拡張

### `utils/`フォルダ
ユーティリティ関数を追加予定:
- 日付フォーマット関数
- バリデーション関数
- ヘルパー関数

### `contexts/`フォルダ（将来追加予定）
React Contextを使用したグローバル状態管理:
- 認証コンテキスト
- テーマコンテキスト
- ユーザー設定コンテキスト

### `constants/`フォルダ（将来追加予定）
定数定義:
- API URL
- エラーメッセージ
- 設定値

## ✨ メリット

1. **可読性向上**: フォルダ構造が明確で、ファイルが見つけやすい
2. **保守性向上**: 責任が分離され、変更の影響範囲が明確
3. **拡張性**: 新機能の追加が容易
4. **チーム開発**: 規約が明確で、複数人での開発がスムーズ
5. **テストしやすさ**: コンポーネントが分離され、単体テストが書きやすい
