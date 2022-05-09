# LSML2 Final Project «Toxic comments detection»

## Project documentation

### Design document<br>
![image](https://user-images.githubusercontent.com/74063238/167320937-b8d8654a-c3c9-4f21-b681-0bc88e289ee1.png)<br>

### Run instructions (env, commands)<br>
docker-compose up
<br><br>
 
### Architecture, metrics<br>
Accuracy on cross-validation = 0.9012, accuracy on test = 0.9017
<br><br>

### Dataset<br>
toxic_comments.csv, 159571 observations: comments in english marked as 1 (toxic) or 0 (not toxic), preprocessed with BertTokenizer.
<br><br>

### Model training code<br>
Jupyter Notebook: model_creation.ipynb;<br> model — Random Forest Classifier with hyperparameters:<br> class_weight='balanced', max_depth=None, min_samples_leaf=1, min_samples_split=3, n_estimators=120 (selected by  GridSearchCV, scoring='accuracy')
<br><br>

### Service deployment and usage instructions<br>
  - docker-compose up
  - frontend - http://localhost:5000
<br><br>

### The project corresponds to the folowing Review Criteria:<br>
1. Design document and dataset description - 1 point max
2. Model training code:<br>
   2.1. Jupyter Notebook - 1 point
3. Dockerfile:<br>
  3.1. docker-compose for full architecture:<br>
  3.1.2. asynchronous project - 2 points<br>
  3.2. client:<br>
      3.2.1. Flask - 1 point<br>
      3.2.2. HTML Frontend - 2 points<br>
  3.3. model:<br>
      3.3.2. trained from scratch - 2 points
