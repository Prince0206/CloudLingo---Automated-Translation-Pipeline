import os, json, time, boto3, urllib.parse

s3 = boto3.client("s3")
translate = boto3.client("translate")
RESPONSE_BUCKET = os.environ["RESPONSE_BUCKET"]

def chunk_text(s, limit=4000):
    return [s[i:i+limit] for i in range(0, len(s), limit)]

def translate_texts(texts, src, tgt):
    out = []
    for t in texts:
        if len(t) <= 4000:
            r = translate.translate_text(Text=t, SourceLanguageCode=src, TargetLanguageCode=tgt)
            out.append(r["TranslatedText"])
        else:
            parts = []
            for piece in chunk_text(t):
                r = translate.translate_text(Text=piece, SourceLanguageCode=src, TargetLanguageCode=tgt)
                parts.append(r["TranslatedText"])
            out.append("".join(parts))
    return out

def handler(event, context):
    for rec in event.get("Records", []):
        bucket = rec["s3"]["bucket"]["name"]
        key = urllib.parse.unquote_plus(rec["s3"]["object"]["key"])
        if not key.endswith(".json"):
            continue

        obj = s3.get_object(Bucket=bucket, Key=key)
        data = json.loads(obj["Body"].read().decode("utf-8"))

        src = data["sourceLanguageCode"]
        tgt = data["targetLanguageCode"]
        texts = data["texts"]
        metadata = data.get("metadata", {})

        translations = translate_texts(texts, src, tgt)

        result = {
            "sourceLanguageCode": src,
            "targetLanguageCode": tgt,
            "texts": texts,
            "translations": translations,
            "metadata": metadata,
            "timestamp": int(time.time()),
            "sourceKey": key
        }

        out_key = f"translated/{os.path.basename(key).replace('.json', f'_to_{tgt}.json')}"
        s3.put_object(
            Bucket=RESPONSE_BUCKET,
            Key=out_key,
            Body=json.dumps(result, ensure_ascii=False).encode("utf-8"),
            ContentType="application/json"
        )
    return {"ok": True}