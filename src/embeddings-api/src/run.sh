dapr run --app-id agntsmth-lab-embeddings-api \
    --placement-host-address localhost:50000 \
    --resources-path ../.dapr.local/components/ \
    --config ../.dapr/configuration/config.yaml \
    --app-port 6002 \
    -- python3 -m uvicorn app:app --host 0.0.0.0 --port 6002
