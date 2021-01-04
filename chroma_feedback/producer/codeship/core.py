from typing import Any, Dict, List
from argparse import ArgumentParser
import base64
from chroma_feedback import helper, request
from .normalize import normalize_data

ARGS = None


def init(program : ArgumentParser) -> None:
	global ARGS

	if not ARGS:
		program.add_argument('--codeship-host', default = 'https://api.codeship.com')
		program.add_argument('--codeship-slug', action = 'append')
		program.add_argument('--codeship-username', required = True)
		program.add_argument('--codeship-password', required = True)
	ARGS = helper.get_first(program.parse_known_args())


def run() -> List[Dict[str, Any]]:
	result = []

	if ARGS.codeship_slug:
		for slug in ARGS.codeship_slug:
			result.extend(fetch(ARGS.codeship_host, slug, ARGS.codeship_username, ARGS.codeship_password))
	else:
		result.extend(fetch(ARGS.codeship_host, None, ARGS.codeship_username, ARGS.codeship_password))
	return result


def fetch(host : str, slug : str, username : str, password : str) -> List[Dict[str, Any]]:
	result = []
	auth = fetch_auth(host, username, password)

	if 'organizations' in auth and 'token' in auth:
		for organization in auth['organizations']:
			result.extend(fetch_projects(host, organization['uuid'], slug, auth['token']))
	return result


def fetch_auth(host : str, username : str, password : str) -> Dict[str, Any]:
	result = {}
	response = None

	if host and username and password:
		username_password = username + ':' + password
		response = request.post(host + '/v2/auth', headers =
		{
			'Accept': 'application/json',
			'Authorization': 'Basic ' + base64.b64encode(username_password.encode('utf-8')).decode('ascii')
		})

	# process response

	if response and response.status_code == 200:
		data = request.parse_json(response)

		if 'access_token' and 'organizations' in data:
			result['token'] = data['access_token']
			result['organizations'] = data['organizations']
	return result


def fetch_projects(host : str, organization : str, slug : str, token : str) -> List[Dict[str, Any]]:
	result = []
	response = None

	if host and organization and token:
		response = request.get(host + '/v2/organizations/' + organization + '/projects', headers =
		{
			'Accept': 'application/json',
			'Authorization': 'Bearer ' + token
		})

	# process response

	if response and response.status_code == 200:
		data = request.parse_json(response)

		if 'projects' in data:
			for project in data['projects']:
				project_id = str(project['id'])
				if not slug or slug == project_id:
					result.extend(fetch_builds(host, organization, project['uuid'], token))
	return result


def fetch_builds(host : str, organization : str, project : str, token : str) -> List[Dict[str, Any]]:
	result = []
	response = None

	if host and organization and project and token:
		response = request.get(host + '/v2/organizations/' + organization + '/projects/' + project + '/builds', headers =
		{
			'Accept': 'application/json',
			'Authorization': 'Bearer ' + token
		})

	# process response

	if response and response.status_code == 200:
		data = request.parse_json(response)

		if 'builds' in data:
			build = helper.get_first(data['builds'])
			if build:
				result.append(normalize_data(build))
	return result
