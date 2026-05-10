from flask import Flask, render_template, request
from src.pipelines.predict_pipeline import DataFormat, PredictionPipeline
import traceback
from src.logger import logging

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def predict():
    try:
        if request.method == "POST":
            logging.info("Processing POST request for prediction")
            
            # Log the form data received
            form_data = dict(request.form)
            logging.info(f"Form data received: {form_data}")
            
            data = DataFormat(
                gender=request.form.get("gender", None),
                race_ethnicity=request.form.get("race_ethnicity", None),
                parental_level_of_education=request.form.get("parental_level_of_education", None),
                lunch=request.form.get("lunch", None),
                test_preparation_course=request.form.get("test_preparation_course", None),
                reading_score=float(request.form.get("reading_score", 0)),
                writing_score=float(request.form.get("writing_score", 0)),
            )
            
            logging.info(f"DataFormat object created: {data}")
            prediction = PredictionPipeline.predict(data)
            logging.info(f"Prediction successful: {prediction}")
            
            return render_template("index.html", prediction=prediction, data=data)
        else:
            logging.info("Processing GET request")
            return render_template("index.html")
    except Exception as e:
        logging.error(f"Error in predict route: {str(e)}")
        logging.error(f"Traceback: {traceback.format_exc()}")
        return render_template("index.html", error=f"An error occurred: {str(e)}")

if __name__=="__main__":
    app.run("0.0.0.0", port=5000, debug=True)