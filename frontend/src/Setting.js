import React from 'react';
import { ChevronRight, Bell, Globe, Calendar, User, LogOut, ChevronLeft } from 'lucide-react';

const Setting = () => {
  const menuItems = [
    { icon: <User size={24} />, title: '個人情報変更', onClick: () => alert('個人情報変更がクリックされました') },
    { icon: <Globe size={24} />, title: '言語変更', onClick: () => alert('言語変更がクリックされました') },
    { icon: <Calendar size={24} />, title: '日程変更', onClick: () => alert('日程変更がクリックされました') },
    { icon: <Bell size={24} />, title: '通知設定', onClick: () => alert('通知設定がクリックされました') },
  ];

  const handleLogout = () => {
    alert('ログアウトしました');
  };

  const handleBack = () => {
    alert('戻るボタンがクリックされました');
  };

  return (
    <div style={{
      minHeight: '100vh',
      backgroundColor: '#f0f0dd',
      padding: '1.5rem',
      display: 'flex',
      flexDirection: 'column'
    }}>
      <div style={{
        maxWidth: '28rem',
        margin: '0 auto',
        width: '100%',
        flex: '1'
      }}>
        {/* ヘッダー */}
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: '2rem'
        }}>
          <h1 style={{
            fontSize: '1.5rem',
            fontWeight: 'bold'
          }}>設定</h1>
          <button 
            onClick={handleLogout} // ログアウト処理を追加
            onMouseEnter={(e) => {
              e.target.style.backgroundColor = 'rgba(220, 38, 38, 0.05)';
            }}
            onMouseLeave={(e) => {
              e.target.style.backgroundColor = 'transparent';
            }}
            style={{
              color: '#dc2626',
              fontWeight: '500',
              borderRadius: '0.75rem',
              padding: '0.75rem 1.5rem',
              display: 'flex',
              alignItems: 'center',
              gap: '0.75rem',
              fontSize: '1rem',
              transition: 'background-color 0.2s'
            }}
          >
            <LogOut size={24} />
            ログアウト
          </button>
        </div>

        {/* メニュー項目 */}
        <div style={{
          display: 'flex',
          flexDirection: 'column',
          gap: '1rem'
        }}>
          {menuItems.map((item, index) => (
            <button
              key={index}
              onClick={item.onClick} // 各ボタンのクリックイベント
              onMouseEnter={(e) => {
                e.target.style.boxShadow = '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)';
                const chevron = e.target.querySelector('.chevron-icon');
                if (chevron) chevron.style.color = '#4b5563';
              }}
              onMouseLeave={(e) => {
                e.target.style.boxShadow = '0 1px 3px 0 rgba(0, 0, 0, 0.1)';
                const chevron = e.target.querySelector('.chevron-icon');
                if (chevron) chevron.style.color = '#9ca3af';
              }}
              style={{
                width: '100%',
                backgroundColor: 'white',
                padding: '1.25rem',
                borderRadius: '1rem',
                boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                transition: 'box-shadow 0.2s'
              }}
            >
              <div style={{
                display: 'flex',
                alignItems: 'center',
                gap: '1.25rem'
              }}>
                <div style={{ color: '#6b7280' }}>{item.icon}</div>
                <span style={{ 
                  color: '#1f2937',
                  fontWeight: '500',
                  fontSize: '1rem'
                }}>{item.title}</span>
              </div>
              <ChevronRight 
                size={24}
                className="chevron-icon"
                style={{ 
                  color: '#9ca3af',
                  transition: 'color 0.2s'
                }}
              />
            </button>
          ))}
        </div>
      </div>

      {/* 戻るボタン */}
      <div style={{
        maxWidth: '7rem',
        margin: '1rem auto 0',
        width: '100%'
      }}>
        <button 
          onClick={handleBack} // 戻る処理を追加
          onMouseEnter={(e) => {
            e.target.style.backgroundColor = 'rgba(0, 0, 0, 0.05)';
          }}
          onMouseLeave={(e) => {
            e.target.style.backgroundColor = 'transparent';
          }}
          style={{
            width: '100%',
            backgroundColor: 'white',
            padding: '1.25rem',
            borderRadius: '1rem',
            boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '1rem',
            transition: 'background-color 0.2s, box-shadow 0.2s'
          }}
        >
          <ChevronLeft size={24} style={{ color: '#1f2937' }} />
          <span style={{ 
            color: '#1f2937',
            fontWeight: '500',
            fontSize: '1rem'
          }}>戻る</span>
        </button>
      </div>
    </div>
  );
};

export default Setting;
