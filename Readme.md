# Description:
	1. Perform fake bruteforce attempt on an API
	2. Ingest data via Kinesis Data Stream
	3. Detect bruteforce attempt via Kinesis Analytics App

# Requirements:
	1. Installation of python3 libraries mentioned in 'requirements.txt'
	2. IAM permission for 'KinesisFullAccess'
	3. A Kinesis Data Stream
	4. A Kinesis Analytics App

# Execution:
	1. Execute python script to send sample data representing bruteforce attack on your APIs, via Kinesis Data Streams
	2. Use sql_code to detect bruteforce/DOS attack in Kinesis Analytics App