curl --location 'http://localhost:6002/embed' \
--header 'Content-Type: application/json' \
--data '{
    "file_system_path": "/Users/simon.stipcich/code/repo/agnt-smth-lab/.data/c4"
}'

curl --location 'http://localhost:6002/embed' \
--header 'Content-Type: application/json' \
--data '{
    "file_system_path": "/Users/simon.stipcich/code/repo/agnt-smth-lab/.data/wis"
}'

curl --location 'http://localhost:6002/embed' \
--header 'Content-Type: application/json' \
--data '{
    "file_system_path": "/Users/simon.stipcich/code/azdo/Platform-RaffleMania/"
}'
