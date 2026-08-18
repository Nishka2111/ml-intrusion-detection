# ML-Based Intrusion Detection System

A machine learning-based network intrusion detection system that classifies network traffic into different types of attacks using network flow features.

## Project Overview

The system uses network traffic flow data to identify whether a network connection is benign or belongs to a specific attack category.

The machine learning pipeline includes:

- Exploratory Data Analysis
- Data preprocessing
- Feature preparation
- Class imbalance handling
- Random Forest classification
- Hyperparameter optimization
- Model evaluation
- Reusable prediction pipeline

---

## Dataset

The processed dataset contains:

- **504,063 samples**
- **78 features**
- **7 target classes**

### Attack Classes

| Encoded Label | Class |
|---|---|
| 0 | BENIGN |
| 1 | Bot |
| 2 | Brute Force |
| 3 | DDoS |
| 4 | DoS |
| 5 | PortScan |
| 6 | Web Attack |

---

# Machine Learning Pipeline

## 1. Exploratory Data Analysis

The first notebook performs exploratory analysis of the network traffic dataset.

The analysis includes:

- Dataset structure
- Feature inspection
- Missing values
- Target class distribution
- Numerical feature analysis
- Class imbalance analysis

Notebook:

```text
notebooks/01_data_exploration.ipynb

2\. Data Preprocessing
----------------------

The second notebook prepares the dataset for machine learning.

The preprocessing includes:

*   Removing unnecessary columns
    
*   Cleaning feature names
    
*   Handling missing values
    
*   Converting data into numerical features
    
*   Mapping attack labels into broader attack categories
    
*   Preparing the final model dataset
    

Notebook:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   notebooks/02_data_preprocessing.ipynb   `

The final model input contains **78 features**.

3\. Baseline Model Training
---------------------------

The third notebook trains the initial Random Forest classifier.

The dataset is divided into:

*   **80% training data**
    
*   **20% testing data**
    

This resulted in:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   Training: 403,250 samplesTesting:  100,813 samples   `

The baseline Random Forest achieved approximately:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   Accuracy: 99.73%   `

The model performed very well on the majority classes but showed weaker performance on the minority Web Attack class.

Notebook:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   notebooks/03_training.ipynb   `

4\. Class Imbalance Handling
----------------------------

The dataset contains significant class imbalance, particularly for:

*   Bot
    
*   Web Attack
    
*   Brute Force
    

SMOTE (Synthetic Minority Over-sampling Technique) was applied **only to the training data**.

After SMOTE:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   Original training set: 403,250SMOTE training set:    418,150   `

The resulting training distribution was:

ClassSamplesBENIGN119,997Bot8,500Brute Force8,498DDoS80,000DoS120,000PortScan72,655Web Attack8,500

SMOTE improved the model's ability to identify minority attack classes.

Model Optimization
==================

The fourth notebook evaluates different Random Forest configurations.

Notebook:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   notebooks/04_model_optimization.ipynb   `

Number of Trees
---------------

Different values of n\_estimators were tested:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   50100150200   `

The best overall configuration used:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   n_estimators = 150   `

Maximum Depth
-------------

The following configurations were tested:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   None2030   `

The selected configuration used:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   max_depth = 20   `

Minimum Samples per Leaf
------------------------

The following values were tested:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   124   `

The final configuration used:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   min_samples_leaf = 1   `

Final Model
===========

The final model is a Random Forest classifier with the following configuration:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   n_estimators = 150max_depth = 20min_samples_leaf = 1random_state = 42   `

The trained model is saved as:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   models/intrusion_model.pkl   `

The label encoder is saved as:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   models/label_encoder.pkl   `

Final Model Performance
=======================

The final model achieved:

MetricScoreAccuracy99.68%Macro Recall96.57%Macro F191.86%

The final model showed strong classification performance across the majority classes.

The minority Web Attack class also showed improved recall compared with the baseline model.

Feature Importance
==================

The Random Forest identified the following features among the most important:

FeatureImportanceSubflow Fwd Bytes0.0572Fwd Packet Length Max0.0466Flow IAT Max0.0367Total Length of Fwd Packets0.0336Average Packet Size0.0330Avg Bwd Segment Size0.0323Max Packet Length0.0317Fwd IAT Max0.0313Packet Length Mean0.0306Avg Fwd Segment Size0.0296

Reusable ML Code
================

The trained model has been separated from the experimentation notebooks into reusable Python modules.

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   ml/├── preprocessing.py├── predict.py├── evaluate.py└── train_rf.py   `

### preprocessing.py

Contains reusable preprocessing functions for preparing network-flow data.

### train\_rf.py

Contains the complete Random Forest training pipeline, including:

*   Dataset loading
    
*   Label encoding
    
*   Train/test splitting
    
*   Missing-value handling
    
*   SMOTE
    
*   Random Forest training
    
*   Model saving
    

### predict.py

Loads the trained model and label encoder and performs predictions on new data.

### evaluate.py

Contains evaluation utilities for calculating classification metrics.

Scripts
=======

The scripts/ directory contains executable project utilities.

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   scripts/├── generate_sample_data.py├── preprocess_data.py├── setup_database.py├── train_model.py└── test_model.py   `

Train the Model
---------------

From the project root:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python -m scripts.train_model   `

This trains the Random Forest and saves the model to:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   models/intrusion_model.pkl   `

Test the Model
--------------

Run:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python -m scripts.test_model   `

This loads the saved model and generates predictions from sample processed data.

Installation
============

Create and activate a virtual environment:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python -m venv .venv   `

Activate it on macOS/Linux:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   source .venv/bin/activate   `

Install project dependencies:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   pip install -r requirements.txt   `

Technologies Used
=================

*   Python
    
*   Pandas
    
*   NumPy
    
*   Scikit-learn
    
*   Imbalanced-learn
    
*   Joblib
    
*   PyTorch
    
*   FastAPI
    
*   Streamlit
    
*   Plotly
    
*   SQLAlchemy
    

Project Structure
=================

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   ml-intrusion-detection/│├── backend/├── frontend/│├── data/│   ├── raw/│   ├── processed/│   └── sample/│├── ml/│   ├── __init__.py│   ├── preprocessing.py│   ├── predict.py│   ├── evaluate.py│   └── train_rf.py│├── models/│   ├── intrusion_model.pkl│   └── label_encoder.pkl│├── notebooks/│   ├── 01_data_exploration.ipynb│   ├── 02_data_preprocessing.ipynb│   ├── 03_training.ipynb│   └── 04_model_optimization.ipynb│├── scripts/│   ├── generate_sample_data.py│   ├── preprocess_data.py│   ├── setup_database.py│   ├── train_model.py│   └── test_model.py│├── requirements.txt└── README.md   `

Current ML Status
=================

The machine learning pipeline can independently:

1.  Load the processed dataset
    
2.  Preprocess network-flow features
    
3.  Encode attack classes
    
4.  Handle missing values
    
5.  Apply SMOTE to the training data
    
6.  Train the optimized Random Forest
    
7.  Save the trained model
    
8.  Load the model for inference
    
9.  Generate attack predictions
    
10.  Evaluate model performance
    

ML Pipeline
===========

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   Processed Dataset        ↓Data Preprocessing        ↓Label Encoding        ↓Train/Test Split        ↓Missing Value Handling        ↓SMOTE on Training Data        ↓Random Forest Training        ↓Model Evaluation        ↓Saved Model        ↓Prediction Pipeline   `
