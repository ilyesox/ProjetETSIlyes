import pandas as pd

# Load the detailed data
file_path = '/content/project_provider_upgrades_downgrades results per provider.xlsx'
data = pd.read_excel(file_path)

# Aggregate the data by project
aggregated_data = data.groupby('project').agg({
    'upgrades': 'sum',
    'downgrades': 'sum'
})
aggregated_data['total changes'] = aggregated_data['upgrades'] + aggregated_data['downgrades']

# Sort the data by 'total changes' in descending order
sorted_data = aggregated_data.sort_values('total changes', ascending=False).reset_index()

# Save the sorted aggregated data to a new Excel file
output_file_path = '/content/upgrades, downgrades and changes per project (sorted).xlsx'
sorted_data.to_excel(output_file_path, index=False)

print("Data aggregated and saved successfully.")
