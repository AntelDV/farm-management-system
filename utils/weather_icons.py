WEATHER_DATA = {
    # Clear
    '01d': {'text': '☀️', 'color': "#FF9D00"},  # clear sky day
    '01n': {'text': '🌙', 'color': "#FF9900"},  # clear sky night
    
    # Clouds
    '02d': {'text': '⛅', 'color': "#98D0D4"},  # few clouds day
    '02n': {'text': '⛅', 'color': "#3A475A"},  # few clouds night
    '03d': {'text': '☁️', 'color': '#7F8C8D'},  # scattered clouds
    '03n': {'text': '☁️', 'color': '#AAB7B8'},  # scattered clouds
    '04d': {'text': '☁️☁️', 'color': '#566573'},  # broken clouds
    '04n': {'text': '☁️☁️', 'color': '#7B7D7D'},  # broken clouds
    
    # Rain
    '09d': {'text': '🌧️', 'color': '#5DADE2'},  # shower rain
    '09n': {'text': '🌧️', 'color': '#3498DB'},  # shower rain
    '10d': {'text': '🌦️', 'color': '#2980B9'},  # rain day
    '10n': {'text': '🌧️', 'color': '#2471A3'},  # rain night
    
    # Thunderstorm
    '11d': {'text': '⛈️', 'color': '#5D6D7E'},  # thunderstorm
    '11n': {'text': '⛈️', 'color': '#34495E'},  # thunderstorm
    
    # Snow
    '13d': {'text': '❄️', 'color': '#AED6F1'},  # snow
    '13n': {'text': '❄️', 'color': '#85C1E9'},  # snow
    
    # Mist/Fog
    '50d': {'text': '🌫️', 'color': "#3C4A4A"},  # mist
    '50n': {'text': '🌫️', 'color': "#5A6B7F"},  # mist
    
    # Default
    'default': {'text': '🌈', 'color': '#000000'}  # default
}

def get_weather_icon(icon_code):
    """Lấy thông tin icon và màu sắc theo mã thời tiết"""
    return WEATHER_DATA.get(icon_code, WEATHER_DATA['default'])

def get_weather_description(description):
    """Chuyển đổi mô tả thời tiết sang tiếng Việt"""
    translations = {
        'clear sky': 'trời quang',
        'few clouds': 'ít mây',
        'scattered clouds': 'mây rải rác',
        'broken clouds': 'nhiều mây',
        'shower rain': 'mưa rào',
        'rain': 'mưa',
        'thunderstorm': 'giông bão',
        'snow': 'tuyết',
        'mist': 'sương mù',
        'haze': 'sương mù nhẹ',
        'fog': 'sương mù dày',
        'overcast clouds': 'mây u ám',
        'light rain': 'mưa nhẹ',
        'moderate rain': 'mưa vừa',
        'heavy intensity rain': 'mưa to'
    }
    return translations.get(description.lower(), description)