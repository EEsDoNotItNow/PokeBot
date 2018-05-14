
FROM python:3.6.5

RUN pip install pipenv
RUN mkdir /.local/share/virtualenvs/
RUN chmod +w /.local/share/virtualenvs/
