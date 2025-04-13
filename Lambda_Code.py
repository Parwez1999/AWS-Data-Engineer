import csv
import boto3
import json

def lambda_handler(event, context):
    # Check if 'Records' key exists in the event
    if 'Records' not in event or not event['Records']:
        return {
            'statusCode': 400,
            'body': "'Records' key is missing or empty in the event object"
        }

    try:
        # Safely access event details
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        object_key = event['Records'][0]['s3']['object']['key']

        # Initialize S3 client
        s3 = boto3.client('s3')

        # Download the file from S3
        download_path = f"/tmp/{object_key.split('/')[-1]}"
        s3.download_file(bucket_name, object_key, download_path)

        # Debug: Log file path
        print(f"File downloaded to: {download_path}")

        # Process the CSV file
        salaries = []
        with open(download_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            # Debug: Log column headers
            print("Column headers:", reader.fieldnames)
            
            # Ensure headers exist
            if not reader.fieldnames or 'Name' not in reader.fieldnames or 'Salary' not in reader.fieldnames:
                return {
                    'statusCode': 400,
                    'body': "CSV file is missing required 'Name' or 'Salary' columns"
                }

            for row in reader:
                try:
                    # Append cleaned data
                    name = row['Name'].strip()
                    salary = float(row['Salary'].strip())
                    salaries.append({'name': name, 'salary': salary})
                except KeyError as e:
                    print(f"Missing column in row: {e}")
                except ValueError as e:
                    print(f"Invalid data format in row: {e}")

        # Debug: Log salary data
        print("Salaries data:", salaries)

        # Calculate metrics if salary data exists
        if salaries:
            highest_salary = max(salaries, key=lambda x: x['salary'])
            lowest_salary = min(salaries, key=lambda x: x['salary'])
            average_salary_amount = sum(item['salary'] for item in salaries) / len(salaries)

            highest_salary_amount = highest_salary['salary']
            highest_salary_person = highest_salary['name']
            lowest_salary_amount = lowest_salary['salary']
            lowest_salary_person = lowest_salary['name']
        else:
            highest_salary_amount = lowest_salary_amount = average_salary_amount = 0
            highest_salary_person = lowest_salary_person = "N/A"

        # Debug: Log calculated metrics
        print(f"Highest Salary: {highest_salary_amount} ({highest_salary_person})")
        print(f"Lowest Salary: {lowest_salary_amount} ({lowest_salary_person})")
        print(f"Average Salary: {average_salary_amount}")

        # Create the aggregated CSV file
        aggregated_file_path = "/tmp/aggregated.csv"
        with open(aggregated_file_path, 'w', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Metric', 'Value', 'Person'])
            writer.writerow(['Highest Salary', highest_salary_amount, highest_salary_person])
            writer.writerow(['Lowest Salary', lowest_salary_amount, lowest_salary_person])
            writer.writerow(['Average Salary', average_salary_amount, 'N/A'])

        # Upload the aggregated CSV file to S3
        aggregated_object_key = "aggregated/aggregated.csv"
        s3.upload_file(aggregated_file_path, bucket_name, aggregated_object_key)

        return {
            'statusCode': 200,
            'body': f"Aggregated file created and uploaded to {aggregated_object_key} in bucket {bucket_name}"
        }

    except Exception as e:
        # Log and return error
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': f"An error occurred: {e}"
        }
