FROM python:3.12.2-bullseye

# forces stderr and stdin to terminal
ENV PYTHONUNBUFFERED 1 
# set terminal
ENV TERM xterm
# required by zappa
ENV ZAPPA_RUNNING_IN_DOCKER=True

RUN mkdir /www
WORKDIR /www

RUN pip install --upgrade pip
RUN pip install poetry setuptools gevent

ENV POETRY_VIRTUALENVS_IN_PROJECT=true

# optimisation, this prevents rebuilding whole container on every change.
ADD Dshop/poetry.lock poetry.lock
ADD Dshop/pyproject.toml pyproject.toml 

# size optimisation
RUN poetry install && poetry cache clear pypi --all
ENV PATH=$PATH:/www/.venv/:/www/.venv/bin
ADD . /www
CMD [ "sh", "docker-entrypoint.sh" ]


# RUN pip install --upgrade pip
# # new version pipenv 2021.11.5.post0 is broken - pipenv run fails, django not found
# # (latest stable: 2021.5.29)
# RUN pip install pipenv==2021.5.29

# ENV PATH=$PATH:/www/.venv/:/www/.venv/bin
# # this should avoid rebuilding pipenv each time. Hopefully.
# ADD ./Pipfile /www/Pipfile
# ADD ./Pipfile.lock /www/Pipfile.lock
# ENV PIPENV_VENV_IN_PROJECT=true
# # clear after install
# RUN pipenv install && rm -rf /root/.cache
# # /this should avoid rebuilding pipenv each time. Hopefully.
# ADD supervisord.conf /etc/supervisor/supervisord.conf
# ADD supervisor_celery.conf /etc/supervisor/conf.d/celery.conf
# ADD . /www
# CMD [ "sh", "docker-entrypoint.sh" ]

# ARG BRANCH="not_set"
# ARG COMMIT=""
# LABEL branch=${BRANCH}
# LABEL commit=${COMMIT}

# ENV COMMIT_SHA=${COMMIT}
# ENV COMMIT_BRANCH=${BRANCH}
