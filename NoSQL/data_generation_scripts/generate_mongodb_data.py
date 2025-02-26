import openai
import json
from datetime import datetime
from bson import ObjectId
import time
import re
import os
import logging

# Configure OpenAI client
client = openai.OpenAI(api_key="PLACE KEY HERE")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to generate ObjectId
def generate_object_id():
    return str(ObjectId())

# Function to clean and validate JSON string
def clean_json_string(json_str: str) -> str:
    if "```" in json_str:
        pattern = r"```(?:json)?(.*?)```"
        matches = re.findall(pattern, json_str, re.DOTALL)
        if matches:
            json_str = matches[0]
    json_str = json_str.strip()
    if not json_str.startswith('['):
        json_str = '[' + json_str
    if not json_str.endswith(']'):
        json_str = json_str + ']'
    json_str = json_str.replace('\n', ' ').replace('\r', ' ')
    return json_str

# Function to generate data using GPT-4 with retry mechanism
def generate_data_with_gpt(prompt: str, max_retries: int = 3):
    for attempt in range(max_retries):
        try:
            formatted_prompt = f"""
            Please generate data exactly as specified. Your response must be a valid JSON array.
            Format: {prompt}
            Rules:
            1. Response must be a valid JSON array
            2. All string values must be properly escaped
            3. No comments or explanations, just the JSON array
            4. No markdown formatting
            5. The data generated for any field should be meaningful and related to the other collection generated if applicable.
            """
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{
                    "role": "system",
                    "content": "You are a data generation assistant for the Asian Research Network Database. Return only valid JSON arrays without any additional text or formatting."
                }, {
                    "role": "user",
                    "content": formatted_prompt
                }],
                temperature=0.4,
                max_tokens=16384
            )
            json_str = response.choices[0].message.content.strip()
            json_str = clean_json_string(json_str)
            try:
                data = json.loads(json_str)
                if not isinstance(data, list):
                    raise ValueError("Response is not a JSON array")
                return data
            except json.JSONDecodeError as je:
                print(f"JSON decode error on attempt {attempt + 1}: {str(je)}")
                print(f"Problematic JSON string: {json_str[:200]}...")
                if attempt == max_retries - 1:
                    raise
                time.sleep(2)
        except Exception as e:
            if attempt == max_retries - 1:
                raise Exception(f"Failed to generate data after {max_retries} attempts: {str(e)}")
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            time.sleep(2)

# Function to generate data in smaller batches
def generate_data_in_batches(prompt_template: str, total_count: int, batch_size: int = 50) -> list:
    all_data = []
    remaining = total_count
    while remaining > 0:
        current_batch = min(batch_size, remaining)
        batch_prompt = prompt_template.replace("<count>", str(current_batch))
        try:
            batch_data = generate_data_with_gpt(batch_prompt)
            all_data.extend(batch_data)
            remaining -= current_batch
            print(f"Generated {current_batch} records. {remaining} remaining...")
            time.sleep(1)
        except Exception as e:
            print(f"Error generating batch: {str(e)}")
            print("Reducing batch size and retrying...")
            batch_size = max(5, batch_size // 2)
            if batch_size < 5:
                raise Exception("Batch size too small, aborting")
    return all_data

# Function to generate JSON data for MongoDB
def generate_json_data(collection_name: str, data: list) -> str:
    if not data:
        return ""
    json_data = []
    for item in data:
        item['_id'] = generate_object_id()
        if collection_name == "Researcher":
            item['biography'] = {"biography": item.pop('biography', '')}  # Corrected key
            item['currentPosition'] = {"position": item.pop('currentPosition', '')}  # Corrected key
            item['academicStatus'] = {"status": item.pop('academicStatus', '')}  # Corrected key
        json_data.append(item)
    return json.dumps(json_data, indent=4)

# Function to generate data for a single collection and save to a file
def generate_collection_data(collection_name: str, prompt: str, count: int = None, batch_size: int = None):
    output_dir = 'generated_data'
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f'{collection_name.lower()}.json')
    logging.info(f"Starting data generation for {collection_name}...")
    try:
        if count and batch_size:
            data = generate_data_in_batches(prompt, count, batch_size)
        else:
            data = generate_data_with_gpt(prompt)
        json_data = generate_json_data(collection_name, data)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(json_data)
        logging.info(f"Successfully generated data for {collection_name} and saved to {output_file}")
        return True
    except Exception as e:
        logging.error(f"Error generating data for {collection_name}: {str(e)}")
        return False

# Main function to generate all mock data
def main():
    collections = [
        {
            "name": "Researcher",
            "prompt": """Generate <count> researchers with their details in this format:
            [{"_id": <ObjectId>, "firstName": "<firstName>", "middleName": "<middleInitial>", "lastName": "<lastName>", "email": "<firstName>.<lastName>@example.com", "orcID": "<randomOrcID>", "hIndex": <randomHIndex>, "totalCitations": <randomCitations>, "profileURL": "http://example.com/<firstName><lastName>", "biography": "<firstName> <lastName> is a renowned researcher in <field>.", "currentPosition": "Professor of <field>", "academicStatus": "<status>", "departmentId": "<should match with the department name generated in the departments collection>", "researchStatements": ["<researchTopic>"], "publications": ["<publicationTitle>"], "researchGroups": ["<researchGroup>"], "reviews": ["<reviewTopic>"]}]""",
            "count": 100,
            "batch_size": 25
        },
        {
            "name": "Department",
            "prompt": """Generate <count> departments with their details in this format:
            [{"_id": <ObjectId>, "name": "<departmentName>", "head": "Dr. <headFirstName> <headLastName>", "budget": <randomBudget>, "researchFocus": "<researchFocus>", "facultyCount": <randomFacultyCount>, "institutionId": "<should match the institution name generated in the institutions collection>"}]""",
            "count": 100,
            "batch_size": 25
        },
        {
            "name": "Publication",
            "prompt": """Generate <count> publications with their details in this format:
            [{"_id": <ObjectId>, "title": "<publicationTitle>", "abstract": "This paper explores <abstractTopic>.", "publicationDate": "<randomPublicationDate>", "doi": "<randomDOI>", "keywords": ["<keyword1>", "<keyword2>"], "field": "<field>", "topicId": "<topic>", "citations": ["Cited by <citationSource>"], "researchImpact": "<impact>", "venue": {"type": "<venueType>", "venueId": "<venue>"}, "datasets": ["<dataset>"]}]""",
            "count": 300,
            "batch_size": 100
        },
        {
            "name": "ResearchGroup",
            "prompt": """Generate <count> research groups with their details in this format:
            [{"_id": <ObjectId>, "name": "<groupName>", "description": "A group focused on <focusArea>.", "formationDate": "<randomFormationDate>", "leader": "Dr. <leaderFirstName> <leaderLastName>", "memberCount": <randomMemberCount>, "projectCount": <randomProjectCount>, "focusArea": "<focusArea>", "grants": ["<grant>", "<grant>"]}]""",
            "count": 50,
            "batch_size": 50
        },
        {
            "name": "FundingAgency",
            "prompt": """Generate 20 funding agencies with their details in this format:
            [{"_id": <ObjectId>, "name": "<agencyName>", "type": "<agencyType>", "totalBudget": <randomTotalBudget>, "focusArea": "<focusArea>", "successRate": <randomSuccessRate>, "countryId": "<country>"}]"""
        },
        {
            "name": "Country",
            "prompt": """Generate 50 countries in Asia with their details in this format:
            [{"_id": <ObjectId>, "name": "<countryName>", "code": "<countryCode>", "codeInt": <countryCodeInt>}]"""
        },
        {
            "name": "ResearchTopic",
            "prompt": """Generate 50 research topics with their details in this format:
            [{"_id": <ObjectId>, "name": "<topicName>", "description": "Research focused on <topicDescription>.", "popularityScore": <randomPopularityScore>, "trendIndex": <randomTrendIndex>, "parentTopicId": "<parentTopic>"}]"""
        },
        {
            "name": "Dataset",
            "prompt": """Generate 100 datasets with their details in this format:
            [{"_id": <ObjectId>, "name": "<datasetName>", "description": "A dataset for <datasetPurpose>.", "size": <randomSize>, "format": "<format>", "license": "<license>", "accessURL": "http://example.com/<datasetName>", "version": "<version>", "publicationDate": "<randomPublicationDate>"}]"""
        },
        {
            "name": "Journal",
            "prompt": """Generate 50 academic journals with their details in this format:
            [{"_id": <ObjectId>, "name": "<journalName>", "issn": "<randomISSN>", "impactFactor": <randomImpactFactor>, "publisher": "<publisher>", "frequency": "<frequency>", "scope": "<scope>", "reviewTime": <randomReviewTime>, "acceptanceRate": <randomAcceptanceRate>, "openAccessStatus": "<openAccessStatus>"}]"""
        },
        {
            "name": "Conference",
            "prompt": """Generate 50 academic conferences with their details in this format:
            [{"_id": <ObjectId>, "name": "<conferenceName>", "seriesName": "<seriesName>", "date": "<randomDate>", "location": "<location>", "ranking": <randomRanking>, "acceptanceRate": <randomAcceptanceRate>, "submissionDeadline": "<randomSubmissionDeadline>", "reviewProcess": "<reviewProcess>", "virtualHybridPhysical": "<virtualHybridPhysical>"}]"""
        },
        {
            "name": "CitationNetwork",
            "prompt": """Generate <count> citation relationships with their details in this format:
            [{"_id": <ObjectId>, "citingPublicationId": "<citingPublication>", "citedPublicationId": "<citedPublication>", "citationContext": "Referenced in <citationContext>", "citationType": "<citationType>", "citationImpact": <randomCitationImpact>}]""",
            "count": 500,
            "batch_size": 50
        },
        {
            "name": "ResearchImpact",
            "prompt": """Generate <count> research impact records with their details in this format:
            [{"_id": <ObjectId>, "description": "Impact of <impactDescription>", "publicationId": "<publication>", "field": "<field>", "citationScore": <randomCitationScore>, "fieldWeightImpact": <randomFieldWeightImpact>, "industryImpact": <randomIndustryImpact>}]""",
            "count": 300,
            "batch_size": 50
        },
        {
            "name": "ResearchStatement",
            "prompt": """Generate 100 research statements with their details in this format:
            [{"_id": <ObjectId>, "researcherId": "<researcher>", "statement": "<statement>"}]"""
        },
        {
            "name": "Review",
            "prompt": """Generate <count> reviews with their details in this format:
            [{"_id": <ObjectId>, "researcherId": "<researcher>", "publicationId": "<publication>", "reviewText": "<reviewText>", "rating": <randomRating>, "reviewDate": "<randomReviewDate>", "decision": "<decision>", "reviewerComments": "<reviewerComments>"}]""",
            "count": 500,
            "batch_size": 50
        },
        {
            "name": "Institution",
            "prompt": """Generate 50 institutions in Asia with their details in this format:
            [{"_id": <ObjectId>, "name": "<institutionName>", "type": "<institutionType>", "address": "<address>", "countryId": "<country>", "ranking": <randomRanking>, "researchBudget": <randomResearchBudget>, "departmentCount": <randomDepartmentCount>}]"""
        },
        {
            "name": "CollaborationNetwork",
            "prompt": """Generate collaboration network data for the number of institutions as above. Each institution must have one or more than one record reflecting multiple collaborations for a few institutions:
            [{"_id": <ObjectId>, "institutionId": "<institution>", "partnerCount": <randomPartnerCount>, "jointPublications": <randomJointPublications>, "successRate": <randomSuccessRate>}]"""
        },
        {
            "name": "ResearchGroupMembers",
            "prompt": """Generate <count> research group memberships with their details in this format:
            [{"_id": <ObjectId>, "researchGroupId": "<researchGroup>", "researcherId": "<researcher>", "role": "<role>"}]""",
            "count": 200,
            "batch_size": 50
        },
        {
            "name": "Grants",
            "prompt": """Generate <count> grants with their details in this format:
            [{"_id": <ObjectId>, "agencyId": "<agency>", "title": "<grantTitle>", "description": "<grantDescription>", "amount": <randomAmount>, "currencyId": "<currency>", "startDate": "<randomStartDate>", "endDate": "<randomEndDate>"}]""",
            "count": 200,
            "batch_size": 20
        },
        {
            "name": "DatasetGroup",
            "prompt": """Generate 150 dataset group mappings with their details in this format:
            [{"_id": <ObjectId>, "publicationId": "<publication>", "datasetId": "<dataset>"}]"""
        }
    ]
    for collection in collections:
        logging.info(f"Processing collection: {collection['name']}")
        if "count" in collection and "batch_size" in collection:
            generate_collection_data(collection["name"], collection["prompt"], collection["count"], collection["batch_size"])
        else:
            generate_collection_data(collection["name"], collection["prompt"])

if __name__ == "__main__":
    main()