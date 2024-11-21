
import pandas as pd
from tqdm import tqdm
from datetime import datetime

# Load the Excel file into a DataFrame
file_path = r"C:\Users\theal\MakersFund\MakersFundraising\MakersFundraising\updated_staff_data_with_games.xlsx"
df = pd.read_excel(file_path)

# Remove rows without a value in the 'experiences' column
df = df.dropna(subset=['experiences'])

# Add new columns 'years of experience' and 'start date'
df['years of experience'] = 0.0
df['start date'] = None

# Function to calculate the total years of experience and extract the start date
def process_experiences(experiences):
    total_months = 0
    current_date = datetime.now()
    
    if isinstance(experiences, list) and experiences:
        # Extract the start date from the first experience
        first_experience = experiences[0]
        start_date = datetime.strptime(first_experience['start_date'], '%Y-%m-%d')
        
        for experience in experiences:
            start_date = datetime.strptime(experience['start_date'], '%Y-%m-%d')
            end_date = experience['end_date']
            
            if end_date is None:
                end_date = current_date
            else:
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
            
            # Calculate the difference in months
            months = (end_date.year - start_date.year) * 12 + end_date.month - start_date.month
            total_months += months
        
        # Convert total months to years
        years_of_experience = total_months / 12
        return years_of_experience, first_experience['start_date']
    return 0.0, None

# Apply the transformation to the 'experiences' column
df[['years of experience', 'start date']] = df['experiences'].apply(lambda exp: process_experiences(exp)).apply(pd.Series)

# Save the updated DataFrame to an Excel file
df.to_excel("YoE Updated.xlsx", index=False)
