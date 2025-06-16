dapr run --app-id agntsmth-lab-qry-api \
    --placement-host-address localhost:50000 \
    --resources-path ../../.dapr/components.localhost/ \
    --config ../../.dapr/configuration/config.yaml \
    --app-port 6001 \
    -- python3 -m uvicorn app:app --host 0.0.0.0 --port 6001
