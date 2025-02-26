#!/usr/bin/env python3

import re
import json
import os
from datetime import datetime
from bson import ObjectId
from typing import Dict, List, Any, Optional

class SQLToMongoDBConverter:
    def __init__(self):
        self.output_dir = 'output'
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        # Store all records from SQL files
        self.sql_data = {}
        
        # Store ObjectId mappings
        self.id_mappings = {}
        
        # Store relationship mappings
        self.relationships = {
            'researcher_publications': {},  # ResearcherID -> [PublicationIDs]
            'researcher_groups': {},       # ResearcherID -> [GroupIDs]
            'researcher_reviews': {},      # ResearcherID -> [ReviewIDs]
            'researcher_statements': {},   # ResearcherID -> [StatementIDs]
            'publication_datasets': {},    # PublicationID -> [DatasetIDs]
            'publication_citations': {},   # PublicationID -> [CitationIDs]
            'group_members': {},          # GroupID -> [ResearcherIDs]
            'group_grants': {}            # GroupID -> [GrantIDs]
        }
    
    def load_all_sql_files(self, directory='.'):
        """First load all SQL files to build relationships"""
        for file in os.listdir(directory):
            if file.endswith('.sql'):
                with open(os.path.join(directory, file), 'r', encoding='utf-8') as f:
                    content = f.read()
                table_name, records = self.parse_sql_insert(content)
                self.sql_data[table_name] = records
                
                # Generate ObjectIds for each record
                for record in records:
                    id_field = next((k for k in record.keys() if k.endswith('ID')), None)
                    if id_field:
                        self.id_mappings[f"{table_name}.{record[id_field]}"] = str(ObjectId())
        
        # Build relationships after loading all data
        self.build_relationships()
    
    def build_relationships(self):
        """Build all relationships between entities"""
        # PublicationNetwork -> Researcher-Publication relationships
        if 'PublicationNetwork' in self.sql_data:
            for record in self.sql_data['PublicationNetwork']:
                researcher_id = record['ResearcherID']
                publication_id = record['PublicationID']
                if researcher_id not in self.relationships['researcher_publications']:
                    self.relationships['researcher_publications'][researcher_id] = []
                self.relationships['researcher_publications'][researcher_id].append(publication_id)
        
        # ResearchGroupMembers -> Researcher-Group relationships
        if 'ResearchGroupMembers' in self.sql_data:
            for record in self.sql_data['ResearchGroupMembers']:
                researcher_id = record['ResearcherID']
                group_id = record['ResearchGroupID']
                if researcher_id not in self.relationships['researcher_groups']:
                    self.relationships['researcher_groups'][researcher_id] = []
                self.relationships['researcher_groups'][researcher_id].append(group_id)
                if group_id not in self.relationships['group_members']:
                    self.relationships['group_members'][group_id] = []
                self.relationships['group_members'][group_id].append(researcher_id)
        
        # Review -> Researcher-Review relationships
        if 'Review' in self.sql_data:
            for record in self.sql_data['Review']:
                researcher_id = record['ResearcherID']
                if researcher_id not in self.relationships['researcher_reviews']:
                    self.relationships['researcher_reviews'][researcher_id] = []
                self.relationships['researcher_reviews'][researcher_id].append(record['ReviewID'])
        
        # ResearchStatement -> Researcher-Statement relationships
        if 'ResearchStatement' in self.sql_data:
            for record in self.sql_data['ResearchStatement']:
                researcher_id = record['ResearchID']
                if researcher_id not in self.relationships['researcher_statements']:
                    self.relationships['researcher_statements'][researcher_id] = []
                self.relationships['researcher_statements'][researcher_id].append(record['ResearchStatementID'])
        
        # DatasetGroup -> Publication-Dataset relationships
        if 'DatasetGroup' in self.sql_data:
            for record in self.sql_data['DatasetGroup']:
                pub_id = record['PublicationID']
                if pub_id not in self.relationships['publication_datasets']:
                    self.relationships['publication_datasets'][pub_id] = []
                self.relationships['publication_datasets'][pub_id].append(record['DatasetID'])
    
    def get_reference_ids(self, table: str, original_id: Any) -> List[str]:
        """Get MongoDB ObjectIds for references"""
        if not original_id:
            return []
        if isinstance(original_id, list):
            return [self.id_mappings.get(f"{table}.{id}", str(ObjectId())) for id in original_id]
        return [self.id_mappings.get(f"{table}.{original_id}", str(ObjectId()))]
    
    def convert_researcher(self, record: Dict) -> Dict:
        """Convert Researcher record to MongoDB format"""
        doc = {
            '_id': ObjectId(self.id_mappings[f"Researcher.{record['ResearcherID']}"]),
            'firstName': record['FirstName'],
            'middleName': record.get('MiddleName', ''),
            'lastName': record['LastName'],
            'email': record['Email'],
            'orcID': record.get('OrcID', ''),
            'hIndex': record.get('HIndex', 0),
            'totalCitations': record.get('TotalCitations', 0),
            'profileURL': record.get('ProfileURL', ''),
            
            # Embedded documents
            'biography': {'biography': self.get_biography(record['ResearcherID'])},
            'currentPosition': {'position': self.get_current_position(record['ResearcherID'])},
            'academicStatus': {'status': self.get_academic_status(record['ResearcherID'])},
            
            # References
            'departmentId': self.get_reference_ids('Department', record['DepartmentID'])[0],
            'researchStatements': self.get_reference_ids('ResearchStatement', 
                self.relationships['researcher_statements'].get(record['ResearcherID'], [])),
            'publications': self.get_reference_ids('Publication',
                self.relationships['researcher_publications'].get(record['ResearcherID'], [])),
            'researchGroups': self.get_reference_ids('ResearchGroup',
                self.relationships['researcher_groups'].get(record['ResearcherID'], [])),
            'reviews': self.get_reference_ids('Review',
                self.relationships['researcher_reviews'].get(record['ResearcherID'], []))
        }
        return doc
    
    def convert_publication(self, record: Dict) -> Dict:
        """Convert Publication record to MongoDB format"""
        doc = {
            '_id': ObjectId(self.id_mappings[f"Publication.{record['PublicationID']}"]),
            'title': record['Title'],
            'abstract': record['Abstract'],
            'publicationDate': record['PublicationDate'],
            'doi': record.get('DOI', ''),
            'keywords': record.get('Keywords', '').split(',') if record.get('Keywords') else [],
            'field': record['Field'],
            'topicId': self.get_reference_ids('ResearchTopic', record['TopicID'])[0],
            
            # References
            'citations': self.get_reference_ids('CitationNetwork',
                self.relationships['publication_citations'].get(record['PublicationID'], [])),
            'researchImpact': self.get_reference_ids('ResearchImpact', record['PublicationID'])[0],
            'venue': self.get_venue_reference(record),
            'datasets': self.get_reference_ids('Dataset',
                self.relationships['publication_datasets'].get(record['PublicationID'], []))
        }
        return doc
    
    def get_venue_reference(self, record: Dict) -> Dict:
        """Get venue reference for publication"""
        if record.get('ConferenceID'):
            return {
                'type': 'conference',
                'venueId': self.get_reference_ids('Conference', record['ConferenceID'])[0]
            }
        elif record.get('JournalID'):
            return {
                'type': 'journal',
                'venueId': self.get_reference_ids('Journal', record['JournalID'])[0]
            }
        return {'type': 'unknown', 'venueId': str(ObjectId())}
    
    def get_biography(self, researcher_id: Any) -> str:
        """Get biography for researcher"""
        if 'Biography' in self.sql_data:
            for bio in self.sql_data['Biography']:
                if bio['BiographyId'] == researcher_id:
                    return bio['Biography']
        return ''
    
    def get_current_position(self, researcher_id: Any) -> str:
        """Get current position for researcher"""
        if 'CurrentPosition' in self.sql_data:
            for pos in self.sql_data['CurrentPosition']:
                if pos['CurrentPositionID'] == researcher_id:
                    return pos['CurrentPosition']
        return ''
    
    def get_academic_status(self, researcher_id: Any) -> str:
        """Get academic status for researcher"""
        if 'AcademicStatus' in self.sql_data:
            for status in self.sql_data['AcademicStatus']:
                if status['AcademicStatusID'] == researcher_id:
                    return status['AcademicStatus']
        return ''
    
    def parse_sql_insert(self, content: str) -> tuple:
        """Parse SQL INSERT statement"""
        # Extract table name
        table_match = re.search(r'INSERT\s+INTO\s+`?(\w+)`?', content, re.IGNORECASE)
        if not table_match:
            raise ValueError("Could not find table name in SQL")
        table_name = table_match.group(1)
        
        # Extract column names
        columns_match = re.search(r'\(([\s\n]*(?:`?\w+`?(?:\s*,\s*|\s*\n\s*)?)+[\s\n]*)\)', content, re.IGNORECASE)
        if not columns_match:
            raise ValueError("Could not find columns in SQL")
        columns = [col.strip('` \n\r\t') for col in re.split(r'\s*,\s*|\s*\n\s*', columns_match.group(1)) if col.strip()]
        
        # Extract values
        values_pattern = r'\(([^)]+)\)'
        values_matches = re.finditer(values_pattern, content)
        
        records = []
        for match in values_matches:
            values = self.parse_values(match.group(1))
            if len(values) == len(columns):
                record = dict(zip(columns, values))
                records.append(record)
        
        return table_name, records
    
    def parse_values(self, values_str: str) -> List:
        """Parse SQL values"""
        values = []
        current = ''
        in_quotes = False
        quote_char = None
        
        for char in values_str:
            if char in ["'", '"']:
                if not in_quotes:
                    in_quotes = True
                    quote_char = char
                elif quote_char == char:
                    in_quotes = False
                    quote_char = None
                current += char
            elif char == ',' and not in_quotes:
                values.append(self.convert_value(current.strip()))
                current = ''
            else:
                current += char
        
        if current:
            values.append(self.convert_value(current.strip()))
        
        return values
    
    def convert_value(self, value: str) -> Any:
        """Convert SQL value to appropriate Python type"""
        if not value or value.lower() == 'null':
            return None
            
        # Remove quotes and handle escaped quotes
        if (value.startswith("'") and value.endswith("'")) or \
           (value.startswith('"') and value.endswith('"')):
            value = value[1:-1].replace("\\'", "'").replace('\\"', '"')
        
        # Try converting to number
        try:
            if '.' in value:
                return float(value)
            return int(value)
        except ValueError:
            pass
        
        # Try converting to date
        date_formats = ['%Y-%m-%d', '%Y-%m-%d %H:%M:%S']
        for fmt in date_formats:
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                continue
        
        return value.strip()
    
    def convert_directory(self):
        """Convert all SQL files following the schema"""
        try:
            # First load all SQL files to build relationships
            self.load_all_sql_files()
            
            # Now convert each collection according to schema
            for table, records in self.sql_data.items():
                output_docs = []
                
                if table == 'Researcher':
                    output_docs = [self.convert_researcher(record) for record in records]
                elif table == 'Publication':
                    output_docs = [self.convert_publication(record) for record in records]
                # Add other table conversions here...
                
                if output_docs:
                    output_file = os.path.join(self.output_dir, f"{table.lower()}.json")
                    with open(output_file, 'w', encoding='utf-8') as f:
                        json.dump(output_docs, f, default=str, indent=2)
                    print(f"Converted {table}: {len(output_docs)} documents")
            
            print("\nConversion complete!")
            
        except Exception as e:
            print(f"Error during conversion: {str(e)}")
            raise

if __name__ == "__main__":
    converter = SQLToMongoDBConverter()
    converter.convert_directory()
