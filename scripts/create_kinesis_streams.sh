awslocal kinesis create-stream --stream-name ingestion-stream --shard-count  1
awslocal kinesis create-stream --stream-name alert-stream --shard-count  1

echo awslocal kinesis list-streams