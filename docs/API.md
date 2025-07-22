# API Documentation

## Overview

The Huffman Coding API provides endpoints for text compression and decompression using the Huffman algorithm.

## Base URL

```
http://127.0.0.1:5000
```

## Endpoints

### GET /

**Description:** Serves the main web interface

**Response:** HTML page with the interactive Huffman coding interface

---

### POST /encode

**Description:** Encode text using Huffman coding

**Request Body:**
```json
{
  "text": "string"
}
```

**Response:**
```json
{
  "encoded": "binary_string",
  "frequency_table": [
    {"char": "character", "freq": number}
  ],
  "huffman_codes": [
    {"char": "character", "code": "binary_code"}
  ],
  "stats": {
    "original_size": number,
    "compressed_size": number,
    "compression_ratio": number,
    "space_saved": number
  }
}
```

**Error Response:**
```json
{
  "error": "error_message"
}
```

**Example:**
```bash
curl -X POST http://127.0.0.1:5000/encode \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello World!"}'
```

---

### POST /decode

**Description:** Decode Huffman encoded text

**Request Body:**
```json
{
  "encoded": "binary_string",
  "frequency_table": [
    {"char": "character", "freq": number}
  ]
}
```

**Response:**
```json
{
  "decoded": "original_text"
}
```

**Error Response:**
```json
{
  "error": "error_message"
}
```

**Example:**
```bash
curl -X POST http://127.0.0.1:5000/decode \
  -H "Content-Type: application/json" \
  -d '{
    "encoded": "110100101...",
    "frequency_table": [{"char": "H", "freq": 1}, ...]
  }'
```

## Error Codes

- `400 Bad Request`: Invalid input data
- `404 Not Found`: Endpoint not found
- `405 Method Not Allowed`: Wrong HTTP method
- `500 Internal Server Error`: Server error

## Rate Limiting

Currently no rate limiting is implemented. In production, consider implementing rate limiting to prevent abuse.
