import requests


def fetch(slug):
	response = requests.get('https://api.travis-ci.org/repos/' + slug, headers =
	{
		'Accept': 'application/vnd.travis-ci.2+json'
	})

	# process response

	if response and response.status_code == 200:
		data = response.json()
		if 'repo' in data:
			return normalize_data(data['repo'])
		if 'repos' in data:
			result = []
			for project in data['repos']:
				result.extend(normalize_data(project))
			return result
	return []


def normalize_data(project):
	return\
	[
		{
			'provider': 'travis',
			'slug': project['slug'],
			'active': project['active'],
			'status': normalize_status(project['last_build_state'])
		}
	]


def normalize_status(status):
	if status == 'started' or status == 'created':
		return 'process'
	if status == 'cancelled' or status == 'errored':
		return 'errored'
	if status == 'failed':
		return 'failed'
	return 'passed'
