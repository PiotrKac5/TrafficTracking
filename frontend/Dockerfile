FROM nginx

# Copy the existing build folder to the Nginx server directory
COPY ./build /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
