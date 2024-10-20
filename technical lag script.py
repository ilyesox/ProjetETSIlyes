import pandas as pd
import matplotlib.pyplot as plt
import glob

# Step 1: Load and combine CSV files
path = '/content'  # CSV files directory
all_files = glob.glob(path + "/*.csv")
df = pd.concat((pd.read_csv(f) for f in all_files))

# Filter out rows where 'operator' is "_" or 'sourceName' is "_"
df = df[(df['operator'] != '_') & (df['sourceName'] != '_')]

# Step 2: Preprocess data
df['date'] = pd.to_datetime(df['date'])
df['date_of_latest_available_version_at_date'] = pd.to_datetime(df['date_of_latest_available_version_at_date'])
df['month'] = df['date'].dt.to_period('M')

# Step 3: Aggregate data
monthly_data = df.groupby('month')['DELTA3'].agg(['median', 'quantile', lambda x: x.quantile(0.25), lambda x: x.quantile(0.75)]).rename(columns={'quantile': 'mean', '<lambda_0>': 'q1', '<lambda_1>': 'q3'})

# Step 4: Plot
plt.fill_between(monthly_data.index.astype(str), monthly_data['q1'], monthly_data['q3'], color='green', alpha=0.3)
plt.plot(monthly_data.index.astype(str), monthly_data['median'], color='green', marker='o', linestyle='-')
plt.plot(monthly_data.index.astype(str), monthly_data['mean'], color='green', linestyle='--')
plt.xticks(rotation=90)  # Rotate date labels for better visibility
plt.xlabel('Date')
plt.ylabel('Technical Lag (days)')
plt.title('Monthly Distribution of Technical Lag')
plt.grid(True)
plt.tight_layout()
plt.show()
