# Stage 1

# Campus Notification System Design

## Objective

Design a scalable notification platform that enables students to receive real-time updates related to:

- Placements
- Events
- Results

The system should provide secure and structured REST APIs that allow frontend applications to efficiently fetch, manage, and display notifications for logged-in users.

---

# Core Actions Supported

The notification platform supports the following core actions:

1. Fetch notifications for a student
2. Fetch unread notifications
3. Mark notifications as read
4. Send notifications to students
5. Delete notifications
6. Deliver notifications in real time

---

# Base URL

```txt
/api/v1
```

---

# Authentication

All APIs require authentication headers.

## Request Headers

```http
Authorization: Bearer <token>
Content-Type: application/json
```

---

# 1. Fetch Notifications

## Endpoint

```http
GET /notifications
```

---

## Query Parameters

| Parameter | Type | Description |
|---|---|---|
| studentId | integer | Unique student ID |
| unreadOnly | boolean | Fetch only unread notifications |
| page | integer | Pagination page number |
| limit | integer | Number of notifications per page |

---

## Example Request

```http
GET /notifications?studentId=1042&unreadOnly=true&page=1&limit=10
```

---

## Example Response

```json
{
  "notifications": [
    {
      "id": "d100a14576bc",
      "type": "Placement",
      "message": "CSX Corporation hiring for SDE roles",
      "isRead": false,
      "createdAt": "2026-04-22T17:51:18"
    },
    {
      "id": "b2853d64b0",
      "type": "Result",
      "message": "Mid-semester results published",
      "isRead": false,
      "createdAt": "2026-04-22T17:55:30"
    }
  ],
  "page": 1,
  "limit": 10,
  "total": 2
}
```

---

# 2. Fetch Unread Notifications

## Endpoint

```http
GET /notifications/unread
```

---

## Example Request

```http
GET /notifications/unread?studentId=1042
```

---

## Example Response

```json
{
  "notifications": [
    {
      "id": "b283218f-ea5a-4b7c-93a9-1f2f240d64b0",
      "type": "Placement",
      "message": "Amazon hiring for internship roles",
      "isRead": false,
      "createdAt": "2026-04-22T17:55:30"
    }
  ]
}
```

---

# 3. Mark Notification as Read

## Endpoint

```http
PATCH /notifications/{notificationId}/read
```

---

## Example Request

```http
PATCH /notifications/d146095a-0d86-4a34-9e69-3900a14576bc/read
```

---

## Example Response

```json
{
  "message": "Notification marked as read successfully"
}
```

---

# 4. Send Notification

## Endpoint

```http
POST /notifications/send
```

---

## Example Request Body

```json
{
  "studentIds": [1042, 1043, 1044],
  "type": "Placement",
  "message": "Google is hiring for Software Engineer roles"
}
```

---

## Example Response

```json
{
  "message": "Notifications queued successfully"
}
```

---

# 5. Delete Notification

## Endpoint

```http
DELETE /notifications/{notificationId}
```

---

## Example Request

```http
DELETE /notifications/d146095a-0d86-4a34-9e69-3900a14576bc
```

---

## Example Response

```json
{
  "message": "Notification deleted successfully"
}
```

---

# Notification JSON Schema

```json
{
  "id": "UUID",
  "studentId": "integer",
  "type": "Placement | Result | Event",
  "message": "string",
  "isRead": "boolean",
  "createdAt": "timestamp"
}
```

---

# Error Response Schema

```json
{
  "error": "Invalid request",
  "statusCode": 400
}
```

---

# Real-Time Notification Mechanism

## Recommended Technology

WebSockets

---

# Real-Time Notification Flow

```txt
Client connects to WebSocket server
↓
Server maintains persistent connection
↓
New notification generated
↓
Server pushes notification instantly
↓
Student receives notification in real time
```

---

# Why WebSockets?

Advantages:

- Real-time communication
- Reduced API polling
- Lower latency
- Faster notification delivery
- Better user experience
- Efficient server-client communication

---

# Stage 2

## Persistent Storage Choice

I would use PostgreSQL for storing notifications because the data is structured and relational. It supports indexing, filtering, sorting, pagination and handles large-scale data efficiently.

It is reliable and suitable for production systems where notification data consistency is important.

---

# Database Schema

## Students Table

```sql
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE
);
```

---

## Notifications Table

```sql
CREATE TYPE notification_type AS ENUM (
    'Placement',
    'Result',
    'Event'
);

CREATE TABLE notifications (
    id UUID PRIMARY KEY,
    studentId INTEGER REFERENCES students(id),
    notificationType notification_type,
    message TEXT,
    isRead BOOLEAN DEFAULT FALSE,
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

# Problems As Data Grows

As notifications increase:
- queries may become slow
- sorting takes more time
- DB load increases
- fetching unread notifications becomes expensive
- can slow down APIs.

---

# Solutions

## Indexing

```sql
CREATE INDEX idx_notifications
ON notifications(studentId, isRead, createdAt DESC);
```

This improves unread notification queries.

---

## Pagination

Instead of loading all notifications we can use this to limit the response size

---

## Redis Caching

Unread notifications can be cached to reduce repeated DB reads.

---

## Archiving Old Notifications

Older notifications can be moved to archive tables to keep active tables smaller.

---

# Queries Based On APIs

## Fetch Notifications

```sql
SELECT *
FROM notifications
WHERE studentId = 1042
ORDER BY createdAt DESC
LIMIT 10 OFFSET 0;
```

---

## Fetch Unread Notifications

```sql
SELECT *
FROM notifications
WHERE studentId = 1042
AND isRead = FALSE
ORDER BY createdAt DESC;
```

---

## Mark Notification As Read

```sql
UPDATE notifications
SET isRead = TRUE
WHERE id = 'notification-id';
```

---

## Send Notification

```sql
INSERT INTO notifications (
    id,
    studentId,
    notificationType,
    message
)
VALUES (
    gen_random_uuid(),
    1042,
    'Placement',
    'Google hiring for SDE roles'
);
```


## Delete Notification

```sql

DELETE FROM notifications

WHERE id = 'notification-id';

```

---

# Stage 3

The query is accurate because it correctly fetches unread notifications for a particular student and sorts them by latest notifications.

```sql
SELECT * FROM notifications
WHERE studentID = 1042 AND isRead = false
ORDER BY createdAt DESC;
```

However, the query becomes slow when the database grows to millions of notifications because the database may perform large table scans and sorting operations.

The main issue is the absence of a proper index for the filtering and sorting columns.

I would improve the query performance by adding a composite index:

```sql
CREATE INDEX idx_notifications_student_read_created
ON notifications(studentID, isRead, createdAt DESC);
```

This helps the database quickly filter unread notifications for a student and return them in sorted order.

Without indexing, the computation cost can approach:

```txt
O(n log n)
```

because of filtering and sorting large datasets.

With indexing, the query becomes significantly faster and closer to:

```txt
O(log n)
```

---

Adding indexes on every column is not a good idea.

Too many indexes:
- increase storage usage
- slow down INSERT and UPDATE operations
- increase maintenance overhead

Indexes should only be added on columns that are frequently:
- filtered
- sorted
- used in joins

---

# Query To Find Students Who Received Placement Notifications In Last 7 Days

```sql
SELECT DISTINCT studentID
FROM notifications
WHERE notificationType = 'Placement'
AND createdAt >= NOW() - INTERVAL '7 days';


# Stage 4

Fetching notifications on every page load increases database traffic and causes unnecessary repeated queries. As the number of users grows, this can overload the database and increase API response time.

To improve performance, I would use the following approaches.

---

# 1. Redis Caching

Unread notifications can be temporarily stored in Redis so that repeated requests do not always hit the database.

Advantages:
- very fast reads
- reduces DB load
- improves response time

Tradeoff:
- cache invalidation becomes slightly complex

---

# 2. WebSockets

Instead of repeatedly fetching notifications, the server can push notifications in real time using WebSockets.

Advantages:
- real-time updates
- fewer API requests
- better user experience

Tradeoff:
- maintaining persistent connections requires additional server resources

---

# 3. Pagination

Instead of loading all notifications at once:

```http
GET /notifications?page=1&limit=10
```

Advantages:
- smaller payload size
- faster queries
- lower memory usage

Tradeoff:
- frontend must handle pagination logic

---

# 4. Background Processing

Notification generation and delivery can be moved to background workers using queues like RabbitMQ or Kafka.

Advantages:
- improves scalability
- reduces API processing time
- handles bulk notifications efficiently

Tradeoff:
- additional infrastructure complexity

---

# Recommended Approach

A combination of:
- Redis caching
- WebSockets
- pagination
- background workers

would provide the best scalability and performance for the notification platform.
```


