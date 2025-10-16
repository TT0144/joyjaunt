import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import { getCountries, getCitiesByCountry, getWeatherForecast } from './services/api';
import ErrorMessage from './components/ErrorMessage';
import './tour.css';
import './LoginSignup.css';
import './style.css';

import globe_icon from './image/globe.svg';
import date_icon from './image/calendar.svg';
import add_icon from './image/add.svg';
import desktopImage from './image/desktop-1.svg';

const componentStyle = {
    backgroundImage: `url(${desktopImage})`,
    backgroundSize: 'cover',
    backgroundRepeat: 'no-repeat',
    backgroundPosition: 'center',
};


const Tour = () => {
    const [departureDate, setDepartureDate] = useState(null);
    const [returnDate, setReturnDate] = useState(null);
    const [locations, setLocations] = useState([{ from: '', stopovers: [''], to: '' }]);
    const [selectedCountry, setSelectedCountry] = useState('JPN');
    const [availableCities, setAvailableCities] = useState([]);
    const [weather, setWeather] = useState(null);
    const [selectedCity, setSelectedCity] = useState('');
    const [countryList, setCountryList] = useState([]);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    // Fetch cities when country changes

    useEffect(() => {
        const fetchCountries = async () => {
            try {
                setError(null);
                const data = await getCountries();
                const sortedCountries = data.sort((a, b) => a.name.localeCompare(b.name));
                setCountryList(sortedCountries);
            } catch (error) {
                console.error('Error fetching country list:', error);
                setError(error.message);
            }
        };

        fetchCountries();
    }, []);

    useEffect(() => {
        const fetchCities = async () => {
            try {
                setError(null);
                const cities = await getCitiesByCountry(selectedCountry);
                const sortedCities = cities.sort((a, b) => a.localeCompare(b));
                setAvailableCities(sortedCities);
            } catch (error) {
                console.error('Error fetching cities:', error);
                setError(error.message);
                setAvailableCities([]);
            }
        };
    
        localStorage.setItem("selectedCountry", selectedCountry);
        fetchCities();
    }, [selectedCountry]);

    // 初期都市を設定するための新しいuseEffect
    useEffect(() => {
        if (availableCities.length > 0) {
            setSelectedCity(availableCities[0]);
            // 初期都市をローカルストレージに保存
            localStorage.setItem("selectedCity", availableCities[0]);
        }
    }, [availableCities]);

    // Fetch weather for the selected city
    useEffect(() => {
        const fetchWeather = async (city) => {
            try {
                setError(null);
                const data = await getWeatherForecast(city);
                setWeather(data.forecast);
            } catch (error) {
                console.error('Error fetching weather:', error);
                setError(error.message);
                setWeather(null);
            }
        };

        if (availableCities.length > 0) {
            const defaultCity = availableCities[0];
            fetchWeather(defaultCity);
        }
    }, [availableCities]);

    const handleLocationChange = (index, field, value) => {
        const newLocations = [...locations];
        newLocations[index][field] = value;
        setLocations(newLocations);

        // 出発地（from）が変更された場合、その都市をローカルストレージに保存
        if (field === 'from') {
            localStorage.setItem("selectedCity", value);
            setSelectedCity(value);
        }
    };

    const handleStopoverChange = (index, stopoverIndex, value) => {
        const newLocations = [...locations];
        newLocations[index].stopovers[stopoverIndex] = value;
        setLocations(newLocations);
    };

    const addStopover = (index) => {
        const newLocations = [...locations];
        newLocations[index].stopovers.push('');
        setLocations(newLocations);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        // 選択された国と都市のデータを保存
        const countryName = countryList.find(c => c.code === selectedCountry)?.name || '';
        localStorage.setItem("selectedCountry", selectedCountry);
        localStorage.setItem("selectedCountryName", countryName);
        localStorage.setItem("selectedCity", locations[0].from);
    
        // セットアップ完了フラグを保存（emailはログイン時のものを使用）
        const email = localStorage.getItem("userEmail"); // ログイン時にemailを保存しておく必要があります
        if (email) {
            localStorage.setItem(`user_${email}_completed_setup`, 'true');
        }
    
        const formData = { departureDate, returnDate, locations, selectedCountry };
        console.log("フォーム送信データ:", formData);
        
        try {
            await fetch('/submit', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });
            
            navigate('/', { 
                state: { 
                    isLoggedIn: true,
                    selectedCountry: selectedCountry,
                    selectedCity: locations[0].from
                } 
            });
        } catch (error) {
            console.error('フォーム送信エラー:', error);
        }
    };

    // スクロールを自動で下に移動
    useEffect(() => {
        const container = document.querySelector('.location-section');
        if (container) {
            container.scrollTop = container.scrollHeight;
        }
    }, [locations]);

    return (
        <div className="bigbox" style={componentStyle}>
            {error && (
                <ErrorMessage
                    type="error"
                    message={error}
                    onClose={() => setError(null)}
                />
            )}
            <div className="box">
                <div className='container'>
                    <div className="header2">
                        <div className="text">Plan Your<br /> Holiday</div>
                    </div>

                    <div className="inputs">
                        <p className='label'>Country</p>
                        <div className="input">
                            <img src={globe_icon} alt="" />
                            <select
                                value={selectedCountry}
                                onChange={(e) => setSelectedCountry(e.target.value)}
                            >
                                {countryList.map((country) => (
                                    <option key={country.code} value={country.code}>
                                        {country.name}
                                    </option>
                                ))}
                            </select>
                        </div>

                        {/* Rest of the existing code remains the same */}
                        <p className="label">Departure Date</p>
                        <div className="input">
                            <img src={date_icon} alt="" />
                            <DatePicker
                                selected={departureDate}
                                onChange={date => setDepartureDate(date)}
                                dateFormat="MM/dd/yyyy"
                                placeholderText='MM/DD/YY' />
                        </div>
                        <p className="label">Return Date</p>
                        <div className="input">
                            <img src={date_icon} alt="" />
                            <DatePicker
                                selected={returnDate}
                                onChange={date => setReturnDate(date)}
                                dateFormat="MM/dd/yyyy"
                                placeholderText='MM/DD/YY' />
                        </div>
                    </div>

                    <div className="divider">
                        <hr className="custom-hr" />
                    </div>

                    <div className="location-section">
                        {locations.map((location, index) => (
                            <div key={index}>
                                <div className="inputs-below">
                                    <p className='label'>From</p>
                                    <div className="input">
                                        <select
                                            value={location.from}
                                            onChange={(e) => handleLocationChange(index, 'from', e.target.value)}
                                        >
                                            {availableCities.map((city, cityIndex) => (
                                                <option key={cityIndex} value={city}>
                                                    {city}
                                                </option>
                                            ))}
                                        </select>
                                    </div>

                                    {location.stopovers.map((stopover, stopoverIndex) => (
                                        <div key={stopoverIndex}>
                                            <p className='label'>{stopoverIndex + 1}</p>
                                            <div className="input">
                                                <select
                                                    value={stopover}
                                                    onChange={(e) => handleStopoverChange(index, stopoverIndex, e.target.value)}
                                                >
                                                    {availableCities.map((city, cityIndex) => (
                                                        <option key={cityIndex} value={city}>
                                                            {city}
                                                        </option>
                                                    ))}
                                                </select>
                                            </div>
                                        </div>
                                    ))}

                                    <p className='label'>To</p>
                                    <div className="input">
                                        <select
                                            value={location.to}
                                            onChange={(e) => handleLocationChange(index, 'to', e.target.value)}
                                        >
                                            {availableCities.map((city, cityIndex) => (
                                                <option key={cityIndex} value={city}>
                                                    {city}
                                                </option>
                                            ))}
                                        </select>
                                    </div>
                                </div>

                                <div className="add-input">
                                    <button className="add" onClick={() => addStopover(index)}>
                                        <img src={add_icon} alt="Add Stopover" />
                                    </button>
                                </div>
                            </div>
                        ))}
                    </div>

                    <div className="submit-container">
                        <button className="submit" onClick={handleSubmit}>Go</button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Tour;
