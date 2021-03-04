bind = "0.0.0.0:2020"
# Some deployments take a long time, because they might be...
#  - building containers
#  - running database migrations
#  - collecting and post-processing static assets
#  - etc.
# So wait a long time before giving up!
timeout = 240
