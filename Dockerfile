FROM public.ecr.aws/lambda/python:3.12
# required by zappa
ENV ZAPPA_RUNNING_IN_DOCKER=True

WORKDIR ${LAMBDA_TASK_ROOT}

RUN pip install --upgrade pip
RUN pip install poetry setuptools gevent
# optimisation, this prevents rebuilding whole container on every change.
ADD Dshop/poetry.lock poetry.lock
ADD Dshop/pyproject.toml pyproject.toml 

# size optimisation
RUN POETRY_VIRTUALENVS_CREATE=false poetry install --no-cache --no-root
ENV PATH=$PATH:${LAMBDA_TASK_ROOT}/.venv/:${LAMBDA_TASK_ROOT}/.venv/bin
ENV PATH=$PATH:${LAMBDA_TASK_ROOT}/Dshop:${LAMBDA_TASK_ROOT}/Dshop/apps:${LAMBDA_TASK_ROOT}/Dshop/Dshop:${LAMBDA_TASK_ROOT}
# This is critical, otherwise apps not found
ENV PYTHONPATH=$PYTHONPATH:$PATH
ADD . ${LAMBDA_TASK_ROOT}
WORKDIR ${LAMBDA_TASK_ROOT}/Dshop
RUN ln -s ${LAMBDA_TASK_ROOT}/.venv .venv
WORKDIR ${LAMBDA_TASK_ROOT}
# Grab the zappa handler.py and put it in the working directory
RUN ZAPPA_HANDLER_PATH=$( \
    python -c "from zappa import handler; print (handler.__file__)" \
    ) \
    && echo $ZAPPA_HANDLER_PATH \
    && cp $ZAPPA_HANDLER_PATH ${LAMBDA_TASK_ROOT}


CMD [ "handler.lambda_handler" ]