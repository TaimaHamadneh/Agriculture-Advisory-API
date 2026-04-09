def generate_advice(crop_type: str, is_greenhouse: bool, measured: dict, optimal) -> str:
    """
    measured = {"soil_moisture": x, "temperature": y, "humidity": z, "co2_level": w}
    optimal = CropOptimal instance
    """
    advice_lines = [f"Advice for {crop_type} ({'greenhouse' if is_greenhouse else 'open field'}):"]
    
    # Temperature
    if measured["temperature"] < optimal.temp_min:
        advice_lines.append(f"⚠️ Temperature is too low ({measured['temperature']}°C). Optimal range: {optimal.temp_min}–{optimal.temp_max}°C. Increase heating.")
    elif measured["temperature"] > optimal.temp_max:
        advice_lines.append(f"⚠️ Temperature is too high ({measured['temperature']}°C). Optimal range: {optimal.temp_min}–{optimal.temp_max}°C. Provide shade or ventilation.")
    else:
        advice_lines.append(f"✅ Temperature {measured['temperature']}°C is within optimal range ({optimal.temp_min}–{optimal.temp_max}°C).")
    
    # Humidity
    if measured["humidity"] < optimal.humidity_min:
        advice_lines.append(f"⚠️ Humidity is too low ({measured['humidity']}%). Optimal: {optimal.humidity_min}–{optimal.humidity_max}%. Increase misting or irrigation.")
    elif measured["humidity"] > optimal.humidity_max:
        advice_lines.append(f"⚠️ Humidity is too high ({measured['humidity']}%). Optimal: {optimal.humidity_min}–{optimal.humidity_max}%. Improve air circulation.")
    else:
        advice_lines.append(f"✅ Humidity {measured['humidity']}% is optimal.")
    
    # CO2
    if measured["co2_level"] < optimal.co2_min:
        advice_lines.append(f"⚠️ CO2 level is low ({measured['co2_level']} ppm). Optimal: {optimal.co2_min}–{optimal.co2_max} ppm. Consider CO2 enrichment.")
    elif measured["co2_level"] > optimal.co2_max:
        advice_lines.append(f"⚠️ CO2 level is high ({measured['co2_level']} ppm). Optimal: {optimal.co2_min}–{optimal.co2_max} ppm. Increase ventilation.")
    else:
        advice_lines.append(f"✅ CO2 {measured['co2_level']} ppm is within optimal range.")
    
    # Soil moisture
    if measured["soil_moisture"] < optimal.soil_moisture_min:
        advice_lines.append(f"⚠️ Soil moisture is too dry ({measured['soil_moisture']}%). Optimal: {optimal.soil_moisture_min}–{optimal.soil_moisture_max}%. Increase irrigation.")
    elif measured["soil_moisture"] > optimal.soil_moisture_max:
        advice_lines.append(f"⚠️ Soil moisture is too wet ({measured['soil_moisture']}%). Optimal: {optimal.soil_moisture_min}–{optimal.soil_moisture_max}%. Reduce watering and improve drainage.")
    else:
        advice_lines.append(f"✅ Soil moisture {measured['soil_moisture']}% is ideal.")
    
    return "\n".join(advice_lines)