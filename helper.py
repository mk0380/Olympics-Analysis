import numpy as np


def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['total'] = x['total'].astype('int')

    return x


def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years,country

# def data_over_time(df,col):

#     nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('index')
#     nations_over_time.rename(columns={'index': 'Edition', 'Year': col}, inplace=True)
#     return nations_over_time

def data_over_time(df, col):
    # Drop duplicate rows based on 'Year' and the specified column
    unique_df = df.drop_duplicates(['Year', col])

    # Count the occurrences of each year
    year_counts = unique_df['Year'].value_counts().reset_index()
    
    # Rename columns for clarity
    year_counts.columns = ['Year', 'Count']
    
    # Sort by the 'Year' column
    sorted_counts = year_counts.sort_values('Year')

    # Rename columns for final DataFrame
    sorted_counts.rename(columns={'Year': 'Edition', 'Count': col}, inplace=True)

    return sorted_counts



# def most_successful(df, sport):
#     temp_df = df.dropna(subset=['Medal'])

#     if sport != 'Overall':
#         temp_df = temp_df[temp_df['Sport'] == sport]

#     x = temp_df['Name'].value_counts().reset_index().head(15).merge(df, left_on='index', right_on='Name', how='left')[
#         ['index', 'Name_x', 'Sport', 'region']].drop_duplicates('index')
#     x.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)
#     return x

def most_successful(df, sport):
    # Drop rows with NaN values in 'Medal' column
    temp_df = df.dropna(subset=['Medal'])
    
    # Filter rows for the specified sport or all sports
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]
    
    # Get the top 15 names based on medal count
    top15_df = temp_df['Name'].value_counts().reset_index()
    top15_df.columns = ['Name', 'Medals']  # Rename columns to match the merge
    
    # Merge with the original DataFrame
    merged_df = top15_df.merge(df, on='Name', how='left')
    
    # Select relevant columns and drop duplicates
    result_df = merged_df[['Name', 'Medals', 'Sport', 'region']].drop_duplicates('Name')
    
    return result_df[0:100]


def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df

def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]

    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt


# def most_successful_countrywise(df, country):
#     temp_df = df.dropna(subset=['Medal'])

#     temp_df = temp_df[temp_df['region'] == country]

#     x = temp_df['Name'].value_counts().reset_index().head(10).merge(df, left_on='index', right_on='Name', how='left')[
#         ['index', 'Name_x', 'Sport']].drop_duplicates('index')
#     x.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)
#     return x

def most_successful_countrywise(df, country):
    # Drop rows with NaN values in 'Medal' column
    temp_df = df.dropna(subset=['Medal'])

    # Filter rows where the 'region' matches the selected country
    temp_df = temp_df[temp_df['region'] == country]

    # Get the top 10 names based on the count of medals
    top10_df = temp_df['Name'].value_counts().reset_index()
    
    # Rename columns for clarity
    top10_df.columns = ['Name', 'Medals']
    
    # Merge with the original DataFrame
    merged_df = top10_df.merge(df, on='Name', how='left')
    
    # Select relevant columns and drop duplicates
    result_df = merged_df[['Name', 'Medals', 'Sport']].drop_duplicates('Name')[0:10]
    
    return result_df


def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final
