from pathlib import Path
from staffspy import LinkedInAccount, SolverType, DriverType, BrowserType
import pandas as pd

session_file = Path(__file__).resolve().parent / "session.pkl"
account = LinkedInAccount(
    # commenting these out because 2Captcha is not reliable, so sign in with browser
    # username="myemail@gmail.com",
    # password="mypassword",
    # solver_api_key="your-api-key",
    # solver_service=SolverType.TWO_CAPTCHA,
    
    # if issues with webdriver, specify
    # driver_type=DriverType(
    #     browser_type=BrowserType.CHROME,
    #     executable_path="/Users/pc/chromedriver-mac-arm64/chromedriver"
    # ),

    session_file=str(session_file), # save login cookies to only log in once (lasts a week or so)
    log_level=1, # 0 for no logs
)

# Define companies and search terms
companies = ["King", "Supercell", "Riot Games"]
search_terms = ["Product Lead", "Designer"]

# Create a dictionary to store DataFrames for each company and search term
staff_data = {}

# Scrape staff for each company and search term
for company in companies:
    for term in search_terms:
        staff = account.scrape_staff(
            company_name=company,
            search_term=term,
            extra_profile_data=True, # fetch all past experiences, schools, & skills
            max_results=1000, # can go up to 1000
        )
        # Store the DataFrame in the dictionary with a key as "Company - SearchTerm"
        staff_data[f"{company} - {term}"] = staff

# Write all DataFrames to an Excel file with each DataFrame in a separate sheet
with pd.ExcelWriter("staff_data.xlsx") as writer:
    for sheet_name, df in staff_data.items():
        df.to_excel(writer, sheet_name=sheet_name, index=False)