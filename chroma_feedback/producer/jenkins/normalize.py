from typing import Any, Dict
from chroma_feedback import helper


def normalize_data(slug : str, result : str, is_building : bool) -> Dict[str, Any]:
	return\
	{
		'producer': 'jenkins',
		'slug': slug,
		'active': True,
		'status': normalize_status(result, is_building)
	}


def normalize_status(result : str, is_building: bool) -> str:
	result = helper.to_lower_case(result)

	if is_building is True:
		return 'started'
	if result in ['unstable', 'not_build']:
		return 'errored'
	if result == 'failure':
		return 'failed'
	return 'passed'
