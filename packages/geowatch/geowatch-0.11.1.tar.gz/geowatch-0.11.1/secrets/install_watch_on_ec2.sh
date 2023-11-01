#!/bin/bash
# On the EC2 Instance
__doc__="
References:
    https://docs.google.com/document/d/1bW8UM1jR3opJ2qf-OU28Yr3Gyg7chZQ2MH5YQYGBIhs/edit#
"

__install_ssm__(){
    # Needed to login go an ec2 instance
    mkdir -p "$HOME/tmp/install_ssm"
    cd "$HOME/tmp/install_ssm"
    ARCH="$(dpkg --print-architecture)"
    declare -A SSM_DEB_URLS=(
        ["amd64"]="https://s3.amazonaws.com/session-manager-downloads/plugin/latest/ubuntu_64bit/session-manager-plugin.deb"
        ["i386"]="https://s3.amazonaws.com/session-manager-downloads/plugin/latest/ubuntu_32bit/session-manager-plugin.deb"
        ["arm64"]="https://s3.amazonaws.com/session-manager-downloads/plugin/latest/ubuntu_arm64/session-manager-plugin.deb"
    )
    SSM_DEB_URL="${SSM_DEB_URLS[${ARCH}]}"
    curl "$SSM_DEB_URL" -o "session-manager-plugin.deb"
    sudo dpkg -i session-manager-plugin.deb

    # Verify
    session-manager-plugin
}

__setup_ec2_instance__(){
    INSTANCE_ID=i-07d90398508df1a95
    AWS_PROFILE=iarpa
    AWS_REGION=us-west-2

    aws ssm start-session --target "$INSTANCE_ID" --profile "$AWS_PROFILE" --region "$AWS_REGION"

    # once connected switch users
    sudo su ubuntu


    # create a PEM keypair called iarpa-sandbox1
    ssh-keygen -t rsa -N "" -m PEM -f ~/.ssh/iarpa-sandbox1.pem

    cat ~/.ssh/iarpa-sandbox1.pem.pub

    # add public key to EC2 instance
    echo "<contents of public key>" >> /home/ubuntu/.ssh/authorized_keys

    # to be added to ~/.ssh/config on local machine
    echo "
    host sandbox1
        ProxyCommand sh -c 'aws ssm start-session --target $INSTANCE_ID --document-name SandboxKW_SSHDocument --profile iarpa --region us-west-2'
        User ubuntu
        IdentityFile ~/.ssh/iarpa-sandbox1.pem
    "

}

__stop_ec2_instance__(){
    INSTANCE_ID=i-07d90398508df1a95
    AWS_PROFILE=iarpa
    AWS_REGION=us-west-2
    # check the status of the EC2 instance with ID “i-0d46a9b93c43b0cd1”
    aws ec2 describe-instance-status --instance-id "$INSTANCE_ID" --profile "$AWS_PROFILE" --region "$AWS_REGION"

    # stop the EC2 instance with ID “i-0d46a9b93c43b0cd1”
    aws ec2 stop-instances --instance-ids "$INSTANCE_ID" --profile "$AWS_PROFILE" --region "$AWS_REGION"
    
}


##########
#  SECRETS
export WATCH_REPO_GITLAB_RO_DEPLOY_USERNAME=watch-repo-gitlab-ro-deploy-token
export WATCH_REPO_GITLAB_RO_DEPLOY_PASSWORD=_BVLSHsgaH57jriLHELf
export DVC_GITLAB_USERNAME=argo-access
export DVC_GITLAB_PASSWORD=glpat-Q_q5F832E_eG5h4msvxy
export TE_SMART_GITLAB_USERNAME=jon.crall
export TE_SMART_GITLAB_RO_TOKEN=JqEzkpUGTx9CxT1TjziQ
export WATCH_DVC_GITLAB_RW_USERNAME=WATCH_DVC_GITLAB_RW_TOKEN
export WATCH_DVC_GITLAB_RW_PASSWORD=glpat-JQhFjMXiXwBgJg5tQhcy

mkdir -p "$HOME/.aws"

echo "
[default]
region=us-west-2
output=json
" >  "$HOME/.aws/config"


# Note: this part probably has changed and needs to be
# repalced by the most recent data in $HOME/.aws/credentials
echo "
[iarpa]
aws_access_key_id = AKIAQK3GROKELT74PFKS
aws_secret_access_key = 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
" >  "$HOME/.aws/credentials"


chmod 664 "$HOME/.aws/config"
chmod 664 "$HOME/.aws/credentials"
##########


ln -s /data data

# Get my bash environment
git clone https://github.com/Erotemic/local.git
export HAVE_SUDO=False
export IS_HEADLESS=True
export WITH_SSH_KEYS=False
source ~/local/init.sh
source .bashrc

echo "SETUP CONDA ENV"
source "$HOME/local/init/freshstart_ubuntu.sh"
setup_conda_env
conda activate conda38



# Setup the watch algo repo
git clone "https://${WATCH_REPO_GITLAB_RO_DEPLOY_USERNAME}:${WATCH_REPO_GITLAB_RO_DEPLOY_PASSWORD}@gitlab.kitware.com/smart/watch.git" "$HOME/code/watch"

cd "$HOME/code/watch"
./run_developer_setup.sh


# Setup the watch DVC repo
SMART_DVC_DPATH=$HOME/data/dvc-repos/smart_watch_dvc
git clone "https://${DVC_GITLAB_USERNAME}:${DVC_GITLAB_PASSWORD}@gitlab.kitware.com/smart/smart_watch_dvc.git" "$SMART_DVC_DPATH"

git remote add readwrite "https://${WATCH_DVC_GITLAB_RW_USERNAME}:${WATCH_DVC_GITLAB_RW_PASSWORD}@gitlab.kitware.com/smart/smart_watch_dvc.git"

git submodule init

cd "$SMART_DVC_DPATH"
#git submodule set-url annotations git@smartgitlab.com:TE/annotations.git
# TODO: more secure method for this
git submodule set-url annotations https://${TE_SMART_GITLAB_USERNAME}:${TE_SMART_GITLAB_RO_TOKEN}@smartgitlab.com/TE/annotations.git
git submodule update

export AWS_DEFAULT_PROFILE=iarpa
export AWS_REQUEST_PAYER='requester'

#git@smartgitlab.com:TE/annotations.git




#### Debugging


AWS_DEFAULT_PROFILE=iarpa AWS_REQUEST_PAYER='requester' gdalwarp \
    --debug off \
    -t_srs epsg:32611 -overwrite -of COG -co OVERVIEWS=AUTO -co BLOCKSIZE=256 -co COMPRESS=DEFLATE \
    -te -119.867436 39.395105 -119.716295 39.570735 -te_srs epsg:4326 \
    -multi --config GDAL_CACHEMAX 500 -wm 500 -co NUM_THREADS=2 \
    /vsis3/sentinel-s2-l1c/tiles/10/S/GJ/2016/12/31/0/TCI.jp2 \
    "$HOME"/data/dvc-repos/smart_watch_dvc/Aligned-Drop3-L1-MINI/US_R004/S2/affine_warp/crop_20161231T190105Z_N39.395105W119.867436_N39.570735W119.716295_S2_0/.tmp.crop_20161231T190105Z_N39.395105W119.867436_N39.570735W119.716295_S2_0_kzzxivda_3.tif


AWS_DEFAULT_PROFILE=iarpa AWS_REQUEST_PAYER='requester' gdalwarp \
    -t_srs epsg:32611 -overwrite -of COG -co OVERVIEWS=AUTO -co BLOCKSIZE=256 -co COMPRESS=DEFLATE \
    -te -119.867436 39.395105 -119.716295 39.570735 -te_srs epsg:4326 \
    -multi --config GDAL_CACHEMAX 1000 -wm 1000 -co NUM_THREADS=2 \
    /vsis3/sentinel-s2-l1c/tiles/10/S/GJ/2016/12/31/0/TCI.jp2 \
    "$HOME"/data/dvc-repos/smart_watch_dvc/Aligned-Drop3-L1-MINI/US_R004/S2/affine_warp/crop_20161231T190105Z_N39.395105W119.867436_N39.570735W119.716295_S2_0/.tmp.crop_20161231T190105Z_N39.395105W119.867436_N39.570735W119.716295_S2_0_kzzxivda_3.tif
