FROM aler9/rtsp-simple-server AS rtsp
FROM alpine:3.12
RUN apk add --no-cache ffmpeg nodejs-current npm dos2unix
COPY --from=rtsp /rtsp-simple-server /
RUN npm install -g http-server
RUN mkdir /var/www && mkdir /var/www/html
RUN chmod 777 /var/www && chmod 777 /var/www/html
COPY commands.sh .
COPY rtsp-simple-server.yml .
RUN dos2unix ./commands.sh rtsp-simple-server.yml
EXPOSE 8080
ENTRYPOINT [""]
CMD [ "ash", "./commands.sh" ]
