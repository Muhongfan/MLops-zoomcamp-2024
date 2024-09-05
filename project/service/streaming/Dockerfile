FROM public.ecr.aws/lambda/python:3.10

RUN pip install -U pip
RUN pip install pipenv

# Set the working directory inside the container
WORKDIR /app
RUN mkdir -p /app/downloads  

COPY [ "Pipfile", "Pipfile.lock", "./" ]
# COPY ../.env .env

RUN pipenv install --system --deploy

COPY lambda_function.py ./

# Set environment variables
ENV AWS_PROFILE=mac2aws
ENV RUN_ID=ccb1e1f2811a426396410a62e6c81da5
ENV EXP_ID=4
ENV PREDICTIONS_STREAM_NAME=energy_prediction

EXPOSE 9696

CMD ["lambda_function.lambda_handler"]

