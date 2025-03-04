from flask import Flask, request, jsonify, render_template, Response
import pandas as pd
import json
import os
import re

app = Flask(__name__)

# Set base directory
base_dir = r"Your-Path"
FILE_PATH = os.path.join(base_dir, "json", "stock_data_export.json")

# Function to load JSON data
def load_json_data():
    if not os.path.exists(FILE_PATH):
        return []
    try:
        with open(FILE_PATH, 'r', encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                return data  # Ensure it's a list of dictionaries
            else:
                print("Error: JSON data is not a list")
                return []
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return []

# Normalize field names to match HTML input
def normalize_field_name(field_name):
    return re.sub(r'[^a-zA-Z0-9]', '_', field_name).lower()

@app.route('/')
def index():
    return render_template("Personalized_stock_filter.html")

@app.route('/load_data', methods=['GET'])
def load_data():
    """Loads the stock data and returns it as JSON."""
    data = load_json_data()
    return jsonify(data)

@app.route('/filter', methods=['POST'])
def filter_data():
    """Applies filters based on user selection and returns the filtered data."""
    data = load_json_data()
    if not data:
        return jsonify({"error": "No stock data available"}), 404

    filters = request.json
    if not filters:
        return jsonify({"error": "No filters provided"}), 400

    df = pd.DataFrame(data)

    # Normalize column names in the DataFrame
    df.columns = [normalize_field_name(col) for col in df.columns]

    for field, condition in filters.items():
        normalized_field = normalize_field_name(field)

        if normalized_field not in df.columns:
            print(f"Skipping unknown field: {normalized_field}")
            continue  # Skip fields not in the dataset

        value = condition.get("value")
        condition_type = condition.get("type")

        if value is None or condition_type is None:
            print(f"Skipping invalid filter for field: {field}")
            continue  # Skip if filter is incomplete

        # Apply numeric filters
        if condition_type in ["greater_than", "less_than"]:
            try:
                value = float(value)  # Ensure value is numeric
                df[normalized_field] = pd.to_numeric(df[normalized_field], errors="coerce")

                if condition_type == "greater_than":
                    df = df[df[normalized_field].notna() & (df[normalized_field] > value)]
                elif condition_type == "less_than":
                    df = df[df[normalized_field].notna() & (df[normalized_field] < value)]

            except ValueError:
                print(f"Skipping field {field}: Cannot convert to float")
                continue  # Skip if conversion fails

        # Apply string-based filters
        elif condition_type == "equal_to":
            df = df[df[normalized_field].astype(str) == str(value)]
        elif condition_type == "contains":
            df = df[df[normalized_field].astype(str).str.contains(str(value), case=False, na=False)]

    return jsonify(df.to_dict(orient="records"))

@app.route('/download_csv', methods=['POST'])
def download_filtered_csv():
    """Downloads the filtered stock dataset as CSV based on user-applied filters."""
    data = load_json_data()
    
    if not data:
        return jsonify({"error": "No stock data available"}), 404

    filters = request.json
    if not filters:
        return jsonify({"error": "No filters provided"}), 400

    df = pd.DataFrame(data)
    df.columns = [normalize_field_name(col) for col in df.columns]  # Normalize column names

    for field, condition in filters.items():
        normalized_field = normalize_field_name(field)

        if normalized_field not in df.columns:
            continue

        value = condition.get("value")
        condition_type = condition.get("type")

        if value is None or condition_type is None:
            continue

        # Apply filters
        if condition_type in ["greater_than", "less_than"]:
            try:
                value = float(value)
                df[normalized_field] = pd.to_numeric(df[normalized_field], errors="coerce")

                if condition_type == "greater_than":
                    df = df[df[normalized_field].notna() & (df[normalized_field] > value)]
                elif condition_type == "less_than":
                    df = df[df[normalized_field].notna() & (df[normalized_field] < value)]

            except ValueError:
                continue  # Skip invalid values

        elif condition_type == "equal_to":
            df = df[df[normalized_field].astype(str) == str(value)]
        elif condition_type == "contains":
            df = df[df[normalized_field].astype(str).str.contains(str(value), case=False, na=False)]

    # Convert DataFrame to CSV
    csv_data = df.to_csv(index=False)

    response = Response(csv_data, content_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=filtered_stock_data.csv"
    
    return response

if __name__ == '__main__':
    app.run(debug=True)
