import tkinter as tk
from tkinter import ttk
import requests
# Function to fetch exchange rates dynamically
def get_currency_rate(from_currency, to_currency):
    try:
        url = f"https://open.er-api.com/v6/latest/{from_currency}"  # Using Open Exchange Rates API
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data["rates"].get(to_currency, None)
    except Exception as e:
        return f"Error fetching exchange rate: {e}"
# Conversion dictionaries for each type
conversion_factors = {
    "Length": {
        "meters": 1,
        "kilometers": 0.001,
        "miles": 0.000621371,
        "yards": 1.09361,
        "feet": 3.28084,
        "inches": 39.3701,
        "centimeters": 100,
        "millimeters": 1000,
        "nanometers": 1e9,
        "picometers": 1e12,
        "nautical miles": 0.000539957,
    },
    "Mass": {
        "kilograms": 1,
        "grams": 1000,
        "milligrams": 1e6,
        "micrograms": 1e9,
        "metric tons": 0.001,
        "US tons": 0.00110231,
        "imperial tons": 0.000984207,
        "stones": 0.157473,
        "pounds": 2.20462,
        "ounces": 35.274,
    },
    "Temperature": {
        "Celsius": lambda x: x,
        "Fahrenheit": lambda x: (x * 9 / 5) + 32,
        "Kelvin": lambda x: x + 273.15,
    },
    "Area": {
        "square meters": 1,
        "square kilometers": 1e-6,
        "square miles": 3.861e-7,
        "acres": 0.000247105,
        "hectares": 0.0001,
        "square yards": 1.19599,
        "square feet": 10.7639,
        "square inches": 1550,
    },
    "Volume": {
        "liters": 1,
        "milliliters": 1000,
        "cubic meters": 0.001,
        "cubic inches": 61.0237,
        "cubic feet": 0.0353147,
        "imperial gallons": 0.219969,
        "US gallons": 0.264172,
        "Imperial teaspoone": 168.9,
        "Imperial tablesppone": 56.312,
        "Imperial fluid ounce": 35.195,
        "Imperial cup": 3.52, 
        "Imperial pint": 1.76,
        "Imperial quart": 1.136,
        "US teaspoon": 202.884,
        "US tablespoon": 67.628,
        "US fluid ounce": 33.814,
        "US legal cup": 4.167,
        "US liquid pint": 2.113,
        "US liquid quart": 1.057,
    },
    "Speed": {
        "meters/second": 1,
        "kilometers/hour": 3.6,
        "miles/hour": 2.23694,
        "feet/second": 3.28084,
        "knots": 1.94384,
    },
    "Time": {
        "seconds": 1,
        "minutes": 1 / 60,
        "hours": 1 / 3600,
        "days": 1 / 86400,
        "weeks": 1/604800,
        "months": 1/2.628e+6,
        "years": 1/3.154e+7,
        "decades": 1/3.154e+8,
        "centuries": 1/3.154e+9,
        "millisecond": 1000,
        "microsecond": 1e+6,
        "nanosecond": 1e+9
    },
    "Pressure": {
        "pascals": 1,
        "bar": 1e-5,
        "PSI": 0.000145038,
        "torr": 0.00750062,
        "atmosphere": 1/ 101300
    },
    "Energy": {
        "joules": 1,
        "calories": 0.239006,
        "kilocalories": 0.000239006,
        "watt hours": 1/ 3600,
        "kilowatt-hours": 2.77778e-7,
        "BTUs": 0.000947817,
        "Electronvolt": 6.242e+18,
        "US therm": 1/1.055e+8,
        "Foot-pound": 1/1.356
    },
    "Data Storage": {
        "bytes": 1,
        "kilobytes": 0.001,
        "kibibytes": 1/1024,
        "megabytes": 1/1e+6,
        "mebibytes": 1/1.049e+6,
        "gigabytes": 1/1e+9,
        "gibibytes": 1/1.074e+9,
        "terabytes": 1/1e+12,
        "tebibytes": 1/1.1e+12,
        "petabytes": 1/1e+15,
        "pebibytes": 1/1.126e+15,
        "pebibits": 1/1.407e+14,
        "petabits": 1/1.25e+14,
        "tebibits": 1/1.374e+11,
        "terabits": 1/1.25e+11,
        "gibibits": 1/1.342e+8,
        "gigabits": 1/1.25e+8,
        "mebibits": 1/131100,
        "megabits": 1/125000,
        "kibibits": 1/128,
        "kilobits": 1/125,
        "bits": 8
    },
    "Angle": {
        "radians": 1,
        "milliradian": 1000,
        "degrees": 57.2958,
        "arcseconds": 206264.806,
        "gradians": 63.662,
        "minutes of arc": 3437.75,
    },
    "Frequency": {
        "hertz": 1,
        "kilohertz": 0.001,
        "megahertz": 1/1e+6,
        "gigahertz": 1/1e+9       
    },
    "Fuel economy": {
        "kilometer/liter": 1,
        "US miles/gallon": 2.352,
        "Imerpial miles/gallon": 2.825,
        "liter/100 kilometers": 100
    },
    "Data transfer rate": {
        "bit/second": 1,
        "kilobit/second": 0.001,
        "kilobyte/second": 1/8000,
        "kibibit/second": 1/1024,
        "megabit/second": 1/1e+6,
        "megabyte/second": 1/8e+6,
        "mebibit/second": 1/1.049e+6,
        "gigabit/second": 1/1e+9,
        "gigabyte/second":1/8e+9,
        "gibibit/second": 1/1.074e+9,
        "terabit/second": 1/1e+12,
        "terabyte/second": 1/8e+12,
        "tebibit/second": 1/1.1e+12
    },
    "Currency": {
    "USD": "USD",  # United States Dollar
    "EUR": "EUR",  # Euro
    "GBP": "GBP",  # British Pound
    "JPY": "JPY",  # Japanese Yen
    "AUD": "AUD",  # Australian Dollar
    "CAD": "CAD",  # Canadian Dollar
    "CHF": "CHF",  # Swiss Franc
    "CNY": "CNY",  # Chinese Yuan
    "INR": "INR",  # Indian Rupee
    "BRL": "BRL",  # Brazilian Real
    "ZAR": "ZAR",  # South African Rand
    "RUB": "RUB",  # Russian Ruble
    "KRW": "KRW",  # South Korean Won
    "SGD": "SGD",  # Singapore Dollar
    "HKD": "HKD",  # Hong Kong Dollar
    "NZD": "NZD",  # New Zealand Dollar
    "SEK": "SEK",  # Swedish Krona
    "NOK": "NOK",  # Norwegian Krone
    "DKK": "DKK",  # Danish Krone
    "THB": "THB",  # Thai Baht
    "IDR": "IDR",  # Indonesian Rupiah
    "PHP": "PHP",  # Philippine Peso
    "MXN": "MXN",  # Mexican Peso
    "ARS": "ARS",  # Argentine Peso
    "TRY": "TRY",  # Turkish Lira
    "AED": "AED",  # UAE Dirham
    "SAR": "SAR",  # Saudi Riyal
    "EGP": "EGP",  # Egyptian Pound
    "PKR": "PKR",  # Pakistani Rupee
    "MYR": "MYR",  # Malaysian Ringgit
    "TWD": "TWD",  # Taiwan Dollar
    "PLN": "PLN",  # Polish Zloty
    "CZK": "CZK",  # Czech Koruna
    "HUF": "HUF",  # Hungarian Forint
    "ILS": "ILS",  # Israeli New Shekel
    "COP": "COP",  # Colombian Peso
    "CLP": "CLP",  # Chilean Peso
    "NGN": "NGN",  # Nigerian Naira
    },
}
# Adaptive float formatting
def format_result(value):
    if abs(value) > 1e15 or abs(value) < 1e-15 and value != 0:
        return f"{value:.12e}"  # Scientific notation
    return f"{value:.12g}"  # General formatting with 12 significant digits
# Function to update units dynamically
def update_units(*args):
    conversion_type = type_var.get()
    if conversion_type in conversion_factors:
        units = list(conversion_factors[conversion_type].keys())
        from_unit_dropdown.config(values=units)
        to_unit_dropdown.config(values=units)
        from_unit_var.set(units[0])
        to_unit_var.set(units[1] if len(units) > 1 else units[0])
# Conversion logic
def convert_units():
    conversion_type = type_var.get()
    from_unit = from_unit_var.get()
    to_unit = to_unit_var.get()
    try:
        value = float(value_entry.get())
        if conversion_type == "Currency":
            rate = get_currency_rate(from_unit, to_unit)
            if rate:
                result = value * rate
                result_label.config(text=f"{value} {from_unit} = {format_result(result)} {to_unit}")
            else:
                result_label.config(text="Error fetching exchange rate.")
        elif conversion_type == "Temperature":
            if from_unit == "Celsius" and to_unit == "Fahrenheit":
                result = (value * 9 / 5) + 32
            elif from_unit == "Fahrenheit" and to_unit == "Celsius":
                result = (value - 32) * 5 / 9
            elif from_unit == "Celsius" and to_unit == "Kelvin":
                result = value + 273.15
            elif from_unit == "Kelvin" and to_unit == "Celsius":
                result = value - 273.15
            elif from_unit == "Fahrenheit" and to_unit == "Kelvin":
                result = (value - 32) * 5 / 9 + 273.15
            elif from_unit == "Kelvin" and to_unit == "Fahrenheit":
                result = (value - 273.15) * 9 / 5 + 32
            else:
                result = value  # Assume the same unit
            result_label.config(text=f"{value} {from_unit} = {format_result(result)} {to_unit}")
        else:
            factor_from = conversion_factors[conversion_type][from_unit]
            factor_to = conversion_factors[conversion_type][to_unit]
            result = value * (factor_to / factor_from)
            result_label.config(text=f"{value} {from_unit} = {format_result(result)} {to_unit}")
    except ValueError:
        result_label.config(text="Invalid value. Please enter a number.")
# GUI Setup
root = tk.Tk()
root.title("Versatile Unit Converter")
root.geometry("700x600")
# Conversion type label and dropdown
tk.Label(root, text="Conversion Type:", font=("Arial", 14)).pack(pady=5)
type_var = tk.StringVar(value="Length")
type_dropdown = ttk.Combobox(root, textvariable=type_var, values=list(conversion_factors.keys()), font=("Arial", 12), state="readonly")
type_dropdown.pack()
# From unit label and dropdown
tk.Label(root, text="From Unit:", font=("Arial", 14)).pack(pady=5)
from_unit_var = tk.StringVar()
from_unit_dropdown = ttk.Combobox(root, textvariable=from_unit_var, font=("Arial", 12), state="readonly")
from_unit_dropdown.pack()
# To unit label and dropdown
tk.Label(root, text="To Unit:", font=("Arial", 14)).pack(pady=5)
to_unit_var = tk.StringVar()
to_unit_dropdown = ttk.Combobox(root, textvariable=to_unit_var, font=("Arial", 12), state="readonly")
to_unit_dropdown.pack()
# Input value label and entry
tk.Label(root, text="Enter Value:", font=("Arial", 14)).pack(pady=5)
value_entry = tk.Entry(root, font=("Arial", 12))
value_entry.pack()
# Convert button
tk.Button(root, text="Convert", command=convert_units, font=("Arial", 14), bg="#4CAF50", fg="white").pack(pady=15)
# Result label
result_label = tk.Label(root, text="", font=("Arial", 14), fg="blue", wraplength=650, justify="center")
result_label.pack(pady=10)
# Link update_units function to dropdown change
type_var.trace("w", update_units)
# Initialize the dropdowns with default values
update_units()
# Run the GUI loop
root.mainloop()