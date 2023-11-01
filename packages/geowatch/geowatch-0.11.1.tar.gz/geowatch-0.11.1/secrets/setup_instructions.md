Setup instructions for the repo secrets with Transcrypt (https://github.com/elasticdog/transcrypt)


```bash

# Using my fork because it has better security options for ssl
git clone https://github.com/Erotemic/transcrypt.git $HOME/code/transcrypt

# Optional: symlink to your local bin
ln -s $HOME/code/transcrypt/transcrypt $HOME/.local/bin/transcrypt

# Write the .gitattributes file to the repo root


# This command will both initialize and decrypt the secrets in the repo
WATCH_TRANSCRYPT_SECRET=SpoilingFreefallGathererFencingContentsAgile
transcrypt -c aes-256-cbc -p "$WATCH_TRANSCRYPT_SECRET" -y


# To flush credentials use: 
transcrypt -f -y
```
