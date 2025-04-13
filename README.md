Automating CSV Aggregation Using AWS Lambda and S3

Project Overview -
This project demonstrates how to automate the aggregation of employee data from a CSV file uploaded to an AWS S3 bucket. The Lambda function processes the file, calculates key salary metrics, and uploads the results back to a designated S3 folder.

Features -
Automatically triggers on CSV file uploads to S3.
Processes employee data to calculate:
Highest salary and the corresponding employee.
Lowest salary and the corresponding employee.
Average salary.
Saves aggregated results in a new CSV file and uploads it to an S3 folder.


Steps to Deploy
Set Up the S3 Bucket
Create an S3 bucket with folders for the source files and aggregated results.
Prepare Lambda Function
Write the code as shared in this project.
Ensure the function has sufficient IAM roles with access to S3.
Configure S3 Event Trigger
Set up an event notification for the source bucket to trigger the Lambda function upon object creation.
Test the Function
Upload a sample CSV file (e.g., employee_info.csv).
Verify the aggregated file in the aggregated folder of the S3 bucket.
Review Results
Check the aggregated CSV file to ensure accuracy.


Prerequisites
Python 3.x
AWS account with IAM role for Lambda
AWS CLI configured
Boto3 library

Usage
Upload the employee CSV file (e.g., employee_info.csv) to the S3 bucket's source folder.
AWS Lambda automatically triggers, processes the data, and uploads the result to the aggregated folder.
Download the aggregated file and review the results.


Sample Input
employee_info.csv

ID,Name,Age,Salary
101,Ajit,25,20000
102,Virat,27,50000
103,Vijay,32,35000
104,Sharad,43,45000
105,Vinay,21,41000
106,Rohit,27,23000
107,Prasad,29,40000
108,Amey,36,32000
109,Abhijeet,37,35000
110,Rahul,28,43000

Sample Output
aggregated.csv
Metric,Value,Person
Highest Salary,50000,Virat
Lowest Salary,20000,Ajit
Average Salary,36400,N/A



