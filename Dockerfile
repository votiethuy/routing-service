FROM python:3.6

ENV PROJ_PATH /opt/athena

RUN mkdir -p ${PROJ_PATH} /var/log/athena ${PROJ_PATH}/data

ADD data/StationMap.csv ${PROJ_PATH}/data/StationMap.csv

ADD requirements.txt ${PROJ_PATH}/requirements.txt

RUN pip3 install -r ${PROJ_PATH}/requirements.txt

ADD start_service.sh ${PROJ_PATH}/start_service.sh

ADD athena/ ${PROJ_PATH}/athena/

WORKDIR ${PROJ_PATH}

ENTRYPOINT ["/opt/athena/start_service.sh"]