# question_builder.py
import json

json_file = open('question1.json')
json_data = json_file.read()
data = json.loads(json_data) # deserialises it

workhseet = []    
for i in data:
	q = {}
	q['question'] = i['question']
	q['rank'] = i['rank']
	q['type'] = i['type']
	
	opts = dict((k, v) for k,v in sorted(i.iteritems()) if k.startswith('option'))
	q['options'] = opts
	# print 'NEW JSON -> %s' % q
	workhseet.append(json.dumps(q))

print workhseet

json_file.close()