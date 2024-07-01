import requests
from bs4 import BeautifulSoup
import csv

def scrape_election_results(url):

    response = requests.get(url)
    if response.status_code == 200:
 
        soup = BeautifulSoup(response.content, 'html.parser')

        table = soup.find('table', class_='rslt-table table-responsive')
    
        if table:
      
            election_results = []

            for row in table.find_all('tr'):
           
                columns = row.find_all('td')
                if columns:  # Check if row is not empty
                    electioon_year = columns[1].text.strip()
                    state_name = columns[2].text.strip()
                    contituency_name= columns[3].text.strip()
                    constituency_type: = columns[4].text.strip()
                    party_name= columns[5].text.strip()
                    candidate_name= columns[6].text.strip()
                    EVM_votes: = columns[7].text.strip()
                    postal_votes= columns[8].text.strip()
                    total_votes= columns[9].text.strip()
                    rank= columns[10].text.strip()
                    units= columns[11].text.strip()
                    
                    # Store the data in a dictionary
                    result = {
                        'electioon_year':electioon_year ,
                        'state_name': state_name,
                        'contituency_name':contituency_name,
                        'constituency_type': constituency_type,
                        'party_name': party_name,
                        'candidate_name': candidate_name,
                        'EVM_votes':EVM_votes,
                        'postal_votes': postal_votes,
                        'total_votes': total_votes,
                        'rank': rank,
                        'units': units
                    }
                    
                    
                    election_results.append(result)
            
            return election_results
        
        else:
            print(f"No election results table with class 'rslt-table table-responsive' found on the page: {url}")
            return None
    
    else:
        print(f"Failed to retrieve page: {url}")
        return None


def main():
    url = 'https://results.eci.gov.in/PcResultGenJune2024/index.htm'  # Replace with actual URL of election results page
    

    results = scrape_election_results(url)
    
    if results:
     
        for result in results:
            print(result)
        
     
        with open('election_results.csv', mode='w', newline='', encoding='utf-8') as file:
            fieldnames = ['electioon_year','state_name', 'contituency_name','constituency_type','party_name','candidate_name','EVM_votes','postal_votes','total_votes', 'rank','units']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            writer.writeheader()
            for result in results:
                writer.writerow(result)
        
        print("Election results saved to 'election_results.csv'")
    
    else:
        print("No election results found or failed to retrieve data.")

if __name__ == "__main__":
    main()

