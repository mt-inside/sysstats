dev env and deployment:
recall 12 factor: config should come from env, but not other serive's names
code should look up a service as it is morally called, e.g. "sysstats_backend"
everything else needs to accomodate that, e.g. compose, k8s are all to be made to make it available under that name
deplyment env should be docker compose (for petstack)
dev env is compose with individual containers replaced (possible?) or run with replacement code mounted into them
- use compose extension files for this

Interactive proto debugging:
npm install -g grpcc
grpcc --proto ../protos/sysstats.proto --address 127.0.0.1:50051 -i
^^ doesn't seem to work, might need to put the protos in a package?
