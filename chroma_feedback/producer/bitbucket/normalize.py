from typing import Any, Dict
from chroma_feedback import helper


def normalize_data(slug : str, status : str) -> Dict[str, Any]:
	return\
	{
		'producer': 'bitbucket',
		'slug': slug,
		'active': True,
		'status': normalize_status(status)
	}


def normalize_status(status : str) -> str:
	status = helper.to_lower_case(status)

	if status == 'inprogress':
		return 'started'
	if status == 'stopped':
		return 'errored'
	if status == 'failed':
		return 'failed'
	return 'passed'
