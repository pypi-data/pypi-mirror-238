option trader

# package development
cd option_trader/src
pip install e .
py -m build
py -m twine upload --repository pypi dist/*
docker run --restart always -p 8000:8000 docker.io/jihuang/optiontrader
docker run --restart always -p 8000:8000 --mount type=bind,source="$(pwd)"/,target=/option_trader/sites docker.io/jihuang/optiontrader

#tests
https://docs.pytest.org/en/latest/explanation/goodpractices.html

#SSH setup
https://woshub.com/connect-to-windows-via-ssh/
https://learn.microsoft.com/en-us/windows-server/administration/openssh/openssh_keymanagement
