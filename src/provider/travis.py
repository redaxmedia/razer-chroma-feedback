import requests


def fetch_data(slug):
	response = requests.get('https://api.travis-ci.org/repos/' + slug, headers =
	{
		'Accept': 'application/vnd.travis-ci.2+json'
	})
	if response.status_code == 200:
		data = response.json()
		if 'repo' in data:
			return normalize_data(data['repo'])
		if 'repos' in data:
			result = []
			for repo in data['repos']:
				result.extend(normalize_data(repo))
			return result
	return []


def normalize_data(project):
	return \
	[
		{
			'provider': 'Travis CI',
			'slug': project['slug'],
			'active': project['active'],
			'status': normalize_status(project)
		}
	]


def normalize_status(project):
	if project['last_build_finished_at'] is None:
		return 'process'
	return project['last_build_state']
