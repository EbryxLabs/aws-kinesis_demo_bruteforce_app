import sys
from datetime import datetime
import os
from threading import BoundedSemaphore, Thread
import time
import argparse
import boto3
import random
import json


# Global Vars
# first output file is the log file for this script
# second output file is the actual output file for this script
mSemaphores = [BoundedSemaphore(value=1)]
args = ''
default_values_dict = {'generate_records_for_seconds': 360, 'kinesis_data_stream_name': 'test-bruteforceing-ip-datastream', 'log_file': '{0}.log'.format(str(__file__)), 'number_of_records_to_send_every_second': 8}
#############


def setup_argparse():
	global args
	argparse_setup_completed_gracefully = False
	parser = argparse.ArgumentParser(
		description='''Generates and sends sample logs to a kinesis stream''',
		epilog="""All's well that ends well.""",
		usage="""python3 {0}.py""".format(str(__file__)))
	parser.add_argument('--log_file', '-l', default=default_values_dict['log_file'], required=False, help='path/to/name/of/output/file. Default is "{0}" in the same directory'.format(default_values_dict['log_file']))
	parser.add_argument('--kinesis_data_stream_name', '-kdsn', default=default_values_dict['kinesis_data_stream_name'], required=False, help='kinesis stream name to send data to. Default is "{0}"'.format(default_values_dict['kinesis_data_stream_name']))
	parser.add_argument('--generate_records_for_seconds', '-grfs', type=int, default=default_values_dict['generate_records_for_seconds'], required=False, help='Duration in seconds for which logs should be generated and sent. Default is "{0}" seconds'.format(default_values_dict['generate_records_for_seconds']))
	parser.add_argument('--number_of_records_to_send_every_second', '-nortses', type=int, default=default_values_dict['number_of_records_to_send_every_second'], required=False, help='Number of records to send every second. Default is "{0}" records'.format(default_values_dict['number_of_records_to_send_every_second']))
	args = parser.parse_args()

	# outFiles[1] = args.out

	argparse_setup_completed_gracefully = True
	print('Argparse setup complete')
	return argparse_setup_completed_gracefully


def setup_file(inFile):
	with open(inFile, 'w') as o: 
		print('Output file "{0}" has been created'.format(inFile))


def log_msg(msg):
	try:
		with open(args.log_file, 'a') as o: 
			mStr = str(msg)
			o.write('\n' +  mStr + '\n')
			print('\n' +  mStr + '\n')
	except Exception as e:
		print('Unable to write msg to log file')


def num_to_ip(random_num):
	mDict = {1: '192.168.10.1', 2: '192.168.10.2', 3: '192.168.10.3', 4: '192.168.10.4', 5: '192.168.10.5', 6: '192.168.10.6', 7: '192.168.10.7', 8: '192.168.10.8', 9: '192.168.10.9', 0: '192.168.10.0'}
	return mDict[random_num]


def num_to_uri(random_num):
	mDict = {0: 'loginn_endpoint', 1: 'signup_endpoint'}
	return mDict[random_num]


def send_sample_data_to_kinesis_stream(client, kinesis_data_stream_name, generate_records_for_seconds, number_of_records_to_send_every_second):
	total_seconds_passed = 1

	while generate_records_for_seconds > 0: # duration in seconds for which records should be generated. While records need to be generated

		records_this_second = []
		for i in range(number_of_records_to_send_every_second):
			mDict = {
				'ip': num_to_ip(random.randint(0, 9)),
				'uri': num_to_uri(random.randint(0, 1)),
				'eventTime': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
			}
			response = client.put_record(
				StreamName=kinesis_data_stream_name,
				Data=json.dumps(mDict),
				PartitionKey='1'
			)
			if response and response['ShardId']: records_this_second.append(mDict)
			# if record_ip in records_this_second:
			# 	records_this_second[irecord_ip] = records_this_second[record_ip].append('uri')
		
		log_msg('Records generated in second: "{0}"'.format(total_seconds_passed))
		for i in records_this_second:
			log_msg('Second: {0}\tIP: {1}\tURI: {2}'.format(total_seconds_passed, i['ip'], i['uri']))
		# for record in records_this_second:


		time.sleep(1) # assume that the for loop that sends records, sends all records before 1 second is finished. Therefore, sleep 1 second after each iteration of record sending
		total_seconds_passed += 1
		generate_records_for_seconds -= 1 # decrement the number of seconds that remain


def main():
	setup_argparse()
	setup_file(args.log_file)
	send_sample_data_to_kinesis_stream(boto3.client('kinesis', region_name='eu-west-1'), args.kinesis_data_stream_name, args.generate_records_for_seconds, args.number_of_records_to_send_every_second)


if __name__ == '__main__':
	mTime = [datetime.now(), 0]
	log_msg('Start Time: {0}'.format(mTime[0]))
	main()
	mTime[1] = datetime.now()
	log_msg('End Time: {0}'.format(mTime[1]))
	log_msg('Start Time: {0}'.format(mTime[0]))
	log_msg('End Time: {0}'.format(mTime[1]))
	log_msg('Time Diff: {0}'.format(mTime[1] - mTime[0]))
else:
	main()
