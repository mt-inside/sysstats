Interactive proto debugging:
npm install -g grpcc
grpcc --proto ../protos/sysstats.proto --address 127.0.0.1:50051 -i
^^ doesn't seem to work, might need to put the protos in a package?
