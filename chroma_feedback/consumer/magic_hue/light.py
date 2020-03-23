from typing import Any, Dict, List
from chroma_feedback import color
from .api import get_api


def get_lights(ips : List[str]) -> List[Dict[str, Any]]:
	lights = []

	for ip in ips:
		lights.append(get_api(ip))
	return lights


def process_lights(lights : Any, status : str) -> List[Dict[str, Any]]:
	result = []

	# process lights

	for light in lights:

		if status == 'passed':
			result.append(
			{
				'consumer': 'magic_hue',
				'type': 'light',
				'name': light.name,
				'active': static_light(light, color.get_passed()),
				'status': status
			})
		if status == 'process':
			result.append(
			{
				'consumer': 'magic_hue',
				'type': 'light',
				'name': light.name,
				'active': static_light(light, color.get_process()),
				'status': status
			})
		if status == 'errored':
			result.append(
			{
				'consumer': 'magic_hue',
				'type': 'light',
				'name': light.name,
				'active': static_light(light, color.get_errored()),
				'status': status
			})
		if status == 'failed':
			result.append(
			{
				'consumer': 'magic_hue',
				'type': 'light',
				'name': light.name,
				'active': static_light(light, color.get_failed()),
				'status': status
			})
	return result


def static_light(light : Any, state : Dict[str, Any]) -> bool:
	light.mode = state['mpde']
	light.speed = 0
	return light.update_status() is None


def pulsate_light(light : Any, state : Dict[str, Any]) -> bool:
	light.mode = state['mpde']
	return light.update_status() is None
