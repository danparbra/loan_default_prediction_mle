# Qubika Machine Learning Engineer Challenge Solution
This repository hosts a solution for a machine learning prediction problem. It implements a classification task in order to predict if a loan is approved or not based on each client's financial characteristics. Predictions can be requested online via a web app built using Flask and containerized using Docker, ready to be deployed into a production environment. As a demo, a deployment was made using AWS ECR and EC2 instances.

## Tools used
* **DVC**: This open source tool helps tracking models and data files versions. 
* **Docker**: Containerizes the application and its dependencies and setups.
* **GitHub Actions**: For CI/CD pipeline runs.
* **Flask**: To build the web app.

Other tools considered but not implemented:
* **MLFlow**: Special for Mark to keep track of the modeling experiments and parameters and metrics of each trained model.
* **Evidently**: Open source tool to monitor model in production to detect model drifts, data drifts, etc.

## Description
To productionize this model, it was necessary to consider the steps outlined in the *model.py* file delivered by Mike. This file clearly showed three different stages: data loading, data processing and transformation, model training and predictions.

Taking this into account, the following code refactorings and additions were implemented over this *model.py* file. The results of this refactoring can be seen in the *src/components* folder:
1. Data Ingestion: The *src/components/data_ingestion.py* file loads the raw dataset and splits it into train and test sets.
2. Data transformation: In the *src/components/data_transformation.py* file, the ingested data from the previous step is read and then transformed based pn if the features are numerical or categorical. The processing object generated in this transformation (a pickle file) is stored in the *artifacts/models* folder.
3. Model training and monitoring: *src/components/model_trainer.py* file takes the transformed dataset and performs the modeling routines. The best model with the best parameters and metrics is evaluated on the test set and is serialized in a pickle file available in the *artifacts/models* folder.

Other auxiliary scripts are implemented in this *src* folder such as:
* *logger.py* file to define the logging configuration to be used across the components of the machine learning pipelines.
* *exception.py* file to define custom exceptions to catch errors in a way that is appropriate for the specific tasks at hand.
* *utils.py* to store helper functions to be used across multiple modules throughout the application.

It is required from the problem statement that this is meant to be an initial model in a series of future deployments. For this reason, to track the specific versions of the models and the data that was used to train them, I used the DVC (Data Version Control) tool. In this case, the raw dataset *dataset.csv* is tracked using DVC with its respective metadata available in the *artifacts/data* folder. The models' pickle file versions are also tracked with DVC in the *artifacts/models* folder.

Also, to enrich the modeling stage, a Random Forest Classifier model was also trained apart from Mike's Logistic Regression model. Hyperparameter tuning is implemented on each model to further enhance their predictions quality.

Once Mike's script is refactored, the construction of the web app begins. To do this, the *app.py* script uses the html forms available in the *templates* folder to get the user inputs. To process this inputs and make the predictions, the *src/pipelines/prediction_pipeline.py* defines the steps in which the prediction request should be handled.

## Considerations
* Online prediction with batch features: For simplicity I assumed that prediction are real-time, but the features are computed in batch (offline). Model training is also a batch process.
* Accuracy as performance metric: The performance metric selected to evaluate the best model was the accuracy metric because both labels in the target feature (Loan_Approval) are assumed to be equally important (Approved or not) and according to a basic EDA available in the *research* folder, the labels are not imbalanced.
* User Inteface should be a web app: To display the modeling results directly to the client a web app is built using Flask.
* One request at a time: For demostrative purposes, in this version of the web app the client can only make one request at each time.

## Deployment steps
1. Build Docker image of the source code.
2. Push the Docker image to ECR.
3. Lauch EC2 instance.
4. Pull image from ECR to EC2.
5. Launch Docker image in EC2.

## Areas of improvement
These are some additional topics and tasks to enrich the solution:
* Implement unit tests adding testing scripts in the *tests* folder and automate this testings in the CI pipeline using GitHub Actions.
* Implement retrainining tasks in the *pipelines/training_pipeline.py* file to adapt the model to learn patterns from new data. This pipeline can be triggered based on different criteria such as every certain amount of time or whenever there is a reasonable amount of new observations to be passed to the model (e.g. 100 new rows, 500 new rows, 1000 new rows).

## Demo in AWS
To show how the actual web app would look like, a URL was made available. For security reasons, this URL is meant to be accessed only by my specific IP address.