import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import './LoginSignup.css';
import './style.css';

import email_icon from './image/email.png';
import password_icon from './image/password.png';
import globe_icon from './image/globe.svg';
import date_icon from './image/calendar.svg';
import desktopImage from './image/desktop-1.svg';

const componentStyle = {
    backgroundImage: `url(${desktopImage})`,
    backgroundSize: 'cover',
    backgroundRepeat: 'no-repeat',
    backgroundPosition: 'center',
};

const API_URL = "http://10.108.0.4:5000";

const LoginSignup = () => {
    const navigate = useNavigate();
    const [action, setAction] = useState("Login");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [country, setCountry] = useState("JPN");
    const [date, setDate] = useState(null);
    const [message, setMessage] = useState("");
    const [loading, setLoading] = useState(false);
    const [countryList, setCountryList] = useState([]);

    useEffect(() => {
        const fetchCountries = async () => {
            try {
                const response = await fetch(`${API_URL}/countries`);
                if (response.ok) {
                    const data = await response.json();
                    setCountryList(data);
                }
            } catch (error) {
                console.error("エラーが発生しました:", error);
            }
        };
        fetchCountries();
    }, []);

    const validateInputs = () => {
        if (!email || !password) {
            setMessage("メールアドレスとパスワードを入力してください");
            return false;
        }

        const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
        if (!emailPattern.test(email)) {
            setMessage("有効なメールアドレスを入力してください");
            return false;
        }

        if (action === "SignUp" && !date) {
            setMessage("パスポートの有効期限を選択してください");
            return false;
        }

        return true;
    };

    const handleSubmit = async () => {
        if (!validateInputs()) {
            return;
        }
    
        try {
            setLoading(true);
            const endpoint = action === "Login" ? "/login" : "/register";
            const formattedDate = date ? date.toISOString().split("T")[0] : null;
            const payload = action === "Login"
                ? { email, password }
                : { email, password, country_code: country, passport_expiry: formattedDate, language_no: "JPN" };
    
            const response = await fetch(`${API_URL}${endpoint}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload),
            });
    
            if (response.ok) {
                const data = await response.json();
                
                if (action === "Login") {
                    localStorage.setItem("token", data.access_token);
                    
                    // ユーザーの訪問履歴をチェック
                    const hasCompletedSetup = localStorage.getItem(`user_${email}_completed_setup`);
                    
                    if (hasCompletedSetup === 'true') {
                        // 2回目以降のログインの場合、直接ホームへ
                        navigate('/', {
                            state: {
                                isLoggedIn: true,
                                email: email,
                                nationality: data.country || country,
                                passportExpiry: data.passportExpiry
                            }
                        });
                    } else {
                        // 初回ログインの場合、アカウント確認画面へ
                        navigate('/AccountSummary', {
                            state: {
                                email: email,
                                password: password,
                                nationality: data.country || country,
                                passportExpiry: data.passportExpiry
                            }
                        });
                    }
                } else {
                    // 新規登録の場合
                    alert('登録が完了しました！ログインしてください。');
                    setAction("Login");
                }
            } else {
                const errorData = await response.json().catch(() => ({ error: "サーバーエラー" }));
                setMessage(`エラー: ${errorData.error || `${action === "Login" ? "ログイン" : "登録"}に失敗しました`}`);
            }
        } catch (error) {
            setMessage("予期しないエラーが発生しました。");
            console.error("エラーが発生しました:", error);
        } finally {
            setLoading(false);
        }
    };

    const renderInputField = (label, value, setValue, type = "text", icon = null, placeholder = "") => (
        <>
            <p className='label'>{label}</p>
            <div className="input">
                {icon && <img src={icon} alt="" />}
                <input 
                    type={type} 
                    placeholder={placeholder} 
                    value={value} 
                    onChange={(e) => setValue(e.target.value)} 
                />
            </div>
        </>
    );

    const renderCountrySelector = () => (
        <>
            <p className='label'>Nationality</p>
            <div className="input">
                <img src={globe_icon} alt="globe" />
                <select value={country} onChange={(e) => setCountry(e.target.value)}>
                    {countryList.map((country) => (
                        <option key={country.code} value={country.code}>
                            {country.name}
                        </option>
                    ))}
                </select>
            </div>
        </>
    );

    return (
        <div className="bigbox" style={componentStyle}>
            <div className="box">
                <div className='container'>
                    <div className="header2">
                        <div className="text">{action === "Login" ? "Welcome Back!" : "Create an Account"}</div>
                    </div>

                    <div className="inputs">
                        {renderInputField("E-Mail", email, setEmail, "email", email_icon, "Enter Email")}
                        {renderInputField("Password", password, setPassword, "password", password_icon, "Enter Password")}
                        {action === "SignUp" && (
                            <>
                                {renderCountrySelector()}
                                <p className="label">Passport Date of Expiry</p>
                                <div className="input">
                                    <img src={date_icon} alt="" />
                                    <DatePicker 
                                        selected={date} 
                                        onChange={(date) => setDate(date)} 
                                        dateFormat="yyyy-MM-dd" 
                                        placeholderText='YYYY-MM-DD'
                                        minDate={new Date()}
                                    />
                                </div>
                            </>
                        )}
                    </div>

                    <div className="submit-container">
                        <button 
                            className="submit" 
                            onClick={handleSubmit} 
                            disabled={loading}
                        >
                            {loading ? "処理中..." : action === "Login" ? "Login" : "Sign Up"}
                        </button>
                        <p className="message">{message}</p>
                    </div>
                    
                    {action === "Login" ? (
                        <div className="register-now">
                            Don't have an account?{" "}
                            <span onClick={() => setAction("SignUp")}>Register Now</span>
                        </div>
                    ) : (
                        <div className="register-now">
                            Already have an account?{" "}
                            <span onClick={() => setAction("Login")}>Login</span>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default LoginSignup;