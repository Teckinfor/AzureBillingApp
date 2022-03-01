# syntax=docker/dockerfile:1
FROM python:alpine3.15
WORKDIR /home
RUN pip install requests elastic-enterprise-search xmltodict
RUN mkdir billingapp
WORKDIR /home/billingapp
COPY scriptAPI scriptAPI
WORKDIR /home/billingapp/scriptAPI
CMD ["nohup","python","/home/billingapp/scriptAPI/run.py", "use_env", "&"]
