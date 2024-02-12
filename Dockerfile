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
ENV PATH=$PATH:/www/Dshop:/www/Dshop/apps:/www/Dshop/Dshop:/www
# This is critical, otherwise apps not found
ENV PYTHONPATH=$PYTHONPATH:$PATH
ADD . /www
WORKDIR /www/Dshop
# important! - poetry on my machine is creating venv in project so remove. 
RUN rm -rf /www/.venv
RUN ln -s /www/.venv .venv
# /importamt
CMD [ "sh", "../docker-entrypoint.sh" ]
