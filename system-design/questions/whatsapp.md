# WhatsApp System Design

## Problem Statement
Design a real-time messaging application similar to WhatsApp that supports one-on-one chats, group messaging, file sharing, and message status tracking for over 2 billion users globally.

**Mini Example**: Design a chat application like WhatsApp

---

## 1. Requirements Clarification

### Functional Requirements
*[What the system must do]*
- **Core Features**:
  - One-on-one chat messaging
  - Group chats (max 100 people)
  - File sharing (images, videos, documents)
  - Message status tracking (sent, delivered, read)
  - User presence indicators (online/offline, last seen)
- **User Actions**:
  - Send/receive messages in real-time
  - Create/join/leave group chats
  - Share media files
  - View message status and user presence
- **Edge Cases**:
  - Handle offline users with push notifications
  - Manage large group conversations
  - Handle media file uploads/downloads
  - Deal with network connectivity issues

**Mini Example**:
- Send text messages between two users
- Create group chat with multiple participants
- Share photos and videos with delivery confirmation
- Show "last seen" status for contacts

### Non-Functional Requirements
*[Quality constraints]*
- **Performance**:
  - < 100ms message delivery latency
  - Support 24K requests per second
  - Real-time message delivery
- **Scalability**:
  - Handle 50M daily active users
  - Support 2B messages per day
  - Scale to 38PB storage over 10 years
- **Availability**: 99.9% uptime
- **Reliability**: Message delivery guarantees, no data loss

**Mini Example**:
- 99.9% uptime requirement
- < 100ms response time for message delivery
- Handle 24K requests/second peak load

### Extended Requirements
*[Nice-to-have features]*
- **Analytics**:
  - Message delivery metrics
  - User engagement tracking
  - Media usage statistics
- **Security**:
  - End-to-end encryption
  - User authentication
  - Message privacy
- **Additional Features**:
  - Push notifications for offline users
  - Message search functionality
  - Voice/video calling (future)

**Mini Example**:
- Track message delivery and read receipts
- Send push notifications when users are offline
- Implement end-to-end encryption for messages

---

## 2. Estimation and Constraints

### Scale Estimation
*[Back-of-envelope calculations]*

**Traffic Assumptions**:
- **Daily Active Users (DAU)**: 50 million
- **Messages per user per day**: 40 (10 messages × 4 recipients)
- **Total messages per day**: 2 billion
- **Media messages**: 5% of total (100 million files/day)

**Mini Example**:
- 50M users × 40 messages = 2B messages/day
- 5% media = 100M files/day
- 24K requests/second peak

**Storage Requirements**:
- **Text messages**: 100 bytes per message
- **Daily text storage**: 2B × 100 bytes = 200 GB/day
- **Media files**: 100 KB average per file
- **Daily media storage**: 100M × 100 KB = 10 TB/day
- **10-year storage**: (10.2 TB/day) × 365 × 10 = 38 PB

**Mini Example**:
- 200 GB/day for text messages
- 10 TB/day for media files
- 38 PB total over 10 years

**Bandwidth Requirements**:
- **Daily ingress**: 10.2 TB
- **Bandwidth needed**: 10.2 TB ÷ (24 × 3600) ≈ 120 MB/second

**Mini Example**:
- 120 MB/s bandwidth requirement
- Handles 10.2 TB daily data ingress

### Summary Table
| Metric | Estimate | Notes |
|--------|----------|-------|
| DAU | 50M | Daily active users |
| Messages | 2B/day | Total messages sent |
| RPS | 24K/s | Peak requests per second |
| Storage | 10.2 TB/day | Daily storage requirement |
| Bandwidth | 120 MB/s | Required bandwidth |
| Media Files | 100M/day | 5% of total messages |

---

## 3. Data Model Design

### Database Schema
*[Define entities and relationships]*

**Core Tables**:
- **Users**:
  - Fields: id, phone_number, name, email, created_at, last_seen
  - Indexes: phone_number (unique), last_seen
- **Messages**:
  - Fields: id, sender_id, chat_id, group_id, content, type, created_at, delivered_at, seen_at
  - Indexes: sender_id, chat_id, group_id, created_at
- **Chats**:
  - Fields: id, created_at, updated_at
  - Indexes: created_at
- **Users_Chats**:
  - Fields: user_id, chat_id, created_at
  - Indexes: user_id, chat_id (composite)
- **Groups**:
  - Fields: id, name, created_by, created_at, max_members
  - Indexes: created_by, created_at
- **Users_Groups**:
  - Fields: user_id, group_id, role, joined_at
  - Indexes: user_id, group_id (composite)

**Mini Example**:
- **Users**: id, phone_number, name, last_seen
- **Messages**: id, sender_id, chat_id, content, type, delivered_at, seen_at
- **Chats**: id, created_at (for one-on-one conversations)
- **Groups**: id, name, created_by, max_members (for group chats)

### Database Choice
*[SQL vs NoSQL decision]*
- **Microservices approach**: Split data across different services
- **User Service**: PostgreSQL for user data and authentication
- **Chat Service**: Apache Cassandra for message storage and scalability
- **Media Service**: Object storage (S3) for file storage
- **Reasoning**: Different data types require different storage solutions

**Mini Example**:
- **PostgreSQL**: User data (relational, ACID compliance)
- **Cassandra**: Messages (high write throughput, horizontal scaling)
- **S3**: Media files (cost-effective, scalable object storage)

---

## 4. API Design

### Core APIs
*[Define system interfaces]*

```typescript
// Get all chats and groups for a user
getAll(userID: UUID): Chat[] | Group[]
// Example: getAll("user123"): [chat1, chat2, group1]

// Get messages for a chat/group
getMessages(userID: UUID, channelID: UUID, limit: number, offset: number): Message[]
// Example: getMessages("user123", "chat456", 50, 0): [message1, message2, ...]

// Send a message
sendMessage(userID: UUID, channelID: UUID, message: Message): boolean
// Example: sendMessage("user123", "chat456", {type: "text", content: "Hello"})

// Join/leave a group
joinGroup(userID: UUID, groupID: UUID): boolean
leaveGroup(userID: UUID, groupID: UUID): boolean
// Example: joinGroup("user123", "group789")

// Update message status
updateMessageStatus(messageID: UUID, status: "delivered" | "read"): boolean
// Example: updateMessageStatus("msg123", "read")

// Get user presence
getUserPresence(userID: UUID): {online: boolean, lastSeen: Date}
// Example: getUserPresence("user123"): {online: true, lastSeen: "2024-01-01T10:00:00Z"}
```

### API Considerations
- **Authentication**: JWT tokens for user sessions
- **Rate Limiting**: 100 messages/minute per user
- **Error Handling**: Standard HTTP status codes with detailed error messages
- **WebSocket**: Real-time message delivery and presence updates

**Mini Example**:
- JWT authentication for all API calls
- 100 messages/minute rate limit per user
- WebSocket connection for real-time updates

---

## 5. High-Level Architecture

### System Components
*[Core building blocks]*

1. **Client Layer**: Mobile apps (iOS/Android), Web client
2. **API Gateway**: Request routing, authentication, rate limiting
3. **Load Balancer**: Traffic distribution across services
4. **User Service**: User management, authentication, profiles
5. **Chat Service**: Message handling, WebSocket connections
6. **Group Service**: Group management, member operations
7. **Media Service**: File upload/download, storage management
8. **Notification Service**: Push notifications for offline users
9. **Presence Service**: Online/offline status, last seen tracking
10. **Database Layer**: PostgreSQL, Cassandra, Redis
11. **Object Storage**: S3 for media files
12. **CDN**: Content delivery for media files

**Mini Example**:
- **API Gateway**: Route requests to appropriate services
- **Chat Service**: Handle real-time messaging via WebSockets
- **Media Service**: Process and store images/videos
- **Notification Service**: Send push notifications via FCM/APNS

### Data Flow
*[How data moves through the system]*

**Message Send Flow**:
1. Client → API Gateway → Chat Service
2. Chat Service → Database (store message)
3. Chat Service → Cache (update recent messages)
4. Chat Service → WebSocket (deliver to online recipients)
5. Chat Service → Notification Service (for offline users)
6. Response to Client

**Message Receive Flow**:
1. WebSocket connection receives message
2. Client updates UI immediately
3. Client sends ACK to server
4. Server updates message status to "delivered"
5. When user opens chat, status updates to "read"

**Mini Example**:
- **Message Send**: User → API → Chat Service → Database → WebSocket → Recipient
- **Message Receive**: WebSocket → Client → ACK → Status Update

---

## 6. Detailed Design

### Caching Strategy
*[Performance optimization]*

**Cache Levels**:
- **Application Cache**: In-memory caching for active connections
- **Distributed Cache**: Redis for message caching and presence data
- **CDN**: Static media content delivery

**Cache Policies**:
- **Eviction**: LRU for message cache, TTL for presence data
- **Consistency**: Cache-aside for messages, write-through for presence

**Mini Example**:
- **Redis**: Cache recent messages (last 100 per chat)
- **LRU eviction**: Remove least recently accessed messages
- **TTL**: 24 hours for presence data, 1 hour for message cache

### Data Partitioning
*[Scalability strategy]*

**Partitioning Strategies**:
- **Hash-based**: Partition messages by chat_id for even distribution
- **Range-based**: Partition by timestamp for historical data
- **List-based**: Partition by user_id for user-specific data

**Mini Example**:
- **Message partitioning**: Hash by chat_id for even distribution
- **User data**: Partition by user_id for user-specific queries
- **Consistent hashing**: Add/remove nodes without full rebalancing

### Security Considerations
*[Protection mechanisms]*

**Authentication & Authorization**:
- **JWT Tokens**: Stateless authentication for API access
- **WebSocket Authentication**: Token validation for real-time connections
- **Group Permissions**: Role-based access for group operations

**Data Protection**:
- **End-to-End Encryption**: Message encryption at rest and in transit
- **Input Validation**: Sanitize all user inputs
- **Rate Limiting**: Prevent abuse and spam

**Mini Example**:
- **JWT tokens**: Required for all API operations
- **End-to-end encryption**: Messages encrypted client-to-client
- **Rate limiting**: 100 messages/minute per user

---

## 7. Bottleneck Analysis & Resolution

### Single Points of Failure
*[Identify and resolve]*

**Potential Issues**:
- **Chat Service**: Single service handling all messaging
- **Database**: Single database instance
- **WebSocket Connections**: Single connection manager
- **API Gateway**: Single entry point
- **Media Storage**: Single object storage instance

**Solutions**:
- **Multiple Chat Service instances**: Load balanced across regions
- **Database clustering**: Primary + read replicas with failover
- **WebSocket clustering**: Redis pub/sub for connection management
- **Multiple API Gateways**: Active-passive configuration
- **Multi-region object storage**: S3 with cross-region replication

**Mini Example**:
- **Chat Service**: 3 instances with load balancer
- **Database**: Primary + 2 read replicas
- **WebSocket**: Redis cluster for connection management
- **API Gateway**: Active-passive with health checks

### Scalability Improvements
*[Handle growth]*

**Horizontal Scaling**:
- **Chat Service**: Auto-scaling based on WebSocket connections
- **Database**: Sharding by chat_id for message storage
- **Media Service**: Multiple instances with CDN distribution

**Vertical Scaling**:
- **Database optimization**: Query optimization, proper indexing
- **Connection pooling**: Efficient database connections
- **Message compression**: Reduce bandwidth usage

**Mini Example**:
- **Auto-scaling**: Add chat service instances based on connection count
- **Database sharding**: Partition messages by chat_id
- **CDN**: Global distribution for media files

---

## 8. Monitoring & Analytics

### Key Metrics
*[What to measure]*

**Performance Metrics**:
- **Message Latency**: < 100ms for 95% of messages
- **WebSocket Connections**: Active connections per server
- **Error Rate**: < 0.1% failed message deliveries
- **Availability**: 99.9% uptime

**Business Metrics**:
- **Daily Active Users**: 50M target
- **Messages per User**: Average messages sent per day
- **Group Chat Usage**: Percentage of group vs individual chats
- **Media Sharing**: Percentage of media messages

**Mini Example**:
- **Response Time**: < 100ms for 95% of message deliveries
- **Error Rate**: < 0.1% failed deliveries
- **Uptime**: 99.9% availability target

### Monitoring Tools
*[How to monitor]*

**Infrastructure Monitoring**:
- **APM**: New Relic for application performance
- **Logging**: ELK Stack for centralized logging
- **Alerting**: PagerDuty for incident management

**Mini Example**:
- **New Relic**: Monitor chat service performance
- **ELK Stack**: Aggregate logs from all services
- **PagerDuty**: Alert on service failures

---

## 9. Trade-offs & Decisions

### Technology Choices
*[Why specific technologies]*

**Database**:
- **PostgreSQL**: User data (ACID compliance, complex queries)
- **Cassandra**: Messages (high write throughput, horizontal scaling)
- **Redis**: Caching and presence data (fast access, pub/sub)

**Real-time Communication**:
- **WebSockets**: Full-duplex communication for real-time messaging
- **Long Polling**: Fallback for WebSocket failures
- **Server-Sent Events**: Alternative for one-way updates

**Mini Example**:
- **WebSockets**: Chosen for real-time bidirectional communication
- **Cassandra**: Chosen for high message write throughput
- **Redis**: Chosen for fast caching and pub/sub capabilities

### Design Decisions
*[Architecture choices]*

**Microservices vs Monolith**:
- **Microservices**: Independent scaling, technology diversity, fault isolation
- **Monolith**: Simpler deployment, easier debugging, lower latency

**Synchronous vs Asynchronous**:
- **Sync**: Message delivery (immediate consistency)
- **Async**: Push notifications, analytics (eventual consistency)

**Mini Example**:
- **Microservices**: Chosen for independent scaling of chat, media, notification services
- **Async**: Push notifications sent asynchronously via message queues

---

## 10. Future Considerations

### Scalability Roadmap
*[Growth plans]*

**Short-term** (3-6 months):
- **Performance**: Optimize message delivery latency
- **Monitoring**: Improve real-time monitoring and alerting
- **Security**: Implement end-to-end encryption

**Long-term** (6-12 months):
- **Architecture**: Consider event-driven architecture
- **Global**: Multi-region deployment for global users
- **Advanced**: Voice/video calling, message search, AI features

**Mini Example**:
- **Short-term**: Reduce message latency to < 50ms
- **Long-term**: Add voice/video calling capabilities

### Potential Challenges
*[Anticipate problems]*

**Technical Challenges**:
- **Message Ordering**: Ensuring message order in distributed system
- **Exactly Once Delivery**: Preventing duplicate messages
- **Media Storage Costs**: Managing 10TB daily media storage
- **WebSocket Scaling**: Managing millions of concurrent connections

**Business Challenges**:
- **Cost**: Infrastructure costs for 38PB storage over 10 years
- **Compliance**: Data privacy regulations (GDPR, etc.)
- **Competition**: Feature parity with other messaging apps

**Mini Example**:
- **Message ordering**: Use sequence numbers and timestamps
- **Cost management**: Implement media compression and cleanup policies

---

## Summary

### Key Design Decisions
1. **Microservices Architecture**: Independent scaling of chat, media, notification services
2. **WebSocket for Real-time**: Full-duplex communication for instant messaging
3. **Multi-database Approach**: PostgreSQL for users, Cassandra for messages, S3 for media
4. **Push Notifications**: Asynchronous delivery for offline users
5. **End-to-End Encryption**: Message privacy and security

### Estimated Resources
- **Chat Service**: 10 instances (auto-scaling)
- **Database**: 3 Cassandra clusters, 3 PostgreSQL instances
- **Storage**: 38 PB over 10 years
- **Bandwidth**: 120 MB/s peak
- **Cost**: $2-5M/month for infrastructure

### Success Metrics
- **Performance**: < 100ms message delivery, 99.9% uptime
- **Scalability**: Support 50M DAU, 2B messages/day
- **Reliability**: Zero message loss, exactly-once delivery

---

## Notes

### Assumptions
- 50M daily active users
- 40 messages per user per day
- 5% of messages contain media
- 100 bytes average text message size
- 100 KB average media file size
- 10-year data retention period

### Limitations
- No voice/video calling in initial design
- Limited message search functionality
- No message editing/deletion features
- Basic group management (max 100 members)

### Alternatives Considered
- **Monolithic architecture**: Rejected for scaling limitations
- **Long polling**: Rejected for resource inefficiency
- **Single database**: Rejected for performance bottlenecks
- **Client-side encryption only**: Rejected for server-side features

### References
- WhatsApp Engineering Blog
- Apache Cassandra documentation
- WebSocket protocol specification
- Firebase Cloud Messaging documentation
- Amazon S3 best practices
