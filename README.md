# Materials for the course "Machine Learning for Data Analytics with Python" for O'Reilly by Dr. Chester Ismay

# Course content

The major files in this repository are
- `slides_2025-04.pdf`: PDF version of the slides used in this course to motivate the code.
- `telco-customer-churn.csv`: Data for code walkthroughs, one as Comma-Separated Values and the other as a Microsoft Excel file
- `marketing_campaign.csv`: Data for student exercises.
- `exercises.ipynb`: A Jupyter Notebook with pseudocode/instructions provide to be filled in for code walkthroughs and student exercises
- `exercises_solutions.ipynb`: A Jupyter Notebook with answers to the code walkthroughs and exercises. An HTML version of these solutions is available at https://ismay-oreilly-ml.netlify.app/exercises_solutions.html and is the recommended way to view solutions.

## Recommended instructions on getting set up with Python and Jupyter Notebook

If you aren't able to do this on your machine, you may want to check out [Google Colab](https://colab.research.google.com/). 
It's a free service that allows you to run Jupyter notebooks in the cloud. 
Alternatively, I've set up some temporary notebooks on Binder [here](https://mybinder.org/v2/gh/ismayc/oreilly-ml-for-data-analytics-with-python/HEAD?urlpath=%2Fdoc%2Ftree%2Fexercises.ipynb) that you can work with online as well.

### Step 1: Install Python
- **Option 1: Anaconda Installation**:
  - **Download Anaconda**: Go to the [official Anaconda website](https://www.anaconda.com/products/distribution) and download the latest version of Anaconda for your operating system (Windows, macOS, or Linux). Anaconda conveniently installs Python, Jupyter Notebook, and many other commonly used packages for data science and machine learning.
- **Option 2: Python Installation**:
  - **Download Python**: Alternatively, you can download Python directly from the [official Python website](https://www.python.org/downloads/) and install the latest version for your operating system.

### Step 2: Launch Jupyter Notebook
- **Launch Jupyter Notebook**:
  - **Anaconda**: After installing Anaconda, open Anaconda Navigator from your Start Menu (Windows) or using the Anaconda Navigator application (macOS/Linux). In Anaconda Navigator, find Jupyter Notebook in the list of available applications and click on the "Launch" button. This will open Jupyter Notebook in your default web browser.
  - **Python Installation**: Open your command prompt (Windows) or terminal (macOS/Linux), and install Jupyter using pip:
    ```bash
    pip install notebook
    ```
    After installation, you can launch Jupyter Notebook by running:
    ```bash
    jupyter notebook
    ```

### Step 3: Install Required Libraries
- **Open Anaconda Prompt (Windows) or Terminal (macOS/Linux)** (if using Anaconda), or **open your command prompt (Windows) or terminal (macOS/Linux)** (if using Python installation).
- **Install Required Libraries using conda (Anaconda)**:
  ```bash
  conda install pandas seaborn matplotlib scikit-learn mlxtend
  ```
- **Install Required Libraries using pip** (if not using Anaconda):
  ```bash
  pip install pandas seaborn matplotlib scikit-learn mlxtend
  ```

### Step 4: Verify Installation
- **Create a new notebook**: In the Jupyter Notebook interface, click on "New" and select "Python 3" to open a new notebook.
- **Test the installation of the libraries**:
  - Import the libraries in the first cell of your notebook:
    ```python
    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt
    import seaborn as sns
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import mean_absolute_error, r2_score
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix
    from sklearn.cluster import KMeans
    from sklearn.metrics import silhouette_score
    from mlxtend.frequent_patterns import apriori, association_rules
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import cross_val_score, cross_validate
    from sklearn.model_selection import GridSearchCV
    ```
  - Run the cell (`Shift + Enter`). If no errors appear, the libraries are installed correctly.

### Additional Tips
- **Troubleshooting**: If you encounter any errors during installation, please ensure that Anaconda or Python is properly installed and up to date. If using Anaconda, you can also create a new environment and install the libraries within that environment.
- **Learning Resources**: Take advantage of Anaconda's integrated learning resources and documentation available through Anaconda Navigator. Additionally, familiarize yourself with the Jupyter Notebook interface and basic functionality by reading tutorials or watching introductory videos.
