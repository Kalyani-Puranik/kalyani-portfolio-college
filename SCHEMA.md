# MongoDB Schema Design — Kalyani Portfolio

## Collection: `blogs`
```json
{
  "_id": "ObjectId",
  "title": "Why Attention is All You Need",
  "slug": "why-attention-is-all-you-need",
  "excerpt": "Breaking down transformers in plain English...",
  "content": "# Full markdown content here...",
  "tag": "ML",
  "read_time": "8 min read",
  "published": true,
  "featured": false,
  "cover_image": "https://example.com/cover.jpg",
  "views": 142,
  "created_at": "2024-11-15T10:30:00Z",
  "updated_at": "2024-11-15T10:30:00Z"
}
```
**Indexes:** `slug` (unique), `published`, `created_at`

---

## Collection: `projects`
```json
{
  "_id": "ObjectId",
  "title": "SentimentSage",
  "slug": "sentiment-sage",
  "description": "Aspect-level sentiment analysis using fine-tuned BERT",
  "problem": "Brands couldn't understand nuanced customer feelings...",
  "solution": "Fine-tuned BERT with aspect-level granularity...",
  "impact": "94.2% accuracy, 1000+ reviews/second...",
  "tech_stack": ["Python", "BERT", "HuggingFace", "FastAPI", "Docker"],
  "github_url": "https://github.com/kalyani/sentimentsage",
  "demo_url": "https://sentimentsage.kalyani.dev",
  "paper_url": null,
  "cover_image": "https://example.com/project.jpg",
  "images": [],
  "featured": true,
  "year": "2024",
  "project_type": "ML · NLP",
  "order": 1,
  "created_at": "2024-10-01T00:00:00Z",
  "updated_at": "2024-10-01T00:00:00Z"
}
```
**Indexes:** `slug` (unique), `featured`, `order`

---

## Collection: `contacts`
```json
{
  "_id": "ObjectId",
  "name": "Priya Sharma",
  "email": "priya@example.com",
  "subject": "collaboration",
  "message": "Hi Kalyani! I loved your DermaScan project...",
  "read": false,
  "replied": false,
  "created_at": "2024-11-20T14:22:00Z"
}
```

---

## Collection: `analytics`
```json
{
  "_id": "ObjectId",
  "page": "/",
  "referrer": "https://linkedin.com",
  "user_agent": "Mozilla/5.0...",
  "ip_hash": "a1b2c3d4e5f6g7h8",
  "country": "IN",
  "timestamp": "2024-11-20T14:22:00Z"
}
```
**Indexes:** `page`, `timestamp`

---

## Collection: `photos`
```json
{
  "_id": "ObjectId",
  "title": "Morning Light",
  "description": "Sunrise at Hampi",
  "url": "https://cdn.example.com/photos/morning-light.jpg",
  "thumbnail_url": "https://cdn.example.com/photos/morning-light-thumb.jpg",
  "alt": "Golden morning light over ancient ruins",
  "category": "travel",
  "width": 3024,
  "height": 4032,
  "order": 1,
  "created_at": "2024-11-01T00:00:00Z"
}
```
