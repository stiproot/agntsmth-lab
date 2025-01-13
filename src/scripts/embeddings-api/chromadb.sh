
curl -u agnt:smth http://localhost:8000/api/v1/collections

curl -u agnt:smth -X POST http://localhost:8000/api/v1/collections \
    -H "Content-Type: application/json" \
    -d '{
          "name": "example_collection"
        }'

curl -u agnt:smth http://localhost:8000/api/v1/collections/<collection-id>

curl -u agnt:smth -X DELETE http://localhost:8000/api/v1/collections/<collection-id>

curl -u agnt:smth -X POST http://localhost:8000/api/v1/collections/<collection-id>/items \
    -H "Content-Type: application/json" \
    -d '{
          "items": [
            {
              "id": "item1",
              "embedding": [0.1, 0.2, 0.3],
              "metadata": {"key": "value"}
            },
            {
              "id": "item2",
              "embedding": [0.4, 0.5, 0.6],
              "metadata": {"key": "another_value"}
            }
          ]
        }'

curl -u agnt:smth http://localhost:8000/api/v1/collections/<collection-id>/items

curl -u agnt:smth -X DELETE http://localhost:8000/api/v1/collections/<collection-id>/items/<item-id>

curl -u agnt:smth -X POST http://localhost:8000/api/v1/collections/<collection-id>/query \
    -H "Content-Type: application/json" \
    -d '{
          "embedding": [0.1, 0.2, 0.3],
          "top_k": 5
        }'

curl -u agnt:smth -X POST http://localhost:8000/api/v1/collections/<collection-id>/query \
    -H "Content-Type: application/json" \
    -d '{
          "filter": {"key": "value"},
          "top_k": 5
        }'

curl -u agnt:smth http://localhost:8000/health



