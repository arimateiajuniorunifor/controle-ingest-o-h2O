# Use a imagem do Nginx como base
FROM nginx:alpine

# Instalar git (caso não esteja disponível por padrão na imagem)
RUN apk update && apk add git

# Shell inline para obter a versão do Git
RUN export VERSION=$(git describe --tags --abbrev=0) \
    && echo "window.APP_VERSION='${VERSION}';" > /usr/share/nginx/html/version.js

# Expor a porta 80
EXPOSE 80
