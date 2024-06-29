# Use a imagem do Nginx como base
FROM nginx:alpine

# Instalar git (caso não esteja disponível por padrão na imagem)
RUN apk update && apk add git

# Obter a versão do Git e definir como variável de ambiente
RUN export VERSION=$(git describe --tags --abbrev=0)

# Substituir a versão no HTML
RUN echo "window.APP_VERSION='${VERSION}';" > /usr/share/nginx/html/version.js

# Expor a porta 80
EXPOSE 80
