FROM node:8-alpine

ENV DATABASE_URL="sqlite:///BahnMaze.db"

RUN apk add --update \
    python3

RUN mkdir /code
WORKDIR /code
ADD . /code

RUN apk add --no-cache --virtual .build-deps \
     build-base \
     libffi-dev \
     python3-dev \
  && pip3 install --no-cache-dir -r requirements.txt \
  && apk del .build-deps

RUN yarn

EXPOSE 5000

# Command untuk development mode
CMD ["python3", "run.py"]
