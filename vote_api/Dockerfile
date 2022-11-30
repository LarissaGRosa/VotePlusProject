FROM python:3.10


EXPOSE 5000

WORKDIR /vote_api

COPY . /vote_api


RUN python -m pip install --upgrade pip
RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org --no-cache-dir -r requirements.txt

CMD cd .. && python -m vote_api