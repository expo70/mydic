#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
a simple dictionary regist/search application
used combined with mydic.html interface

Note: this file will be put under cgi-bin dir. but it's not actualy CGI but AJAX
"""
import sys
import json
import pymongo
from bson import ObjectId


# delete duplicates with preserving order
def uniq(input):
	output = []
	for x in input:
		if x not in output:
			output.append(x)
	return output

# ref: https://stackoverflow.com/questions/16586180/typeerror-objectid-is-not-json-serializable
class JSONEncoder(json.JSONEncoder):
	def default(self, o):
		if isinstance(o, ObjectId):
			return str(o)
		return json.JSONEncoder.default(self, o)

def main():
	output_string = "" # "" means "no errors"
	data = ""
	result = {};
	try:
		data = sys.stdin.read()
		if len(data) > 0:
			post = json.loads(data)
			conn = pymongo.MongoClient('mongodb://USER:PASS@localhost:27017/')
			db = conn.mydic
			posts = db.posts
			cmd = post.pop('cmd', None) # NOTE: post is now altered.
			if cmd=="register":
				post_id = posts.insert_one(post).inserted_id
			elif cmd=="search":
				pattern = {}
				if post['relation']=='and': # AND search
					keywords = post['word1'].split(',')
					pattern1 = {'$and':[{'word1':{'$regex':k.strip(),'$options':'i'}} for k in keywords]}
					pattern2 = {'$and':[{'word2':{'$regex':k.strip(),'$options':'i'}} for k in keywords]}
					pattern3 = {'$and':[{'relation':{'$regex':k.strip(),'$options':'i'}} for k in keywords]}
				else: # normal search
					pattern1 = {'word1':{'$regex':post['word1'],'$options':'i'}}
					pattern2 = {'word2':{'$regex':post['word1'],'$options':'i'}}
					pattern3 = {'relation':{'$regex':post['word1'],'$options':'i'}}
				
				word1match = [s for s in posts.find(pattern1)]
				word2match = [s for s in posts.find(pattern2)]
				relationmatch = [s for s in posts.find(pattern3)]
				
				private_removed = [s for s in uniq(word1match+word2match+relationmatch) if s['relation'].strip().lower()!='private']
				result.update({'match':private_removed})
			else:
				raise ValueError("Unknown command passed in json")
		result.update({'db_size': posts.count()})
	except ValueError as err:
		output_string = "ValueError: {0}".format(err) + "; data = " + data
	except pymongo.errors.PyMongoError as e:
		output_string = "PyMongoError: {0}".format(str(e))
	
	print("Content-type: application/json")
	print("\n\n")
	result.update({'output': output_string})
	print(JSONEncoder().encode(result))
	print("\n")

if __name__ == '__main__':
	main()

