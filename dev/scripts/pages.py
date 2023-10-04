#!/bin python3

import requests

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
		return

	data = response.json()
	for component in data['result']['pageContext']['def']['components']:
		attr = component['attributes']
		print(attr)


def print_pages():
	results = pages()
	for r in results:
		print(r['label'])
		print(r['pageId'])
		print()

if __name__ == '__main__':
	print_pages()
