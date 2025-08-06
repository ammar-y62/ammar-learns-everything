# Netflix System Design

## Problem Statement
Design a video streaming platform similar to Netflix that allows users to stream movies, TV shows, and other content with high-quality video delivery, personalized recommendations, and global content distribution for over 1 billion users worldwide.

**Mini Example**: Design a video streaming platform like Netflix

---

## 1. Requirements Clarification

### Functional Requirements
*[What the system must do]*
- **Core Features**:
  - Stream videos (movies, TV shows, documentaries)
  - Upload and process video content
  - Search videos by title, genre, or tags
  - Comment on videos (like YouTube)
  - Resume playback from where user left off
  - Share videos with others
- **User Actions**:
  - Browse and search content
  - Stream videos in different qualities
  - Add comments and ratings
  - Create watchlists and favorites
  - Resume watching from last position
- **Edge Cases**:
  - Handle high-definition video streaming (4K, 8K)
  - Manage geo-blocked content restrictions
  - Deal with network connectivity issues
  - Handle massive video file uploads

**Mini Example**:
- Stream a 4K movie with adaptive bitrate
- Search for "action movies" and get personalized results
- Resume watching from 45 minutes into a 2-hour movie
- Comment on a TV show episode

### Non-Functional Requirements
*[Quality constraints]*
- **Performance**:
  - < 2 seconds video start time
  - Support 12K requests per second
  - Adaptive bitrate streaming
- **Scalability**:
  - Handle 200M daily active users
  - Support 1B video views per day
  - Scale to 1,825 PB storage over 10 years
- **Availability**: 99.9% uptime
- **Reliability**: No video uploads lost, seamless streaming

**Mini Example**:
- 99.9% uptime requirement
- < 2 seconds video start time
- Handle 12K requests/second peak load

### Extended Requirements
*[Nice-to-have features]*
- **Analytics**:
  - View metrics and engagement tracking
  - Content performance analytics
  - User behavior analysis
- **Security**:
  - Content geo-blocking
  - Digital rights management (DRM)
  - User authentication and authorization
- **Additional Features**:
  - Personalized recommendations
  - Multiple video qualities (4K, 1080p, 720p)
  - Offline download capability

**Mini Example**:
- Track video views, watch time, and completion rates
- Block content based on user's geographic location
- Recommend similar content based on viewing history

---

## 2. Estimation and Constraints

### Scale Estimation
*[Back-of-envelope calculations]*

**Traffic Assumptions**:
- **Total Users**: 1 billion registered users
- **Daily Active Users (DAU)**: 200 million
- **Videos watched per user per day**: 5
- **Total video views per day**: 1 billion
- **Read/Write ratio**: 200:1
- **Videos uploaded per day**: 5 million

**Mini Example**:
- 200M users × 5 videos = 1B video views/day
- 200:1 ratio = 5M uploads/day
- 12K requests/second peak

**Storage Requirements**:
- **Video files**: 100 MB average per video
- **Daily video storage**: 5M × 100 MB = 500 TB/day
- **10-year storage**: 500 TB × 365 × 10 = 1,825 PB

**Mini Example**:
- 500 TB/day for video uploads
- 1,825 PB total over 10 years
- Massive storage requirements for video content

**Bandwidth Requirements**:
- **Daily ingress**: 500 TB
- **Bandwidth needed**: 500 TB ÷ (24 × 3600) ≈ 5.8 GB/second

**Mini Example**:
- 5.8 GB/s bandwidth requirement
- Handles 500 TB daily video uploads

### Summary Table
| Metric | Estimate | Notes |
|--------|----------|-------|
| Total Users | 1B | Registered users |
| DAU | 200M | Daily active users |
| Video Views | 1B/day | Total videos watched |
| Uploads | 5M/day | New content uploaded |
| RPS | 12K/s | Peak requests per second |
| Storage | 500 TB/day | Daily storage requirement |
| Bandwidth | 5.8 GB/s | Required bandwidth |
| 10-Year Storage | 1,825 PB | Total storage needed |

---

## 3. Data Model Design

### Database Schema
*[Define entities and relationships]*

**Core Tables**:
- **Users**:
  - Fields: id, email, name, subscription_type, created_at, last_login
  - Indexes: email (unique), subscription_type, created_at
- **Videos**:
  - Fields: id, title, description, duration, file_path, quality_levels, created_at, user_id
  - Indexes: title, created_at, user_id, quality_levels
- **Tags**:
  - Fields: id, name, category
  - Indexes: name, category
- **Video_Tags**:
  - Fields: video_id, tag_id
  - Indexes: video_id, tag_id (composite)
- **Views**:
  - Fields: id, user_id, video_id, watch_time, last_position, created_at
  - Indexes: user_id, video_id, created_at
- **Comments**:
  - Fields: id, user_id, video_id, content, created_at
  - Indexes: user_id, video_id, created_at
- **Watchlists**:
  - Fields: user_id, video_id, added_at
  - Indexes: user_id, added_at

**Mini Example**:
- **Users**: id, email, name, subscription_type
- **Videos**: id, title, duration, file_path, quality_levels
- **Views**: user_id, video_id, watch_time, last_position
- **Comments**: user_id, video_id, content

### Database Choice
*[SQL vs NoSQL decision]*
- **Microservices approach**: Split data across different services
- **User Service**: PostgreSQL for user data and subscriptions
- **Video Service**: Apache Cassandra for video metadata and scalability
- **Search Service**: Elasticsearch for full-text search and recommendations
- **Media Service**: Object storage (S3) for video files
- **Analytics Service**: ClickHouse for analytics and metrics
- **Reasoning**: Different data types and access patterns require specialized storage

**Mini Example**:
- **PostgreSQL**: User data and subscriptions (ACID compliance)
- **Cassandra**: Video metadata (high write throughput, horizontal scaling)
- **Elasticsearch**: Search and recommendations (full-text search, analytics)
- **S3**: Video files (cost-effective, scalable object storage)

---

## 4. API Design

### Core APIs
*[Define system interfaces]*

```typescript
// Upload a video
uploadVideo(title: string, description: string, data: Stream<byte>, tags?: string[]): boolean
// Example: uploadVideo("Action Movie", "Epic action scenes", videoStream, ["action", "thriller"])

// Stream a video
streamVideo(videoID: UUID, codec: string, resolution: string, offset?: number): VideoStream
// Example: streamVideo("video123", "h264", "1080p", 2700): video data stream

// Search videos
searchVideos(query: string, filters: SearchFilters, page: number): Video[]
// Example: searchVideos("action movies", {genre: "action", year: 2023}, 1): [video1, video2, ...]

// Add comment
addComment(videoID: UUID, userID: UUID, content: string): boolean
// Example: addComment("video123", "user456", "Great movie!")

// Get recommendations
getRecommendations(userID: UUID, limit: number): Video[]
// Example: getRecommendations("user123", 20): [video1, video2, ...]

// Update watch progress
updateWatchProgress(userID: UUID, videoID: UUID, position: number): boolean
// Example: updateWatchProgress("user123", "video456", 2700): true

// Get video details
getVideoDetails(videoID: UUID): VideoDetails
// Example: getVideoDetails("video123"): {title, description, duration, quality_levels, ...}
```

### API Considerations
- **Authentication**: OAuth 2.0 with JWT tokens
- **Rate Limiting**: 1000 API calls/hour per user
- **Error Handling**: Standard HTTP status codes with detailed error messages
- **Pagination**: Cursor-based pagination for search results
- **Geo-blocking**: Location-based content restrictions

**Mini Example**:
- OAuth 2.0 authentication for all API calls
- 1000 API calls/hour rate limit per user
- Geo-blocking based on user's IP address

---

## 5. High-Level Architecture

### System Components
*[Core building blocks]*

1. **Client Layer**: Web app, iOS/Android mobile apps, Smart TV apps
2. **API Gateway**: Request routing, authentication, rate limiting
3. **Load Balancer**: Traffic distribution across services
4. **User Service**: User management, authentication, subscriptions
5. **Video Service**: Video metadata, streaming coordination
6. **Media Service**: Video upload, processing, storage
7. **Search Service**: Full-text search and recommendations
8. **Analytics Service**: Metrics collection and analysis
9. **CDN/Open Connect**: Content delivery network
10. **Video Processing Pipeline**: Transcoding and quality conversion
11. **Database Layer**: PostgreSQL, Cassandra, Redis, Elasticsearch
12. **Object Storage**: S3 for video files
13. **Message Queue**: Kafka for video processing events
14. **Geo-blocking Service**: Location-based content restrictions

**Mini Example**:
- **API Gateway**: Route requests to appropriate services
- **Video Service**: Handle video metadata and streaming coordination
- **Media Service**: Process and store video files
- **CDN**: Deliver video content globally

### Data Flow
*[How data moves through the system]*

**Video Upload Flow**:
1. Client → API Gateway → Media Service
2. Media Service → Object Storage (store raw video)
3. Media Service → Message Queue (trigger processing)
4. Processing Pipeline → Transcode video
5. Processing Pipeline → Multiple quality versions
6. Processing Pipeline → CDN (distribute content)
7. Response to Client

**Video Streaming Flow**:
1. Client requests video stream
2. API Gateway → Video Service (get metadata)
3. Video Service → CDN (get video chunks)
4. CDN → Client (adaptive bitrate streaming)
5. Client → Analytics Service (track viewing metrics)

**Mini Example**:
- **Video Upload**: User → API → Media Service → Storage → Processing Pipeline → CDN
- **Video Streaming**: User → API → Video Service → CDN → Adaptive Streaming

---

## 6. Detailed Design

### Video Processing Pipeline
*[Content processing workflow]*

**File Chunking**:
- Split videos into scene-based chunks (not time-based)
- Reduces network interruptions
- Better user experience with complete scenes
- Eliminates duplicate data on storage

**Content Filter**:
- ML-powered copyright and NSFW detection
- Piracy and content policy enforcement
- Dead letter queue for manual review
- Pre-approved content for Netflix originals

**Transcoder**:
- Convert to optimized formats (H.264, H.265, VP9)
- Reduce file sizes while maintaining quality
- Use FFmpeg or AWS Elemental MediaConvert
- Multiple codec support for different devices

**Quality Conversion**:
- Generate multiple resolutions (4K, 1440p, 1080p, 720p, 480p)
- Adaptive bitrate streaming support
- Upload to distributed storage (S3, HDFS)
- Thumbnail and subtitle generation

**Mini Example**:
- **Scene-based chunking**: Split at natural scene boundaries
- **Multi-quality**: Generate 5 different resolutions per video
- **ML filtering**: Detect copyrighted content automatically

### Adaptive Bitrate Streaming
*[Dynamic quality adjustment]*

**HLS (HTTP Live Streaming)**:
- Segment-based streaming protocol
- Dynamic quality switching based on network
- Reduces buffering and improves experience
- Multiple quality levels per video

**Quality Selection**:
- Monitor network conditions in real-time
- Switch quality levels seamlessly
- Buffer management for smooth playback
- Fallback to lower quality if needed

**Mini Example**:
- **Network monitoring**: Track bandwidth and latency
- **Quality switching**: Seamlessly switch between 4K and 1080p
- **Buffer management**: Maintain 10-30 seconds of buffer

### Content Delivery Network
*[Global content distribution]*

**Netflix Open Connect**:
- Purpose-built CDN for video delivery
- Direct ISP partnerships worldwide
- 95% of traffic delivered via Open Connect
- 1000+ locations globally

**Traditional CDN Fallback**:
- CloudFront, Cloudflare for backup
- Geographic distribution
- Edge caching for popular content
- Load balancing across regions

**Mini Example**:
- **Open Connect**: Direct delivery to ISPs for 95% of traffic
- **Edge caching**: Cache popular content at edge locations
- **Geographic routing**: Route users to nearest CDN location

### Caching Strategy
*[Performance optimization]*

**Cache Levels**:
- **Application Cache**: In-memory caching for user sessions
- **Distributed Cache**: Redis for video metadata and recommendations
- **CDN Cache**: Edge caching for video content
- **Browser Cache**: Client-side caching for thumbnails

**Cache Policies**:
- **Eviction**: LRU for metadata, TTL for recommendations
- **Consistency**: Cache-aside for metadata, write-through for user data

**Mini Example**:
- **Redis**: Cache video metadata and user recommendations
- **LRU eviction**: Remove least recently accessed content
- **TTL**: 1 hour for recommendations, 24 hours for metadata

### Data Partitioning
*[Scalability strategy]*

**Partitioning Strategies**:
- **Hash-based**: Partition videos by video_id for even distribution
- **Range-based**: Partition by upload date for historical data
- **List-based**: Partition by user_id for user-specific data

**Mini Example**:
- **Video partitioning**: Hash by video_id for even distribution
- **User data**: Partition by user_id for personalized content
- **Analytics**: Shard by date for time-series data

### Security Considerations
*[Protection mechanisms]*

**Authentication & Authorization**:
- **OAuth 2.0**: Third-party authentication
- **JWT Tokens**: Stateless authentication for API access
- **Subscription Validation**: Check user subscription status

**Content Protection**:
- **DRM**: Digital rights management for premium content
- **Geo-blocking**: Location-based content restrictions
- **Rate Limiting**: Prevent abuse and bandwidth consumption

**Mini Example**:
- **OAuth 2.0**: Secure third-party authentication
- **DRM**: Protect premium content from unauthorized access
- **Geo-blocking**: Block content based on user's location

---

## 7. Bottleneck Analysis & Resolution

### Single Points of Failure
*[Identify and resolve]*

**Potential Issues**:
- **Video Processing Pipeline**: Single pipeline handling all uploads
- **CDN**: Single content delivery network
- **Database**: Single database instance
- **Search Service**: Single Elasticsearch cluster
- **API Gateway**: Single entry point

**Solutions**:
- **Multiple processing pipelines**: Parallel processing across regions
- **Multi-CDN strategy**: Open Connect + traditional CDN fallback
- **Database clustering**: Primary + read replicas with failover
- **Search clustering**: Multiple Elasticsearch nodes
- **Multiple API Gateways**: Active-passive configuration

**Mini Example**:
- **Processing Pipeline**: 3 parallel pipelines with load balancing
- **CDN**: Open Connect + CloudFront fallback
- **Database**: Primary + 3 read replicas
- **API Gateway**: Active-passive with health checks

### Scalability Improvements
*[Handle growth]*

**Horizontal Scaling**:
- **Video Service**: Auto-scaling based on streaming demand
- **Processing Pipeline**: Multiple instances for parallel processing
- **Search Service**: Multiple Elasticsearch clusters
- **CDN**: Global distribution with edge locations

**Vertical Scaling**:
- **Database optimization**: Query optimization, proper indexing
- **Connection pooling**: Efficient database connections
- **Video compression**: Advanced codecs to reduce bandwidth

**Mini Example**:
- **Auto-scaling**: Add video service instances based on streaming load
- **Parallel processing**: Multiple transcoding instances
- **Global CDN**: Edge locations in 100+ countries

---

## 8. Monitoring & Analytics

### Key Metrics
*[What to measure]*

**Performance Metrics**:
- **Video Start Time**: < 2 seconds for 95% of videos
- **Streaming Quality**: Adaptive bitrate success rate
- **CDN Performance**: Cache hit ratio, latency
- **Availability**: 99.9% uptime

**Business Metrics**:
- **Daily Active Users**: 200M target
- **Video Views**: Average videos watched per user
- **Engagement Rate**: Watch time, completion rates
- **Content Performance**: Popular videos, trending content

**Mini Example**:
- **Response Time**: < 2 seconds for 95% of video starts
- **Engagement**: 70% average watch time completion
- **Uptime**: 99.9% availability target

### Monitoring Tools
*[How to monitor]*

**Infrastructure Monitoring**:
- **APM**: New Relic for application performance
- **Logging**: ELK Stack for centralized logging
- **Alerting**: PagerDuty for incident management

**Mini Example**:
- **New Relic**: Monitor video streaming performance
- **ELK Stack**: Aggregate logs from all services
- **PagerDuty**: Alert on service failures

---

## 9. Trade-offs & Decisions

### Technology Choices
*[Why specific technologies]*

**Database**:
- **PostgreSQL**: User data and subscriptions (ACID compliance)
- **Cassandra**: Video metadata (high write throughput, horizontal scaling)
- **Elasticsearch**: Search and recommendations (full-text search, analytics)
- **ClickHouse**: Analytics (columnar storage, fast queries)

**Video Processing**:
- **FFmpeg**: Open-source transcoding (cost-effective, flexible)
- **AWS Elemental**: Cloud-based processing (managed, scalable)
- **HLS**: Adaptive streaming (reliability, wide support)

**Mini Example**:
- **Cassandra**: Chosen for high video metadata write throughput
- **Elasticsearch**: Chosen for advanced search and recommendation capabilities
- **HLS**: Chosen for reliable adaptive streaming

### Design Decisions
*[Architecture choices]*

**Microservices vs Monolith**:
- **Microservices**: Independent scaling, technology diversity, fault isolation
- **Monolith**: Simpler deployment, easier debugging, lower latency

**Synchronous vs Asynchronous**:
- **Sync**: Video streaming (immediate delivery)
- **Async**: Video processing, analytics (eventual consistency)

**Mini Example**:
- **Microservices**: Chosen for independent scaling of video, search, analytics services
- **Async**: Video processing sent asynchronously via message queues

---

## 10. Future Considerations

### Scalability Roadmap
*[Growth plans]*

**Short-term** (3-6 months):
- **Performance**: Optimize video start time
- **Monitoring**: Improve real-time monitoring and alerting
- **Content Processing**: Enhance transcoding pipeline

**Long-term** (6-12 months):
- **Architecture**: Consider event-driven architecture
- **Global**: Expand Open Connect network
- **Advanced**: 8K streaming, VR content, interactive videos

**Mini Example**:
- **Short-term**: Reduce video start time to < 1 second
- **Long-term**: Add 8K streaming and VR content support

### Potential Challenges
*[Anticipate problems]*

**Technical Challenges**:
- **Storage Costs**: Managing 1,825 PB over 10 years
- **Bandwidth**: Handling 5.8 GB/s peak bandwidth
- **Video Processing**: Processing 5M videos daily
- **Global Distribution**: Delivering content worldwide

**Business Challenges**:
- **Cost**: Infrastructure costs for massive storage and bandwidth
- **Compliance**: Content licensing and geo-blocking regulations
- **Competition**: Feature parity with other streaming platforms

**Mini Example**:
- **Storage optimization**: Implement intelligent compression and cleanup
- **Cost management**: Use tiered storage and CDN optimization

---

## Summary

### Key Design Decisions
1. **Microservices Architecture**: Independent scaling of video, search, analytics services
2. **Netflix Open Connect**: Purpose-built CDN for global video delivery
3. **Multi-database Approach**: PostgreSQL for users, Cassandra for videos, Elasticsearch for search
4. **Video Processing Pipeline**: Scene-based chunking and multi-quality transcoding
5. **Adaptive Bitrate Streaming**: HLS for dynamic quality adjustment

### Estimated Resources
- **Video Service**: 15 instances (auto-scaling)
- **Processing Pipeline**: 10 parallel instances
- **Database**: 3 Cassandra clusters, 3 PostgreSQL instances, 3 Elasticsearch nodes
- **Storage**: 1,825 PB over 10 years
- **Bandwidth**: 5.8 GB/s peak
- **Cost**: $10-25M/month for infrastructure

### Success Metrics
- **Performance**: < 2 seconds video start, 99.9% uptime
- **Scalability**: Support 200M DAU, 1B video views/day
- **Reliability**: Seamless streaming, no upload losses

---

## Notes

### Assumptions
- 1B total users, 200M daily active users
- 5 videos watched per user per day
- 100 MB average video size
- 200:1 read/write ratio
- 10-year data retention period

### Limitations
- No live streaming in initial design
- Limited interactive content features
- Basic recommendation algorithms
- No advanced DRM features

### Alternatives Considered
- **Monolithic architecture**: Rejected for scaling limitations
- **Single database**: Rejected for performance bottlenecks
- **Traditional CDN only**: Rejected for cost and performance
- **Client-side processing**: Rejected for security and performance

### References
- Netflix Engineering Blog
- Apache Cassandra documentation
- Elasticsearch best practices
- FFmpeg documentation
- AWS Elemental MediaConvert documentation