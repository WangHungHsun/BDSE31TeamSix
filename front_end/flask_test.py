from flask import Flask, render_template, request, url_for
from datetime import datetime
from pathlib import Path
import uuid
import json

app = Flask(__name__)

# UPLOAD_FOLDER = (
#     Path(__file__).resolve().parent / "static/uploaded"
# )  # Path(__file__).resolve().parent為此py檔案的父資料夾
# app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
# app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB


@app.route("/")
def index():
    return render_template("index.html", page_header="page_header")





@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == "GET":
       return render_template("form.html", page_header="page_header")
    elif request.method == "POST":
        data = request.form
        # form_data=[]
        # form_name = data.get('form-name')
        # form_gender = data.get('form-gender')
        # form_age = data.get('form-age')
        # form_marital_status = data.get('form-marital-status')
        # form_education_level = data.get('form-education-level')
        # form_annual_income = data.get('form-annual-income')
        # form_income_type = data.get('form-income_type')
        # form_occupation = data.get('form-occupation')
        # form_own_realty = data.get('form-own-realty')
        # form_own_car = data.get('form-own-car')
        # form_loan_type = data.get('form-loan-type')
        # form_lona_period = data.get('form-lona-period')
        # form_amount_annuity = data.get('form-amount-annuity')
        # form_amount_credit = data.get('form-amount-credit') 
       

        # for key, value in data.items():
        #   form_data += f"{key}: {value}\n"   
        return render_template("scoring.html", data=data)

    print(data.form_name)
    
@app.route('/scoring', methods=['POST'])
def scoring():
    form_data = request.form.get('form_data')
    # Parse the form_data string to extract individual field values
    # ... Process the data as needed
    return render_template("scoring.html", form_data=form_data)



# @app.route("/rec", methods=["GET", "POST"])
# def get_file():
#     if request.method == "GET":
#         return render_template("file.html", page_header="upload hand write picture")
#     elif request.method == "POST":
#         file = request.files["file"]
#         if file:
#             filename = str(uuid.uuid4()) + "_" + file.filename
#             file.save(app.config["UPLOAD_FOLDER"] / filename)
#             predict = model.recog_digit(filename)
#         return render_template(
#             "recog_result.html",
#             page_header="hand writing digit recognition",
#             predict=predict,
#             src=url_for("static", filename=f"uploaded/{filename}"),
#         )


if __name__ == "__main__":
    app.run(debug=True)
