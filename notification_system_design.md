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