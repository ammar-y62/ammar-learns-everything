# Twitter System Design

## Problem Statement
Design a social media platform similar to Twitter that allows users to post short messages (tweets), follow other users, view personalized newsfeeds, and search content for over 1 billion users globally.

**Mini Example**: Design a social media platform like Twitter

---

## 1. Requirements Clarification

### Functional Requirements
*[What the system must do]*
- **Core Features**:
  - Post tweets (text, images, videos) up to 280 characters
  - Follow/unfollow other users
  - View personalized newsfeed with tweets from followed users
  - Search tweets and users
  - Like/favorite tweets
  - Retweet functionality
- **User Actions**:
  - Create and publish tweets
  - Follow/unfollow users
  - View and interact with newsfeed
  - Search for content and users
  - Like and retweet posts
- **Edge Cases**:
  - Handle viral tweets with millions of views
  - Manage celebrity accounts with millions of followers
  - Handle trending topics and hashtags
  - Deal with spam and content moderation

**Mini Example**:
- Post a 280-character tweet with an image
- Follow a celebrity and see their tweets in newsfeed
- Search for tweets containing specific hashtags
- Like and retweet posts from other users

### Non-Functional Requirements
*[Quality constraints]*
- **Performance**:
  - < 200ms newsfeed loading time
  - Support 12K requests per second
  - Real-time tweet delivery
- **Scalability**:
  - Handle 200M daily active users
  - Support 1B tweets per day
  - Scale to 19PB storage over 10 years
- **Availability**: 99.9% uptime
- **Reliability**: Fast newsfeed generation, no data loss

**Mini Example**:
- 99.9% uptime requirement
- < 200ms response time for newsfeed
- Handle 12K requests/second peak load

### Extended Requirements
*[Nice-to-have features]*
- **Analytics**:
  - Tweet engagement metrics
  - User behavior tracking
  - Trending topics analysis
- **Security**:
  - Content moderation
  - User authentication
  - Spam detection
- **Additional Features**:
  - Push notifications for interactions
  - Trending topics and hashtags
  - User recommendations

**Mini Example**:
- Track tweet likes, retweets, and engagement
- Send push notifications for new followers
- Display trending hashtags and topics

---

## 2. Estimation and Constraints

### Scale Estimation
*[Back-of-envelope calculations]*

**Traffic Assumptions**:
- **Total Users**: 1 billion registered users
- **Daily Active Users (DAU)**: 200 million
- **Tweets per user per day**: 5
- **Total tweets per day**: 1 billion
- **Media tweets**: 10% of total (100 million files/day)

**Mini Example**:
- 200M users × 5 tweets = 1B tweets/day
- 10% media = 100M files/day
- 12K requests/second peak

**Storage Requirements**:
- **Text tweets**: 100 bytes per tweet
- **Daily text storage**: 1B × 100 bytes = 100 GB/day
- **Media files**: 50 KB average per file
- **Daily media storage**: 100M × 50 KB = 5 TB/day
- **10-year storage**: (5.1 TB/day) × 365 × 10 = 19 PB

**Mini Example**:
- 100 GB/day for text tweets
- 5 TB/day for media files
- 19 PB total over 10 years

**Bandwidth Requirements**:
- **Daily ingress**: 5.1 TB
- **Bandwidth needed**: 5.1 TB ÷ (24 × 3600) ≈ 60 MB/second

**Mini Example**:
- 60 MB/s bandwidth requirement
- Handles 5.1 TB daily data ingress

### Summary Table
| Metric | Estimate | Notes |
|--------|----------|-------|
| Total Users | 1B | Registered users |
| DAU | 200M | Daily active users |
| Tweets | 1B/day | Total tweets posted |
| RPS | 12K/s | Peak requests per second |
| Storage | 5.1 TB/day | Daily storage requirement |
| Bandwidth | 60 MB/s | Required bandwidth |
| Media Files | 100M/day | 10% of total tweets |

---

## 3. Data Model Design

### Database Schema
*[Define entities and relationships]*

**Core Tables**:
- **Users**:
  - Fields: id, username, email, name, bio, created_at, followers_count, following_count
  - Indexes: username (unique), email (unique), created_at
- **Tweets**:
  - Fields: id, user_id, content, type, media_url, created_at, likes_count, retweets_count
  - Indexes: user_id, created_at, type
- **Followers**:
  - Fields: follower_id, followee_id, created_at
  - Indexes: follower_id, followee_id (composite), followee_id
- **Likes**:
  - Fields: user_id, tweet_id, created_at
  - Indexes: user_id, tweet_id (composite), tweet_id
- **Retweets**:
  - Fields: user_id, original_tweet_id, created_at
  - Indexes: user_id, original_tweet_id (composite), original_tweet_id
- **Newsfeeds**:
  - Fields: user_id, tweet_id, created_at, score
  - Indexes: user_id, created_at, score

**Mini Example**:
- **Users**: id, username, email, name, followers_count
- **Tweets**: id, user_id, content, type, likes_count, retweets_count
- **Followers**: follower_id, followee_id (for follow relationships)
- **Likes**: user_id, tweet_id (for tweet interactions)

### Database Choice
*[SQL vs NoSQL decision]*
- **Microservices approach**: Split data across different services
- **User Service**: PostgreSQL for user data and relationships
- **Tweet Service**: Apache Cassandra for tweet storage and scalability
- **Search Service**: Elasticsearch for full-text search
- **Media Service**: Object storage (S3) for file storage
- **Reasoning**: Different data types and access patterns require specialized storage

**Mini Example**:
- **PostgreSQL**: User data and relationships (ACID compliance)
- **Cassandra**: Tweets (high write throughput, horizontal scaling)
- **Elasticsearch**: Search functionality (full-text search, analytics)
- **S3**: Media files (cost-effective, scalable object storage)

---

## 4. API Design

### Core APIs
*[Define system interfaces]*

```typescript
// Post a tweet
postTweet(userID: UUID, content: string, mediaURL?: string): boolean
// Example: postTweet("user123", "Hello Twitter!", "https://s3.com/image.jpg")

// Follow/unfollow a user
follow(followerID: UUID, followeeID: UUID): boolean
unfollow(followerID: UUID, followeeID: UUID): boolean
// Example: follow("user123", "user456")

// Get newsfeed
getNewsfeed(userID: UUID, page: number, limit: number): Tweet[]
// Example: getNewsfeed("user123", 1, 20): [tweet1, tweet2, ...]

// Like/unlike a tweet
likeTweet(userID: UUID, tweetID: UUID): boolean
unlikeTweet(userID: UUID, tweetID: UUID): boolean
// Example: likeTweet("user123", "tweet789")

// Retweet
retweet(userID: UUID, originalTweetID: UUID): boolean
// Example: retweet("user123", "tweet789")

// Search tweets
searchTweets(query: string, page: number, limit: number): Tweet[]
// Example: searchTweets("#technology", 1, 20): [tweet1, tweet2, ...]

// Get user profile
getUserProfile(userID: UUID): User
// Example: getUserProfile("user123"): {id, username, name, followers_count, ...}
```

### API Considerations
- **Authentication**: OAuth 2.0 with JWT tokens
- **Rate Limiting**: 300 tweets/day per user, 1000 API calls/hour
- **Error Handling**: Standard HTTP status codes with detailed error messages
- **Pagination**: Cursor-based pagination for newsfeed and search results

**Mini Example**:
- OAuth 2.0 authentication for all API calls
- 300 tweets/day rate limit per user
- Cursor-based pagination for efficient data retrieval

---

## 5. High-Level Architecture

### System Components
*[Core building blocks]*

1. **Client Layer**: Web app, iOS/Android mobile apps
2. **API Gateway**: Request routing, authentication, rate limiting
3. **Load Balancer**: Traffic distribution across services
4. **User Service**: User management, authentication, profiles
5. **Tweet Service**: Tweet creation, storage, retrieval
6. **Newsfeed Service**: Feed generation and delivery
7. **Search Service**: Full-text search and trending topics
8. **Media Service**: File upload/download, storage management
9. **Notification Service**: Push notifications for interactions
10. **Analytics Service**: Metrics collection and analysis
11. **Database Layer**: PostgreSQL, Cassandra, Redis, Elasticsearch
12. **Object Storage**: S3 for media files
13. **CDN**: Content delivery for media files
14. **Message Queue**: Kafka for event streaming

**Mini Example**:
- **API Gateway**: Route requests to appropriate services
- **Tweet Service**: Handle tweet creation and storage
- **Newsfeed Service**: Generate personalized feeds
- **Search Service**: Provide full-text search capabilities

### Data Flow
*[How data moves through the system]*

**Tweet Posting Flow**:
1. Client → API Gateway → Tweet Service
2. Tweet Service → Database (store tweet)
3. Tweet Service → Newsfeed Service (update feeds)
4. Tweet Service → Search Service (index for search)
5. Tweet Service → Notification Service (notify followers)
6. Response to Client

**Newsfeed Generation Flow**:
1. Client requests newsfeed
2. Newsfeed Service → Cache (check for cached feed)
3. If cache miss: Newsfeed Service → Database (fetch tweets)
4. Newsfeed Service → Ranking Algorithm (sort by relevance)
5. Return paginated results to Client

**Mini Example**:
- **Tweet Post**: User → API → Tweet Service → Database → Newsfeed Service → Followers
- **Newsfeed**: User → API → Newsfeed Service → Cache/Database → Ranked Results

---

## 6. Detailed Design

### Newsfeed Generation Strategies
*[Feed delivery approaches]*

**Pull Model (Fan-out on Load)**:
- Generate feed when user requests it
- Reduces write operations
- Increases read operations
- Better for users with many followers

**Push Model (Fan-out on Write)**:
- Push tweets to all followers' feeds immediately
- Reduces read operations
- Increases write operations
- Better for users with few followers

**Hybrid Model**:
- Push model for users with < 1000 followers
- Pull model for users with > 1000 followers
- Balanced approach for optimal performance

**Mini Example**:
- **Celebrity (1M followers)**: Pull model to avoid overwhelming writes
- **Regular user (500 followers)**: Push model for instant delivery
- **Hybrid**: Automatic switching based on follower count

### Ranking Algorithm
*[Content relevance scoring]*

**EdgeRank Formula**:
```
Rank = Affinity × Weight × Decay
```

**Factors**:
- **Affinity**: User interaction history with tweet author
- **Weight**: Engagement type (comment > like > view)
- **Decay**: Time since tweet creation
- **Additional**: User interests, trending topics, content type

**Mini Example**:
- **High affinity**: User frequently likes author's tweets
- **High weight**: Tweet with many comments and retweets
- **Low decay**: Recent tweet (within last hour)

### Caching Strategy
*[Performance optimization]*

**Cache Levels**:
- **Application Cache**: In-memory caching for user sessions
- **Distributed Cache**: Redis for newsfeeds and trending topics
- **CDN**: Static media content delivery

**Cache Policies**:
- **Eviction**: LRU for newsfeeds, TTL for trending topics
- **Consistency**: Cache-aside for feeds, write-through for user data

**Mini Example**:
- **Redis**: Cache user newsfeeds (last 100 tweets)
- **LRU eviction**: Remove least recently accessed feeds
- **TTL**: 1 hour for newsfeeds, 5 minutes for trending topics

### Data Partitioning
*[Scalability strategy]*

**Partitioning Strategies**:
- **Hash-based**: Partition tweets by user_id for even distribution
- **Range-based**: Partition by timestamp for historical data
- **List-based**: Partition by user_id for user-specific data

**Mini Example**:
- **Tweet partitioning**: Hash by user_id for even distribution
- **Newsfeed partitioning**: Partition by user_id for personalized feeds
- **Search partitioning**: Shard by content type and timestamp

### Security Considerations
*[Protection mechanisms]*

**Authentication & Authorization**:
- **OAuth 2.0**: Third-party authentication
- **JWT Tokens**: Stateless authentication for API access
- **Rate Limiting**: Prevent abuse and spam

**Data Protection**:
- **Content Moderation**: AI-powered spam and abuse detection
- **Input Validation**: Sanitize all user inputs
- **Encryption**: Data encryption at rest and in transit

**Mini Example**:
- **OAuth 2.0**: Secure third-party authentication
- **Content moderation**: AI filters for inappropriate content
- **Rate limiting**: 300 tweets/day per user

---

## 7. Bottleneck Analysis & Resolution

### Single Points of Failure
*[Identify and resolve]*

**Potential Issues**:
- **Newsfeed Service**: Single service handling all feed generation
- **Database**: Single database instance
- **Search Service**: Single Elasticsearch cluster
- **API Gateway**: Single entry point
- **Media Storage**: Single object storage instance

**Solutions**:
- **Multiple Newsfeed Service instances**: Load balanced across regions
- **Database clustering**: Primary + read replicas with failover
- **Search clustering**: Multiple Elasticsearch nodes
- **Multiple API Gateways**: Active-passive configuration
- **Multi-region object storage**: S3 with cross-region replication

**Mini Example**:
- **Newsfeed Service**: 5 instances with load balancer
- **Database**: Primary + 3 read replicas
- **Elasticsearch**: 3-node cluster for search
- **API Gateway**: Active-passive with health checks

### Scalability Improvements
*[Handle growth]*

**Horizontal Scaling**:
- **Newsfeed Service**: Auto-scaling based on request volume
- **Database**: Sharding by user_id for tweet storage
- **Search Service**: Multiple Elasticsearch clusters
- **Media Service**: Multiple instances with CDN distribution

**Vertical Scaling**:
- **Database optimization**: Query optimization, proper indexing
- **Connection pooling**: Efficient database connections
- **Content compression**: Reduce bandwidth usage

**Mini Example**:
- **Auto-scaling**: Add newsfeed service instances based on request count
- **Database sharding**: Partition tweets by user_id
- **CDN**: Global distribution for media files

---

## 8. Monitoring & Analytics

### Key Metrics
*[What to measure]*

**Performance Metrics**:
- **Newsfeed Latency**: < 200ms for 95% of requests
- **Tweet Posting**: < 100ms for 95% of tweets
- **Search Response**: < 500ms for search queries
- **Availability**: 99.9% uptime

**Business Metrics**:
- **Daily Active Users**: 200M target
- **Tweets per User**: Average tweets per day
- **Engagement Rate**: Likes, retweets, comments per tweet
- **User Retention**: Daily/weekly/monthly active users

**Mini Example**:
- **Response Time**: < 200ms for 95% of newsfeed requests
- **Engagement**: 5% average engagement rate per tweet
- **Uptime**: 99.9% availability target

### Monitoring Tools
*[How to monitor]*

**Infrastructure Monitoring**:
- **APM**: New Relic for application performance
- **Logging**: ELK Stack for centralized logging
- **Alerting**: PagerDuty for incident management

**Mini Example**:
- **New Relic**: Monitor newsfeed service performance
- **ELK Stack**: Aggregate logs from all services
- **PagerDuty**: Alert on service failures

---

## 9. Trade-offs & Decisions

### Technology Choices
*[Why specific technologies]*

**Database**:
- **PostgreSQL**: User data and relationships (ACID compliance)
- **Cassandra**: Tweets (high write throughput, horizontal scaling)
- **Elasticsearch**: Search functionality (full-text search, analytics)
- **Redis**: Caching and session management (fast access)

**Newsfeed Generation**:
- **Push Model**: Immediate delivery for users with few followers
- **Pull Model**: Efficient for users with many followers
- **Hybrid Model**: Balanced approach based on follower count

**Mini Example**:
- **Cassandra**: Chosen for high tweet write throughput
- **Elasticsearch**: Chosen for advanced search capabilities
- **Hybrid Model**: Chosen for optimal performance across user types

### Design Decisions
*[Architecture choices]*

**Microservices vs Monolith**:
- **Microservices**: Independent scaling, technology diversity, fault isolation
- **Monolith**: Simpler deployment, easier debugging, lower latency

**Synchronous vs Asynchronous**:
- **Sync**: Tweet posting (immediate consistency)
- **Async**: Newsfeed updates, notifications (eventual consistency)

**Mini Example**:
- **Microservices**: Chosen for independent scaling of tweet, newsfeed, search services
- **Async**: Newsfeed updates sent asynchronously via message queues

---

## 10. Future Considerations

### Scalability Roadmap
*[Growth plans]*

**Short-term** (3-6 months):
- **Performance**: Optimize newsfeed generation latency
- **Monitoring**: Improve real-time monitoring and alerting
- **Content Moderation**: Enhance AI-powered spam detection

**Long-term** (6-12 months):
- **Architecture**: Consider event-driven architecture
- **Global**: Multi-region deployment for global users
- **Advanced**: Video streaming, live audio spaces, AI recommendations

**Mini Example**:
- **Short-term**: Reduce newsfeed latency to < 100ms
- **Long-term**: Add live audio spaces and video streaming

### Potential Challenges
*[Anticipate problems]*

**Technical Challenges**:
- **Newsfeed Generation**: Handling users with millions of followers
- **Search Scalability**: Managing billions of tweets in search index
- **Media Storage Costs**: Managing 5TB daily media storage
- **Content Moderation**: Real-time spam and abuse detection

**Business Challenges**:
- **Cost**: Infrastructure costs for 19PB storage over 10 years
- **Compliance**: Data privacy regulations (GDPR, etc.)
- **Competition**: Feature parity with other social platforms

**Mini Example**:
- **Newsfeed optimization**: Use hybrid model for celebrity accounts
- **Cost management**: Implement media compression and cleanup policies

---

## Summary

### Key Design Decisions
1. **Microservices Architecture**: Independent scaling of tweet, newsfeed, search services
2. **Hybrid Newsfeed Model**: Push for regular users, pull for celebrities
3. **Multi-database Approach**: PostgreSQL for users, Cassandra for tweets, Elasticsearch for search
4. **Real-time Analytics**: Kafka for event streaming and analytics
5. **Content Moderation**: AI-powered spam and abuse detection

### Estimated Resources
- **Newsfeed Service**: 10 instances (auto-scaling)
- **Database**: 3 Cassandra clusters, 3 PostgreSQL instances, 3 Elasticsearch nodes
- **Storage**: 19 PB over 10 years
- **Bandwidth**: 60 MB/s peak
- **Cost**: $3-8M/month for infrastructure

### Success Metrics
- **Performance**: < 200ms newsfeed loading, 99.9% uptime
- **Scalability**: Support 200M DAU, 1B tweets/day
- **Reliability**: Fast newsfeed generation, comprehensive search

---

## Notes

### Assumptions
- 1B total users, 200M daily active users
- 5 tweets per user per day
- 10% of tweets contain media
- 100 bytes average tweet size
- 50 KB average media file size
- 10-year data retention period

### Limitations
- No direct messaging in initial design
- Limited video streaming capabilities
- Basic content moderation features
- No advanced recommendation algorithms

### Alternatives Considered
- **Monolithic architecture**: Rejected for scaling limitations
- **Single database**: Rejected for performance bottlenecks
- **Pure push model**: Rejected for celebrity account inefficiency
- **Client-side search**: Rejected for performance and security

### References
- Twitter Engineering Blog
- Apache Cassandra documentation
- Elasticsearch best practices
- Apache Kafka documentation
- Amazon S3 best practices