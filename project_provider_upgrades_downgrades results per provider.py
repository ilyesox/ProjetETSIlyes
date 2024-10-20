import pandas as pd
import os
import glob

def calculate_changes(df):
    df = df.sort_values(by='date')
    df[['prev_major', 'prev_minor', 'prev_patch']] = df[['major', 'minor', 'patch']].shift(1)

    def compare_versions(row):
        if row['major'] > row['prev_major']:
            return 'upgrade'
        elif row['major'] < row['prev_major']:
            return 'downgrade'
        else:
            if row['minor'] > row['prev_minor']:
                return 'upgrade'
            elif row['minor'] < row['prev_minor']:
                return 'downgrade'
            else:
                if row['patch'] > row['prev_patch']:
                    return 'upgrade'
                elif row['patch'] < row['prev_patch']:
                    return 'downgrade'
                else:
                    return 'no change'

    df['change_type'] = df.apply(compare_versions, axis=1)
    return df

def analyze_csv(file_path):
    data = pd.read_csv(file_path)
    data = data[data['blockType'] == 'provider']
    data = data[data['sourceName'] != '_']
    data = data[~((data['major'] == -1) & (data['minor'] == -1) & (data['patch'] == -1))]
    data.loc[:, 'patch'] = data['patch'].replace(-1, 0)
    data.loc[:, ['major', 'minor', 'patch']] = data[['major', 'minor', 'patch']].fillna(0).astype(int)

    if data.empty:
        return pd.DataFrame(), os.path.basename(file_path).split('versioning')[0].strip('_')

    results = data.groupby(['workingDirectory', 'sourceName']).apply(calculate_changes).reset_index(drop=True)

    if 'change_type' not in results.columns:
        results['change_type'] = pd.Series(['no change'] * len(results))

    summary = results.groupby(['sourceName', 'change_type']).size().unstack(fill_value=0)
    summary = summary.reindex(columns=['upgrade', 'downgrade'], fill_value=0)

    project_name = os.path.basename(file_path).split('versioning')[0].strip('_')
    return summary, project_name

directory_path = '/content'
file_paths = glob.glob(os.path.join(directory_path, '*.csv'))
all_projects_summary = {}

for file_path in file_paths:
    summary, project_name = analyze_csv(file_path)
    if project_name in all_projects_summary:
        all_projects_summary[project_name] = all_projects_summary[project_name].add(summary, fill_value=0)
    else:
        all_projects_summary[project_name] = summary

consolidated_results = []
total_per_provider = pd.DataFrame()

for project, summary in all_projects_summary.items():
    total_per_provider = total_per_provider.add(summary, fill_value=0)

total_per_provider['total_changes'] = total_per_provider['upgrade'] + total_per_provider['downgrade']

for project, summary in all_projects_summary.items():
    for provider, row in summary.iterrows():
        consolidated_results.append({
            'project': project,
            'provider': provider,
            'upgrades': int(row['upgrade']),
            'downgrades': int(row['downgrade']),
            'total upgrades in the project': summary['upgrade'].sum(),
            'total downgrades in the project': summary['downgrade'].sum(),
            'total changes in the project': summary['upgrade'].sum() + summary['downgrade'].sum(),
            'total upgrades of the provider across all projects': total_per_provider.at[provider, 'upgrade'],
            'total downgrades of the provider across all projects': total_per_provider.at[provider, 'downgrade'],
            'total changes of the provider across all projects': total_per_provider.at[provider, 'total_changes']
        })

df_results = pd.DataFrame(consolidated_results)
output_path = '/content/project_provider_upgrades_downgrades.csv'
df_results.to_csv(output_path, index=False)
print(f"Data written to {output_path}")
