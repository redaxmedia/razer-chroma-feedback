from unittest.mock import MagicMock
from src import miner


def test_progress(mocker):
	args = MagicMock()
	args.host = None
	args.provider = []
	args.provider.append('appveyor')
	args.provider.append('circle')
	args.provider.append('gitlab')
	args.provider.append('jenkins')
	args.provider.append('teamcity')
	args.provider.append('travis')
	args.slug = []
	args.slug.append('one')
	args.slug.append('two')
	args.token = None
	fetch = mocker.spy(miner, 'fetch')
	miner.process(args)
	assert fetch.call_count == 12
