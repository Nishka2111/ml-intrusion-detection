# ML-Based Intrusion Detection System

A machine learning-based network intrusion detection system that classifies network traffic into different attack categories using network flow features.

## Overview

The system uses network traffic flow data to determine whether a network connection is benign or belongs to a specific attack category. The pipeline covers exploratory data analysis, preprocessing, feature preparation, class imbalance handling, Random Forest classification, hyperparameter optimization, model evaluation, and a reusable prediction pipeline.

## Dataset

- **504,063** samples
- **78** features
- **7** target classes

| Encoded Label | Class |
|---|---|
| 0 | BENIGN |
| 1 | Bot |
| 2 | Brute Force |
| 3 | DDoS |
| 4 | DoS |
| 5 | PortScan |
| 6 | Web Attack |

## Machine Learning Pipeline

### 1. Exploratory Data Analysis
`notebooks/01_data_exploration.ipynb`

Covers dataset structure, feature inspection, missing values, target class distribution, numerical feature analysis, and class imbalance analysis.

### 2. Data Preprocessing
`notebooks/02_data_preprocessing.ipynb`

- Removes unnecessary columns
- Cleans feature names
- Handles missing values
- Converts features into numerical form
- Maps attack labels into broader attack categories
- Prepares the final model dataset (78 features)

### 3. Baseline Model Training
`notebooks/03_training.ipynb`

| Split | Samples |
|---|---|
| Training (80%) | 403,250 |
| Testing (20%) | 100,813 |

The baseline Random Forest achieved **99.73% accuracy**, performing well on majority classes but weaker on the minority Web Attack class.

### 4. Class Imbalance Handling

The dataset is significantly imbalanced, particularly for Bot, Web Attack, and Brute Force. SMOTE (Synthetic Minority Over-sampling Technique) was applied to the training data only.

| | Samples |
|---|---|
| Original training set | 403,250 |
| SMOTE training set | 418,150 |

Resulting training distribution after SMOTE:

| Class | Samples |
|---|---|
| BENIGN | 119,997 |
| Bot | 8,500 |
| Brute Force | 8,498 |
| DDoS | 80,000 |
| DoS | 120,000 |
| PortScan | 72,655 |
| Web Attack | 8,500 |

### 5. Model Optimization
`notebooks/04_model_optimization.ipynb`

Different Random Forest configurations were evaluated:

| Parameter | Values Tested | Selected |
|---|---|---|
| `n_estimators` | 50, 100, 150, 200 | 150 |
| `max_depth` | None, 20, 30 | 20 |
| `min_samples_leaf` | 1, 2, 4 | 1 |

## Final Model

```python
RandomForestClassifier(
    n_estimators=150,
    max_depth=20,
    min_samples_leaf=1,
    random_state=42
)
```

Saved artifacts:
- `models/intrusion_model.pkl`
- `models/label_encoder.pkl`

### Performance

| Metric | Score |
|---|---|
| Accuracy | 99.68% |
| Macro Recall | 96.57% |
| Macro F1 | 91.86% |

The final model showed strong performance across majority classes, with improved recall on the minority Web Attack class compared to the baseline.

### Feature Importance

| Feature | Importance |
|---|---|
| Subflow Fwd Bytes | 0.0572 |
| Fwd Packet Length Max | 0.0466 |
| Flow IAT Max | 0.0367 |
| Total Length of Fwd Packets | 0.0336 |
| Average Packet Size | 0.0330 |
| Avg Bwd Segment Size | 0.0323 |
| Max Packet Length | 0.0317 |
| Fwd IAT Max | 0.0313 |
| Packet Length Mean | 0.0306 |
| Avg Fwd Segment Size | 0.0296 |

## Project Structure

```
ml-intrusion-detection/
├── backend/
├── frontend/
├── data/
│   ├── raw/
│   ├── processed/
│   └── sample/
├── ml/
│   ├── __init__.py
│   ├── preprocessing.py
│   ├── predict.py
│   ├── evaluate.py
│   └── train_rf.py
├── models/
│   ├── intrusion_model.pkl
│   └── label_encoder.pkl
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_data_preprocessing.ipynb
│   ├── 03_training.ipynb
│   └── 04_model_optimization.ipynb
├── scripts/
│   ├── generate_sample_data.py
│   ├── preprocess_data.py
│   ├── setup_database.py
│   ├── train_model.py
│   └── test_model.py
├── requirements.txt
└── README.md
```

## Reusable ML Code

The trained model is separated from the experimentation notebooks into reusable modules under `ml/`:

| Module | Purpose |
|---|---|
| `preprocessing.py` | Reusable preprocessing functions for network-flow data |
| `train_rf.py` | Full training pipeline — loading, label encoding, splitting, missing-value handling, SMOTE, training, saving |
| `predict.py` | Loads the trained model and label encoder to run predictions on new data |
| `evaluate.py` | Classification metric utilities |

## Scripts

```
scripts/
├── generate_sample_data.py
├── preprocess_data.py
├── setup_database.py
├── train_model.py
└── test_model.py
```

**Train the model:**
```bash
python -m scripts.train_model
```
Saves the trained model to `models/intrusion_model.pkl`.

**Test the model:**
```bash
python -m scripts.test_model
```
Loads the saved model and generates predictions from sample processed data.

## Installation

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

## Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Imbalanced-learn
- Joblib
- PyTorch
- FastAPI
- Streamlit
- Plotly
- SQLAlchemy

## Pipeline Flow

```
Processed Dataset
      ↓
Data Preprocessing
      ↓
Label Encoding
      ↓
Train/Test Split
      ↓
Missing Value Handling
      ↓
SMOTE on Training Data
      ↓
Random Forest Training
      ↓
Model Evaluation
      ↓
Saved Model
      ↓
Prediction Pipeline
```