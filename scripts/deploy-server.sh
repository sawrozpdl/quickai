export APP_NAME=quickai
heroku container:push web -a $APP_NAME
heroku container:release web -a $APP_NAME
