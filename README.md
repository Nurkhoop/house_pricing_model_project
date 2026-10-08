# Astana Apartment Price Prediction

Machine Learning Algorithms midterm project.

This project predicts apartment asking prices in Astana from real estate listing features such as area, rooms, district, floor, building age, coordinates and amenities. The project follows the midterm workflow from the course: problem definition, data understanding, cleaning, feature engineering, splitting, modelling, tuning, evaluation, error analysis and conclusions.

## Team

| Member | Technical contribution |
| --- | --- |
| Nurkhan Kuanyshov | Dataset loading, initial exploration, cleaning rules, feature engineering, notebook structure and README. |
| Bakytzhan Jangazy | Model training, evaluation, cross-validation, error analysis and presentation preparation. |

Group: SE-2431

## Project Question

Can we predict the asking price of an apartment in Astana from listing features such as area, rooms, district, floor, building age, coordinates and amenities?

- Theme: housing price estimation
- Task type: regression
- Target variable: `price`
- Modelled target: `log1p(price)`, because apartment prices are right-skewed
- Main metrics: RMSE, MAE and R2 on log-price, plus MAE in KZT and median absolute percentage error
- Midterm success criterion: the best lecture-based model should clearly beat the median-price baseline and reach about 15% or lower median percentage error

## Dataset

- Source: Kaggle, Astana Real Estate Dataset by `turarr`
- Link: https://www.kaggle.com/datasets/turarr/astana-real-estate-dataset
- Data type: real apartment listings, not synthetic data
- Topic: apartment listings in Astana scraped from Krisha.kz, current as of March 2026
- Original size in this project: 5,003 listings and 23 columns
- Cleaned size used for modelling: 4,086 listings
- Link/licence note: the dataset should be downloaded from its original Kaggle page. The CSV is intentionally not committed to this repository to avoid redistributing data without checking the dataset page terms.

Important columns used in the workflow:

| Group | Examples |
| --- | --- |
| Target | `price` |
| Size and layout | `area_m2`, `rooms`, area per room |
| Location | `district`, `district_lat`, `district_lon`, apartment coordinates where available |
| Building/floor | `current_floor`, `total_floors`, floor ratio, first/top floor flags |
| Property details | residential complex, furnished, parking, bathroom type, apartment condition, building type |
| Time/building age | year-related fields and engineered age when available |

Known dataset limitations:

- Prices are asking prices from advertisements, not final sale prices.
- Exact and near-duplicate advertisements may exist.
- Seller-entered values can contain typos, unrealistic ranges and outliers.
- Luxury apartments are harder to model because they can depend on renovation quality, view, exact building and negotiation.
- Some text/location fields are noisy or missing.

## Repository Files

| File | Purpose |
| --- | --- |
| `astana_housing_midterm.ipynb` | Main project notebook. Runs in order and contains EDA, cleaning, feature engineering, splitting, baseline, lecture models, tuning, evaluation, error analysis and conclusions. |
| `DATA.md` | Dataset download instructions and redistribution note. |
| `Astana_Housing_Midterm_Presentation2.pptx` | Midterm presentation, 12 slides. |
| `requirements.txt` | Python package requirements for running the notebook. |
| `main.py` | Small helper script for quick dataset inspection from the command line. |
| `README.md` | Project overview, setup, results, midterm coverage and next steps. |
| `.gitignore` | Keeps local environments, IDE files and the Kaggle CSV out of version control. |

## Setup

Create and activate a Python environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Download the dataset from Kaggle and place it in the project root as:

```text
astana_real_estate_dataset.csv
```

Run the notebook from the project folder:

```bash
jupyter notebook astana_housing_midterm.ipynb
```

The notebook expects `astana_real_estate_dataset.csv` to be in the same folder.

Optional quick dataset check:

```bash
python main.py
```

## Methodology

### 1. Data Loading and Initial Exploration

The notebook loads the CSV file with pandas, checks shape, column types, first rows, summary statistics, missing values and duplicated rows. This gives an initial view of numeric ranges, categorical fields and possible data quality issues.

### 2. Data Cleaning

Cleaning steps documented in the notebook:

- Convert the target price to numeric format.
- Split floor-like values when needed, for example values similar to `5 iz 9`.
- Convert object columns that are actually numeric.
- Drop identifiers, long free-text fields and columns with too many missing values.
- Drop price-like columns that would leak the target.
- Remove exact duplicates.
- Remove rows with missing target values.
- Apply realistic range checks for core numeric fields such as price, rooms, area and floors.
- Trim extreme price outliers by keeping the 1st to 99th percentile range.

### 3. Exploratory Data Analysis

The notebook includes more than four meaningful plots with short interpretations:

- Price and log-price distributions to justify modelling `log1p(price)`.
- Area vs price scatter plot to check the main size-price relationship.
- Price by district boxplot to compare location effects.
- Numeric correlation heatmap to inspect relationships between numeric features.
- Missing-value plot to document remaining missingness.
- Validation/error plots after modelling, including predicted vs actual, residuals and error by segment.

### 4. Feature Engineering

Engineered or transformed features include:

- `log1p(price)` as the model target.
- Building or apartment age features when year information is available.
- Floor ratio: current floor divided by total floors.
- First-floor and top-floor indicators.
- Area per room.
- Numeric scaling through `StandardScaler`.
- Categorical encoding through `OneHotEncoder`.
- Missing-value imputation through `SimpleImputer`.

### 5. Splitting and Leakage Control

The data is split into train, validation and test sets as 70/15/15. For regression, the split is stratified with quantile bins of log-price so cheap, middle and expensive apartments are represented in each part.

Leakage is avoided by:

- Splitting data before model fitting.
- Keeping imputation, scaling and one-hot encoding inside scikit-learn pipelines.
- Fitting preprocessing only on the training data.
- Running cross-validation and GridSearchCV on the training data only.
- Using the test set once at the final evaluation step.
- Dropping price-like columns that would directly reveal the target.

## Models

The midterm theme requires lecture-based regression models. The notebook compares:

| Model | Role |
| --- | --- |
| Median baseline (`DummyRegressor`) | Simple benchmark that always predicts the median training price. |
| Linear Regression | Lecture model and final best model in the current notebook. |
| Decision Tree Regressor | Non-linear lecture model, also tuned with GridSearchCV. |
| KNN Regressor | Distance-based lecture model, also tuned with GridSearchCV. |

Cross-validation is performed on the training data. Decision Tree and KNN are tuned with GridSearchCV. Validation curves are used to inspect where overfitting starts.

## Current Results

Validation results:

| Model | RMSE log | R2 | MAE KZT | MedAPE |
| --- | ---: | ---: | ---: | ---: |
| Baseline median | 0.500 | -0.013 | 17.9M | 33.9% |
| Linear Regression | 0.191 | 0.853 | 7.1M | 11.2% |
| Decision Tree tuned | 0.218 | 0.808 | 8.0M | 12.8% |
| KNN tuned | 0.221 | 0.802 | 7.7M | 13.4% |

Best validation model: Linear Regression.

Final test result for Linear Regression:

| Metric | Value |
| --- | ---: |
| RMSE log | 0.205 |
| MAE log | 0.155 |
| R2 | 0.838 |
| MAE KZT | 7.52M |
| MedAPE | 12.0% |

Interpretation: the best model clearly beats the baseline. The validation median percentage error improves from 33.9% to 11.2%, and the final held-out test result is 12.0% MedAPE. This satisfies the stated midterm success criterion.

## Error Analysis

The notebook checks prediction quality by price segment and district. The main observed issue is that the most expensive apartments are harder to predict. This is expected because high-end listings depend on details that are not fully captured in the dataset, such as renovation quality, view, exact building reputation and negotiation.

## Midterm Requirements Coverage

| Requirement | Status | Evidence in this project |
| --- | --- | --- |
| Clear problem statement, task type, target and success metric | Covered | README and notebook section 1 define regression, `price`, metrics and success criterion. |
| Dataset description with source, size, features, target, link and issues | Covered | README dataset section and notebook section 2. |
| EDA with at least 4 meaningful plots and interpretations | Covered | Notebook section 5 has target distribution, area-price, district-price, correlation, missingness and model error plots. |
| Data cleaning documented | Covered | Notebook section 4 documents types, ranges, duplicates, missing values, outliers and leakage columns. |
| Feature engineering with justified transformations | Covered | Notebook section 6 and README methodology section. |
| Correct train/validation/test split and leakage explanation | Covered | Notebook section 7 and README leakage-control section. |
| Baseline plus at least 2 lecture algorithms | Covered | Baseline, Linear Regression, Decision Tree and KNN. |
| Proper metrics and comparison | Covered | RMSE, MAE, R2, MAE KZT and MedAPE tables. |
| Cross-validation for at least one model | Covered | Notebook section 9. |
| Hyperparameter tuning | Covered | GridSearchCV for Decision Tree and KNN in notebook section 10. |
| Open problems and plan for final stage | Covered | Notebook section 13 and README next steps. |
| Project notebook runs in order | Mostly covered | Notebook is structured sequentially; recommended final check is executing it from a clean kernel before submission. |
| Presentation 7-12 slides | Covered | `Astana_Housing_Midterm_Presentation2.pptx` contains 12 slides. |
| README includes team, question, dataset link, setup, results and next steps | Covered | This README includes all required items. |
| Safe public GitHub submission | Covered | Dataset is linked through Kaggle and ignored locally instead of being redistributed. |
| Every member has identifiable technical contribution | Covered in README | Oral defense still needs both members to explain their parts. |

## Rubric Self-Assessment

| Criterion | Max points | Estimated coverage | Comment |
| --- | ---: | ---: | --- |
| Problem and scope | 10 | 9-10 | Clear target, task type, metrics and feasible midterm/final plan. |
| Dataset understanding | 20 | 17-19 | Good source, structure, EDA and limitations. Could be stronger if dataset licence is explicitly confirmed from Kaggle. |
| Data preparation | 20 | 18-20 | Cleaning, preprocessing and feature engineering are documented and implemented with pipelines. |
| Evaluation design | 15 | 14-15 | Correct split, CV, suitable metrics and leakage control. |
| Baseline implementation | 20 | 18-20 | Baseline plus 3 lecture models, tuning, interpretation and error analysis. |
| Presentation and defense | 10 | 8-10 | Slides meet the 7-12 slide requirement. Final score depends on timing and oral answers. |
| Team process | 5 | 4-5 | Roles are listed. Stronger evidence can be added by each member explaining their code sections in defense. |

Estimated midterm score from repository evidence: **88-99 out of 100 for project quality**, or **62-69 out of 70 if the midterm cap is applied and the defense goes well**. The main remaining risks are oral defense quality and a clean re-run of the notebook before submission.

## Open Problems

- Asking prices are not the same as real transaction prices.
- Near-duplicate advertisements may remain after exact duplicate removal.
- Some high-cardinality location and residential complex values are noisy.
- Expensive apartments have larger relative errors than most middle segments.
- The current model does not yet use advanced non-linear models for final-stage improvement.

## Next Steps for Final Defense

- Execute the notebook from a clean kernel and save the final output.
- Confirm the dataset licence/terms on Kaggle and mention it clearly in the presentation or README if required.
- Add stronger non-linear models such as Random Forest and Gradient Boosting.
- Add better location features, for example distance to the city centre.
- Add target-safe aggregate features by residential complex using only training folds.
- Analyze feature importance and prepare clearer model interpretation.
- Keep individual contribution evidence ready for the defense.
