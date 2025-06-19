import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import './LoginSignup.css';
// import './background.css'; //不足
import './AccountSummary.css';
import './style.css'

import email_icon from './image/mail.svg';
import password_icon from './image/pass.svg';
import globe_icon from './image/globe.svg';
import date_icon from './image/calendar.svg';
import desktopImage from './image/desktop-1.svg'; // 背景画像を修正

const componentStyle = {
    backgroundImage: `url(${desktopImage})`,
    backgroundSize: 'cover',
    backgroundRepeat: 'no-repeat',
    backgroundPosition: 'center',
};
const AccountSummary = () => {
    const navigate = useNavigate();
    const location = useLocation();
    console.log('Location State:', location.state);

    


    // `state` からユーザー情報を取得
    const userDetails = location.state || {}; // デフォルト値を空オブジェクトに設定
    return (
        <div className="bigbox" style={componentStyle}>
            <div className="box">
                <div className='container'>
                    <div className="header2">
                        <div className="text">Account<br /> Summary</div>
                    </div>

                    <div className="inputs">
                        <p className='label'>E-Mail</p>
                        <div className="input">
                            <img src={email_icon} alt="" />
                            <input type="email" value={userDetails.email || 'Not provided'} readOnly />
                        </div>
                        <p className='label'>Password</p>
                        <div className="input">
                            <img src={password_icon} alt="" />
                            <input type="password" value={userDetails.password || ''} readOnly />
                        </div>
                        <p className="label">Nationality</p>
                        <div className="input">
                            <img src={globe_icon} alt="" />
                            <input type="text" value={userDetails.nationality || 'Not provided'} readOnly />
                        </div>
                        <p className="label">Passport Date of Expiry</p>
                        <div className="input">
                            <img src={date_icon} alt="" />
                            <input 
                                value={userDetails.passportExpiry || 'Not provided'} 
                                readOnly 
                            />

                        </div>
                    </div>

                    <div className="submit-container">
                        <button className="submit" onClick={() => navigate('/login-signup')}>Edit</button>
                        <button className="submit" onClick={() => {
                            console.log('Submit final data', userDetails);
                            navigate('/tour'); // 次のページに遷移
                        }}>
                            Confirm & Submit
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};


export default AccountSummary;