import pandas as pd
from flask import Flask, request, render_template
from src.pipelines.prediction_pipeline import CustomData, PredictPipeline


app = Flask(__name__)


# Route for a home page
@app.route("/")
def index():
    return render_template("index.html")


# Route for prediction service
@app.route("/predict-data", methods=["GET", "POST"])
def predict_datapoint():
    if request.method == "GET":
        return render_template("home.html")
    else:
        data = [
            CustomData(
                Age=float(request.form.get("Age")),
                Annual_Income=float(request.form.get("Annual_Income")),
                Credit_Score=float(request.form.get("Credit_Score")),
                Loan_Amount=float(request.form.get("Loan_Amount")),
                Loan_Duration_Years=float(request.form.get("Loan_Duration_Years")),
                Number_of_Open_Accounts=int(
                    request.form.get("Number_of_Open_Accounts")
                ),
                Had_Past_Default=int(request.form.get("Had_Past_Default")),
            )
        ]
        pred_df = pd.DataFrame(data)
        print("Logged prediction request:\n", pred_df)
        predict_pipeline = PredictPipeline()
        results = predict_pipeline.predict(pred_df)
        print("Prediction completed")
        return render_template("home.html", results=results[0])


if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=8080)
    app.run(host="127.0.0.1", port=8080, debug=True)
