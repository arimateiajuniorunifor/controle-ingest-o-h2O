# Use a imagem do Nginx como base
FROM nginx:alpine

# Argumento para passar a versão
ARG VERSION

# Copiar arquivos do frontend para o diretório do Nginx
COPY . /usr/share/nginx/html

# Substituir a versão no HTML
RUN echo "<script>window.APP_VERSION='${VERSION}';</script>" > /usr/share/nginx/html/version.js

# Expor a porta 80
EXPOSE 80
