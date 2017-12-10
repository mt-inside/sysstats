function venv()
{
    declare venv=$1
    declare reqs=$2

    python3 -m venv $venv
    source $venv/bin/activate
    pip3 install -r $reqs
    deactivate
}

venv venv-build requirements.build.txt
venv venv-run requirements.txt
