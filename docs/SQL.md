# SQL

## Snippets for fast consultation

### Get user emotions
```
WITH user_metadata_profile_guid AS (
  SELECT user_guid, uuid(value) as value FROM public_gateway.user_metadata WHERE key='profile_guid'
  GROUP BY user_guid, value
)
SELECT emotion_processor.emotion_trace.guid as "emotion_trace_guid",
emotion_processor.emotion.name as "emotion_name", 
emotion_processor.emotion.percent as "emotion_percent", 
emotion_processor.emotion_trace.received_at 
FROM public_gateway.user
JOIN user_metadata_profile_guid ON user_metadata_profile_guid.user_guid = public_gateway.user.guid
LEFT JOIN emotion_processor.emotion_trace ON emotion_processor.emotion_trace.profile_guid = user_metadata_profile_guid.value
LEFT JOIN emotion_processor.emotion ON emotion_processor.emotion.trace_guid = emotion_processor.emotion_trace.guid
WHERE public_gateway.user.email = 'example@example.com';
```

### Get user credit loan requests
```
WITH user_metadata_profile_guid AS (
  SELECT user_guid, uuid(value) as value FROM public_gateway.user_metadata WHERE key='profile_guid'
  GROUP BY user_guid, value
)
SELECT credit_manager.credit_request.* FROM public_gateway.user
JOIN user_metadata_profile_guid ON user_metadata_profile_guid.user_guid = public_gateway.user.guid
LEFT JOIN credit_manager.credit_request ON credit_manager.credit_request.profile_guid = user_metadata_profile_guid.value
WHERE public_gateway.user.email = 'example@example.com';
```

### Get user financial transactions
```
WITH user_metadata_profile_guid AS (
  SELECT user_guid, uuid(value) as value FROM public_gateway.user_metadata WHERE key='profile_guid'
  GROUP BY user_guid, value
)
SELECT credit_manager.financial_transaction.* FROM public_gateway.user
JOIN user_metadata_profile_guid ON user_metadata_profile_guid.user_guid = public_gateway.user.guid
LEFT JOIN credit_manager.financial_transaction ON credit_manager.financial_transaction.profile_guid = user_metadata_profile_guid.value
WHERE public_gateway.user.email = 'example@example.com';
```