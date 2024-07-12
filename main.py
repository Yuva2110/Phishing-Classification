<<<<<<< HEAD
from wsgiref import simple_server
from flask import Flask, request
from flask import Response
import os
from flask_cors import CORS, cross_origin
from prediction_Validation_Insertion import pred_validation
from trainingModel import trainModel
from training_Validation_Insertion import train_validation
import flask_monitoringdashboard as dashboard
from predictFromModel import prediction

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
dashboard.bind(app)
CORS(app)



@app.route("/predict", methods=['POST'])
@cross_origin()
def predictRouteClient():
    try:
        if request.json['folderPath'] is not None:
            path = request.json['folderPath']

            pred_val = pred_validation(path) #object initialization

            pred_val.prediction_validation() #calling the prediction_validation function

            pred = prediction(path) #object initialization

            # predicting for dataset present in database
            path = pred.predictionFromModel()
            return Response("Prediction File created at %s!!!" % path)

    except ValueError:
        return Response("Error Occurred! %s" %ValueError)
    except KeyError:
        return Response("Error Occurred! %s" %KeyError)
    except Exception as e:
        return Response("Error Occurred! %s" %e)



@app.route("/train", methods=['POST'])
@cross_origin()
def trainRouteClient():

    try:
        if request.json['folderPath'] is not None:
            path = request.json['folderPath']
            train_valObj = train_validation(path) #object initialization

            train_valObj.train_validation()#calling the training_validation function


            trainModelObj = trainModel() #object initialization
            trainModelObj.trainingModel() #training the model for the files in the table


    except ValueError:

        return Response("Error Occurred! %s" % ValueError)

    except KeyError:

        return Response("Error Occurred! %s" % KeyError)

    except Exception as e:

        return Response("Error Occurred! %s" % e)
    return Response("Training successfull!!")

port = int(os.getenv("PORT"))
if __name__ == "__main__":
    host = '0.0.0.0'
    #port = 5000
    httpd = simple_server.make_server(host, port, app)
    print("Serving on %s %d" % (host, port))
    httpd.serve_forever()
=======
# from wsgiref import simple_server
# from flask import Flask, request
# from flask import Response
# import os
# from flask_cors import CORS, cross_origin
# from prediction_Validation_Insertion import pred_validation
# from trainingModel import trainModel
# from training_Validation_Insertion import train_validation
# import flask_monitoringdashboard as dashboard
# from predictFromModel import prediction

# os.putenv('LANG', 'en_US.UTF-8')
# os.putenv('LC_ALL', 'en_US.UTF-8')

# app = Flask(__name__)
# dashboard.bind(app)
# CORS(app)



# @app.route("/predict", methods=['POST'])
# @cross_origin()
# def predictRouteClient():
#     try:
#         if request.json['folderPath'] is not None:
#             path = request.json['folderPath']

#             pred_val = pred_validation(path) #object initialization

#             pred_val.prediction_validation() #calling the prediction_validation function

#             pred = prediction(path) #object initialization

#             # predicting for dataset present in database
#             path = pred.predictionFromModel()
#             return Response("Prediction File created at %s!!!" % path)

#     except ValueError:
#         return Response("Error Occurred! %s" %ValueError)
#     except KeyError:
#         return Response("Error Occurred! %s" %KeyError)
#     except Exception as e:
#         return Response("Error Occurred! %s" %e)



# @app.route("/train", methods=['POST'])
# @cross_origin()
# def trainRouteClient():

#     try:
#         if request.json['folderPath'] is not None:
#             path = request.json['folderPath']
#             train_valObj = train_validation(path) #object initialization

#             train_valObj.train_validation()#calling the training_validation function


#             trainModelObj = trainModel() #object initialization
#             trainModelObj.trainingModel() #training the model for the files in the table


#     except ValueError:

#         return Response("Error Occurred! %s" % ValueError)

#     except KeyError:

#         return Response("Error Occurred! %s" % KeyError)

#     except Exception as e:

#         return Response("Error Occurred! %s" % e)
#     return Response("Training successfull!!")

# port = int(os.getenv("PORT"))
# if __name__ == "__main__":
#     host = '0.0.0.0'
#     #port = 5000
#     httpd = simple_server.make_server(host, port, app)
#     print("Serving on %s %d" % (host, port))
#     httpd.serve_forever()
from wsgiref import simple_server
from flask import Flask, request, Response
from flask_cors import CORS
import os
import logging
from prediction_Validation_Insertion import pred_validation
from trainingModel import trainModel
from training_Validation_Insertion import train_validation
import flask_monitoringdashboard as dashboard
from predictFromModel import prediction

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(message)s',
                    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()])
logger = logging.getLogger(__name__)

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
dashboard.bind(app)
CORS(app)

@app.route("/predict", methods=['POST'])
@cross_origin()
def predictRouteClient():
    logger.info("Received prediction request")
    try:
        if 'folderPath' in request.json and request.json['folderPath'] is not None:
            path = request.json['folderPath']

            pred_val = pred_validation(path)  # object initialization
            pred_val.prediction_validation()  # calling the prediction_validation function

            pred = prediction(path)  # object initialization
            path = pred.predictionFromModel()  # predicting for dataset present in database
            logger.info(f"Prediction successful, file created at {path}")
            return Response(f"Prediction File created at {path}!!!", status=200)
    except Exception as e:
        logger.error(f"Error during prediction: {e}")
        return Response("Error Occurred!", status=400)

@app.route("/train", methods=['POST'])
@cross_origin()
def trainRouteClient():
    logger.info("Received training request")
    try:
        if 'folderPath' in request.json and request.json['folderPath'] is not None:
            path = request.json['folderPath']
            train_valObj = train_validation(path)  # object initialization
            train_valObj.train_validation()  # calling the training_validation function

            trainModelObj = trainModel()  # object initialization
            trainModelObj.trainingModel()  # training the model for the files in the table
            logger.info("Training successful!")
            return Response("Training successful!!", status=200)
    except Exception as e:
        logger.error(f"Error during training: {e}")
        return Response("Error Occurred!", status=400)

port = int(os.getenv("PORT", 5000))  # Default to 5000 if PORT env var is not set
if __name__ == "__main__":
    host = '0.0.0.0'
    httpd = simple_server.make_server(host, port, app)
    logger.info(f"Serving on {host} {port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("Shutdown requested...exiting")
        httpd.shutdown()
>>>>>>> 209b4427b07766e3b33fe42f325614335a16fd71
