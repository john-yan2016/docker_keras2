FROM gw000/keras:1.2.0-py2-th-cpu

# install dependencies from debian packages
RUN apt-get update -qq \
 && apt-get install --no-install-recommends -y \
    python-matplotlib \
    python-pillow

# install dependencies from python packages
RUN pip --no-cache-dir install \
    pandas \
    scikit-learn \
    statsmodels

# install your app
ADD /home/dockertest/test02/ai/ /srv/ai/
RUN chmod +x /srv/ai/test.py

CMD ["/srv/ai/test.py"]