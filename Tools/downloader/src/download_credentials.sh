#!/bin/bash -x -eu -o pipefail

if [[ ! -f secrets.conf ]]; then
	echo "ERROR: secrets.conf not found in `pwd`"
	exit 1
fi

mkdir ~/.aws
mv secrets.conf ~/.aws/credentials

cat >~/.aws/config <<EOF
[default]
region=us-east-1
output=json
EOF

FILENAME=`basename $1`

echo $FILENAME

aws s3 cp "$1" - --request-payer requester | tee "$FILENAME" | md5sum -b > "$FILENAME".md5sum

EXITCODE=${PIPESTATUS[0]}

# Get rid of the credentials
rm -rf ~/.aws

# We care about the download exit code
exit $EXITCODE
