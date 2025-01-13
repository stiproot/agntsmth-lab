curl --location 'http://localhost:6001/qry' \
--header 'Content-Type: application/json' \
--data '{
    "qry": "what is a c4 component diagram?",
    "file_system_path": "/Users/simon.stipcich/code/repo/agnt-smth-lab/.data/c4"
}'

curl --location 'http://localhost:6001/qry' \
--header 'Content-Type: application/json' \
--data '{
    "qry": "what is an example of a valid work item structure in yaml format",
    "file_system_path": "/Users/simon.stipcich/code/repo/agnt-smth-lab/.data/wis"
}'

curl --location 'http://localhost:6001/build' \
--header 'Content-Type: application/json' \
--data '{
    "file_system_path": "/Users/simon.stipcich/code/azdo/Platform-RaffleMania/"
}'

curl --location 'http://localhost:6001/qry' \
--header 'Content-Type: application/json' \
--data '{
    "qry": "What is RaffleMania?",
    "file_system_path": "/Users/simon.stipcich/code/azdo/Platform-RaffleMania/"
}'
