#!/usr/bin/env python3
"""
CloudLingo Local Translator
---------------------------
Run translations locally using Amazon Translate, without Lambda.
Uploads the translated output to your S3 response bucket.
"""

import json
import sys
import time
from pathlib import Path
import boto3

def chunk_text(s, limit=4000):
    """Split long text into chunks under AWS Translate's 5000 byte limit."""
    return [s[i:i+limit] for i in range(0, len(s), limit)]

def translate_texts(texts, src, tgt, client):
    """Translate each text, chunking if necessary."""
    results = []
    for t in texts:
        if len(t) <= 4000:
            resp = client.translate_text(Text=t, SourceLanguageCode=src, TargetLanguageCode=tgt)
            results.append(resp["TranslatedText"])
        else:
            parts = []
            for piece in chunk_text(t):
                resp = client.translate_text(Text=piece, SourceLanguageCode=src, TargetLanguageCode=tgt)
                parts.append(resp["TranslatedText"])
            results.append("".join(parts))
    return results

def main():
    if len(sys.argv) != 4:
        print("Usage: python translate_local.py <local_json_path> <request_bucket> <response_bucket>")
        sys.exit(1)

    local_json = Path(sys.argv[1])
    request_bucket = sys.argv[2]
    response_bucket = sys.argv[3]

    s3 = boto3.client("s3", region_name="us-east-1")
    translate = boto3.client("translate", region_name="us-east-1")

    # Load request JSON
    data = json.loads(local_json.read_text(encoding="utf-8"))
    src = data["sourceLanguageCode"]
    tgt = data["targetLanguageCode"]
    texts = data["texts"]
    metadata = data.get("metadata", {})

    # Translate
    translated = translate_texts(texts, src, tgt, translate)

    # Build output JSON
    out = {
        "sourceLanguageCode": src,
        "targetLanguageCode": tgt,
        "texts": texts,
        "translations": translated,
        "metadata": metadata,
        "timestamp": int(time.time())
    }

    # Upload to response bucket
    out_key = f"translated/{local_json.stem}_to_{tgt}.json"
    s3.put_object(
        Bucket=response_bucket,
        Key=out_key,
        Body=json.dumps(out, ensure_ascii=False).encode("utf-8"),
        ContentType="application/json"
    )

    print(f"✅ Uploaded: s3://{response_bucket}/{out_key}")

if __name__ == "__main__":
    main()