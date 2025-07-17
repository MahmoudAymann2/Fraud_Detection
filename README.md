<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>DC Crime Prediction - XGBoost Project</title>
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; max-width: 900px; margin: auto; padding: 20px;">

  <h1>🚨 DC Crime Prediction Using XGBoost</h1>

  <p>
    This machine learning project aims to predict crime types in Washington, D.C. based on various features using the <strong>XGBoost</strong> classifier. 
    It tackles the real-world challenge of imbalanced datasets and low separability between classes using advanced sampling and tuning strategies.
  </p>

  <h2>📚 Dataset Description</h2>
  <p>
    The dataset comes from the <a href="https://opendata.dc.gov/" target="_blank">Open Data DC Portal</a> and contains detailed records of crime incidents reported across the city in 2024.
  </p>

  <ul>
    <li><strong>Total Rows:</strong> 44,000+ individual crime records (as of mid-2024)</li>
    <li><strong>Columns:</strong> 30+ features including date, method, offense type, location details, and demographics</li>
    <li><strong>Time Span:</strong> January 1st, 2024 – Present (ongoing collection)</li>
    <li><strong>Target Variable:</strong> <code>OFFENSE</code> – type of crime committed</li>
  </ul>

  <p>
    With tens of thousands of rows, this dataset provides a rich foundation for training crime prediction models, yet also poses real-world issues such as:
  </p>

  <ul>
    <li>Extreme class imbalance (some crimes occur much more frequently than others)</li>
    <li>High-dimensional categorical data</li>
    <li>Missing or sparse entries in some features</li>
  </ul>

  <h2>🎯 Project Objective</h2>
  <p>
    The goal is to build a model that can predict the type of crime committed given details like location, time, method, and demographics. This could help city planners, law enforcement, and policy makers better understand crime patterns and allocate resources accordingly.
  </p>

  <h2>🧠 Methods & Techniques</h2>
  <ul>
    <li><strong>Data Cleaning & Preprocessing:</strong> Handling missing data, encoding categorical variables</li>
    <li><strong>Feature Engineering:</strong> Extracted temporal patterns, geographic grouping, and simplified offense categories</li>
    <li><strong>Handling Imbalanced Classes:</strong> Used <code>SMOTETomek</code> (SMOTE + Tomek Links) to resample the training data</li>
    <li><strong>Model Used:</strong> <code>XGBClassifier</code> from XGBoost</li>
    <li><strong>Hyperparameter Tuning:</strong> Grid search on parameters like learning rate, depth, child weight, and estimators</li>
    <li><strong>Evaluation:</strong> Accuracy score and full classification report (precision, recall, F1)</li>
  </ul>

  <h2>📊 Results</h2>
  <ul>
    <li><strong>Best Accuracy Achieved:</strong> <code>30%</code> on the test set</li>
    <li>Some crime types (e.g., the most frequent) were predicted better than rare ones</li>
    <li>Significant improvement after applying <code>SMOTETomek</code> over raw imbalanced data</li>
  </ul>

  <h2>📈 Feature Importance</h2>
  <p>
    A feature importance plot was generated to identify which variables were most influential in crime prediction. Key features included:
  </p>
  <ul>
    <li>Neighborhood cluster</li>
    <li>Method of offense (gun, knife, other)</li>
    <li>Date/time components</li>
    <li>Geographic block and ward</li>
  </ul>

  <h2>📦 Tools & Libraries Used</h2>
  <ul>
    <li>Python (Pandas, NumPy, Scikit-learn)</li>
    <li>XGBoost</li>
    <li>Imbalanced-learn (SMOTE, SMOTETomek)</li>
    <li>Matplotlib for visualization</li>
  </ul>

  <h2>🚧 Limitations & Next Steps</h2>
  <ul>
    <li>Crime prediction is inherently difficult due to human behavior and randomness</li>
    <li>The model struggles with rare crimes — consider further grouping or merging of classes</li>
    <li>More advanced models (e.g., deep learning) or additional data (e.g., weather, events) may improve performance</li>
  </ul>

  <h2>🧾 License & Attribution</h2>
  <p>
    Dataset provided by <a href="https://opendata.dc.gov/" target="_blank">Open Data DC</a>. This project is for academic and educational purposes.
  </p>

</body>
</html>
