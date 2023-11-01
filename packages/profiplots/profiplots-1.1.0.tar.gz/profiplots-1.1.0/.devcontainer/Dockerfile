FROM python:3.10.10

ARG USER_ID
ARG USER_NAME
ARG USER_GID
ARG USER_GNAME

ARG QUARTO_VERSION=1.3.450

# Install R
RUN apt-get update && apt-get install -y \
    r-base && \
    rm -rf /var/lib/apt/lists/*
RUN echo 'options(repos = c(REPO_NAME = "https://packagemanager.rstudio.com/all/latest"))' >> /etc/R/Rprofile.site

# Download and install Quarto
RUN mkdir -p /opt/quarto/${QUARTO_VERSION}
RUN curl -o quarto.tar.gz -L \
    "https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VERSION}/quarto-${QUARTO_VERSION}-linux-amd64.tar.gz"
RUN tar -zxvf quarto.tar.gz \
    -C "/opt/quarto/${QUARTO_VERSION}" \
    --strip-components=1
RUN rm quarto.tar.gz
RUN ln -s /opt/quarto/${QUARTO_VERSION}/bin/quarto /usr/local/bin/quarto

# INSTALL THE REST AS A USER
# Create user and group
RUN groupadd -g ${USER_GID} ${USER_GNAME}
RUN useradd ${USER_NAME} -u ${USER_ID} -g ${USER_GNAME} -m -s /bin/bash
USER ${USER_NAME}

# Install Quarto extension for PDF generation
RUN quarto install tinytex
