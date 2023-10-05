#!/bin python3

import requests
import gl2f
import json

def pages():
	size = 99
	page = 1

	results = []
	while True:
		response = requests.get('https://yomo-api.girls2-fc.jp/web/v1/sites/girls2-fc/pages',
			params={
				'size': str(size),
				'page': str(page),
			},
			headers={
				'authority': 'yomo-api.girls2-fc.jp',
				'accept': 'application/json',
				'accept-language': 'en-US,en;q=0.9,ja;q=0.8',
				'origin': 'https://girls2-fc.jp',
				'referer': 'https://girls2-fc.jp/',
				'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
				'sec-ch-ua-mobile': '?0',
				'sec-ch-ua-platform': '"Windows"',
				'sec-fetch-dest': 'empty',
				'sec-fetch-mode': 'cors',
				'sec-fetch-site': 'same-site',
				'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
				'x-from': 'https://girls2-fc.jp/',
				'x-platform-id': 'web',
				'x-root-origin': 'https://girls2-fc.jp',
			})

		if not response.ok:
			break

		data = response.json()
		results += data['list']

		if data['totalCount'] <= size * data['currentPage']:
			return results
		page += 1

def boardId(pageId):
	response = requests.get(f'https://girls2-fc.jp/page-data/page/{pageId}/page-data.json')

	if not response.ok:
		return {
			'name': pageId,
			'status': 'bad response',
		}

	try:
		data = response.json()
		return {
			'name': pageId,
			'status': 'success',
			'components': data['result']['pageContext']['def']['components']
		}
	except Exception as e:
		return {
			'name': pageId,
			'status': str(e),
		}

def print_pages():
	all_pages = pages()

	results = [boardId(i) for i in map(lambda i:i['pageId'], all_pages)]
	print(json.dumps(results, indent=2))

def load():
	with open('pages.json') as f:
		return json.load(f)

def view_hbs():
	table = gl2f.board.table()
	data = load()

	keys = [i['page'] for i in table]
	intersection = [i for i in data if i['name'] in keys]

	print(json.dumps(intersection, indent=2))
	print()
	print({i['hbs']for i in sum((i['components'] for i in intersection), [])})

def filter_list(components):
	return [i for i in components if 'list' in i['hbs']]



def missing():
	table = gl2f.board.table()
	data = load()

	ids = [i['id'] for i in table]

	with_list = list(filter(lambda i: filter_list(i.get('components', [])), data))
	for i in with_list:
		print(i['name'])
		for j in i['components']:
			print(j)
		print()

	print('-'*10)

	diff = filter(lambda i: i['attr'], [
		{
			'name': i['name'],
			'attr': [j['attributes']  for j in i['components'] if 'list' in j['hbs'] and j['attributes']['board-id'] not in ids]
		}
		for i in with_list
	])

	for i in diff:
		print(i['name'])
		for j in i['attr']:
			print(j['board-id'])
		print()

if __name__ == '__main__':
	missing()
