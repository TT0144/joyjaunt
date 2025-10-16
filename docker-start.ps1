# Docker Quick Start Script
# Docker起動速度を最適化したクイックスタートスクリプト

Write-Host "`n╔════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  JoyJaunt Docker Quick Start (最適化版) ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════╝`n" -ForegroundColor Cyan

# 環境変数の確認
Write-Host "📋 環境変数をチェック中..." -ForegroundColor Yellow
$envFiles = @(".\backend\.env", ".\frontend\.env")
$missingEnv = @()

foreach ($envFile in $envFiles) {
    if (-Not (Test-Path $envFile)) {
        $missingEnv += $envFile
    }
}

if ($missingEnv.Count -gt 0) {
    Write-Host "⚠️  以下の.envファイルが見つかりません:" -ForegroundColor Red
    foreach ($file in $missingEnv) {
        Write-Host "   - $file" -ForegroundColor Red
    }
    Write-Host "`n.envファイルを作成してから再実行してください。`n" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ 環境変数ファイルを確認しました`n" -ForegroundColor Green

# Docker起動オプション選択
Write-Host "🚀 Docker起動オプションを選択してください:`n" -ForegroundColor Cyan
Write-Host "  [1] 高速起動 (キャッシュ利用) - 推奨" -ForegroundColor White
Write-Host "      💡 コード修正後の起動に最適" -ForegroundColor DarkGray
Write-Host "      💡 .py, .jsx, .css などのバグ修正後に使用" -ForegroundColor DarkGray
Write-Host ""
Write-Host "  [2] クリーンビルド (初回または依存関係変更時)" -ForegroundColor White
Write-Host "      💡 requirements.txt や package.json 変更時" -ForegroundColor DarkGray
Write-Host "      💡 新しいライブラリをインストールした時" -ForegroundColor DarkGray
Write-Host ""
Write-Host "  [3] 既存コンテナの停止のみ" -ForegroundColor White
Write-Host ""
Write-Host "  [4] システムクリーンアップ (すべて削除して再構築)" -ForegroundColor White
Write-Host "      💡 完全にリセットしたい時のみ" -ForegroundColor DarkGray
Write-Host ""

$choice = Read-Host "選択 (1-4)"

switch ($choice) {
    "1" {
        Write-Host "`n⚡ 高速起動モード - キャッシュを利用して起動します`n" -ForegroundColor Green
        
        # 既存のコンテナを停止
        Write-Host "🛑 既存のコンテナを停止中..." -ForegroundColor Yellow
        docker-compose down
        
        # キャッシュを利用してビルド＆起動
        Write-Host "🔧 ビルド＆起動中 (約10-30秒)..." -ForegroundColor Yellow
        $startTime = Get-Date
        docker-compose up -d --build
        $endTime = Get-Date
        $duration = ($endTime - $startTime).TotalSeconds
        
        Write-Host "`n✅ 起動完了! (所要時間: $([math]::Round($duration, 1))秒)" -ForegroundColor Green
    }
    
    "2" {
        Write-Host "`n🔄 クリーンビルドモード - イメージを再構築します`n" -ForegroundColor Yellow
        
        # コンテナとボリュームを削除
        Write-Host "🛑 コンテナとボリュームを削除中..." -ForegroundColor Yellow
        docker-compose down -v
        
        # イメージキャッシュをクリア
        Write-Host "🧹 ビルドキャッシュをクリア中..." -ForegroundColor Yellow
        docker builder prune -f
        
        # クリーンビルド
        Write-Host "🔧 クリーンビルド中 (約1-2分)..." -ForegroundColor Yellow
        $startTime = Get-Date
        docker-compose build --no-cache
        docker-compose up -d
        $endTime = Get-Date
        $duration = ($endTime - $startTime).TotalSeconds
        
        Write-Host "`n✅ クリーンビルド完了! (所要時間: $([math]::Round($duration, 1))秒)" -ForegroundColor Green
    }
    
    "3" {
        Write-Host "`n🛑 コンテナを停止しています...`n" -ForegroundColor Yellow
        docker-compose down
        Write-Host "✅ すべてのコンテナを停止しました`n" -ForegroundColor Green
        exit 0
    }
    
    "4" {
        Write-Host "`n⚠️  警告: すべてのDockerリソースを削除します" -ForegroundColor Red
        Write-Host "   - すべてのコンテナ" -ForegroundColor Yellow
        Write-Host "   - すべてのイメージ" -ForegroundColor Yellow
        Write-Host "   - すべてのボリューム" -ForegroundColor Yellow
        Write-Host "   - すべてのビルドキャッシュ`n" -ForegroundColor Yellow
        
        $confirm = Read-Host "本当に実行しますか? (yes/no)"
        
        if ($confirm -eq "yes") {
            Write-Host "`n🧹 システムクリーンアップ中..." -ForegroundColor Yellow
            docker-compose down -v
            docker system prune -a --volumes -f
            
            Write-Host "🔧 再構築中 (約1-2分)..." -ForegroundColor Yellow
            $startTime = Get-Date
            docker-compose build --no-cache
            docker-compose up -d
            $endTime = Get-Date
            $duration = ($endTime - $startTime).TotalSeconds
            
            Write-Host "`n✅ システムクリーンアップ＆再構築完了! (所要時間: $([math]::Round($duration, 1))秒)" -ForegroundColor Green
        } else {
            Write-Host "`n❌ キャンセルされました`n" -ForegroundColor Red
            exit 0
        }
    }
    
    default {
        Write-Host "`n❌ 無効な選択です`n" -ForegroundColor Red
        exit 1
    }
}

# 起動確認
Write-Host "`n🔍 コンテナの状態を確認中...`n" -ForegroundColor Yellow
Start-Sleep -Seconds 3
docker-compose ps

Write-Host "`n📊 サービス情報:" -ForegroundColor Cyan
Write-Host "  Frontend: http://localhost:3001" -ForegroundColor White
Write-Host "  Backend:  http://localhost:5000" -ForegroundColor White
Write-Host "  Database: localhost:3307" -ForegroundColor White

Write-Host "`n📝 ログの確認:" -ForegroundColor Cyan
Write-Host "  すべて:       docker-compose logs -f" -ForegroundColor White
Write-Host "  Frontend:     docker-compose logs -f frontend" -ForegroundColor White
Write-Host "  Backend:      docker-compose logs -f backend" -ForegroundColor White
Write-Host "  Database:     docker-compose logs -f db" -ForegroundColor White

Write-Host "`n� コンテナの再起動:" -ForegroundColor Cyan
Write-Host "  .envファイル変更時: docker-compose restart" -ForegroundColor White
Write-Host "  バックエンドのみ:   docker-compose restart backend" -ForegroundColor White
Write-Host "  フロントエンドのみ: docker-compose restart frontend" -ForegroundColor White

Write-Host "`n💡 開発のヒント:" -ForegroundColor Cyan
Write-Host "  ✅ コードのバグ修正 → ファイル保存のみ（自動リロード）" -ForegroundColor Green
Write-Host "  ✅ .env変更 → docker-compose restart" -ForegroundColor Green
Write-Host "  ⚠️  パッケージ追加 → .\docker-start.ps1 → [2] クリーンビルド" -ForegroundColor Yellow

Write-Host "`n�🛠️  トラブルシューティング:" -ForegroundColor Cyan
Write-Host "  詳細情報:     cat DOCKER_OPTIMIZATION.md" -ForegroundColor White

Write-Host "`n✨ Docker起動スクリプト完了!`n" -ForegroundColor Green
