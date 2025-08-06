# System Design Interviews: Comprehensive Guide

## Overview

System design interviews evaluate your capability to produce technical solutions to abstract problems. They are **not designed for specific answers** but rather assess your problem-solving approach and technical depth.

### Key Characteristics
- **Two-way nature**: Interactive between candidate and interviewer
- **Level-dependent expectations**: Different for junior vs senior engineers
- **Vague/abstract problems**: Require clarification and scope definition
- **No single strategy**: Adapts based on experience level

## Common Strategies for System Design Interviews

### 1. Requirements Clarifications

System design questions are inherently vague. **Always start by clarifying requirements** before diving into solutions.

#### Three Types of Requirements:

**Functional Requirements** (Must-have features)
- Basic functionalities the system must offer
- Part of the contract with end users
- Examples:
  - "What features do we need to design?"
  - "What edge cases should we consider?"

**Non-Functional Requirements** (Quality constraints)
- Performance, scalability, reliability, security, etc.
- Varies in priority by project
- Examples:
  - "Each request should be processed with minimum latency"
  - "System should be highly available"

**Extended Requirements** (Nice-to-have)
- Out of scope but valuable additions
- Examples:
  - "System should record metrics and analytics"
  - "Service health and performance monitoring"

### 2. Estimation and Constraints

**Critical questions to ask:**
- What is the desired scale?
- What is the read/write ratio?
- How many requests per second?
- How much storage will be needed?

**Why this matters:**
- Helps scale design appropriately
- Influences technology choices
- Determines infrastructure requirements

### 3. Data Model Design

**Early-stage database schema definition:**
- Define all entities and relationships
- Understand data flow (core of every system)
- Questions to consider:
  - What are the different entities?
  - What are the relationships between entities?
  - How many tables do we need?
  - Is NoSQL a better choice?

### 4. API Design

**Define system interfaces explicitly:**
- Simple interface definitions (no code needed)
- Parameters, functions, classes, types, entities
- Example: `createUser(name: string, email: string): User`
- Keep interfaces simple initially
- Revisit for extended requirements

### 5. High-Level Component Design

**Identify system components:**
- Load balancers, API gateways, databases, etc.
- Choose architecture (monolithic vs microservices)
- Draft first system design diagram
- Discuss client perspective workflow

### 6. Detailed Design

**Deep dive into major components:**
- Demonstrate expertise in your areas
- Present different approaches with pros/cons
- Explain design decisions with examples
- Discuss additional features (optional)
- Key questions:
  - How should we partition data?
  - What about load distribution?
  - Should we use cache?
  - How handle traffic spikes?

**Important:** Be humble about knowledge gaps. Avoid overly opinionated statements about technologies.

### 7. Identify and Resolve Bottlenecks

**Critical questions:**
- Do we have enough database replicas?
- Is there any single point of failure?
- Is database sharding required?
- How can we make the system more robust?
- How to improve cache availability?

**Pro tip:** Read the company's engineering blog to understand their tech stack and priorities.

---

## URL Shortener System Design Example

### What is a URL Shortener?

A service that creates short aliases for long URLs. Users are redirected to the original URL when visiting short links.

**Example:**
- Long URL: `https://karanpratapsingh.com/courses/system-design/url-shortener`
- Short URL: `https://bit.ly/3I71d3o`

### Why URL Shorteners?

1. **Space saving** when sharing URLs
2. **Reduced typos** with shorter URLs
3. **Cross-device optimization**
4. **Link tracking** capabilities

### Requirements

#### Functional Requirements
- Generate shorter, unique aliases for given URLs
- Redirect users to original URL when visiting short links
- Links expire after default timespan

#### Non-Functional Requirements
- High availability with minimal latency
- Scalable and efficient system

#### Extended Requirements
- Prevent service abuse
- Record analytics and metrics for redirections

### Estimation and Constraints

#### Traffic Assumptions
- **Read/Write Ratio**: 100:1 (read-heavy system)
- **New URLs per month**: 100 million
- **Reads per month**: 100 × 100 million = 10 billion/month
- **Writes per month**: 1 × 100 million = 100 million/month

#### Requests Per Second (RPS)
- **Writes**: 100 million ÷ (30 days × 24 hrs × 3600 seconds) ≈ 40 URLs/second
- **Reads**: 100 × 40 URLs/second = 4,000 requests/second

#### Bandwidth Calculations
- **Incoming data** (writes): 40 × 500 bytes = 20 KB/second
- **Outgoing data** (reads): 4,000 × 500 bytes ≈ 2 MB/second

#### Storage Requirements
- **Retention period**: 10 years
- **Total records**: 100 million × 10 years × 12 months = 12 billion
- **Storage needed**: 12 billion × 500 bytes = 6 TB

#### Cache Requirements
- **Pareto principle**: 80% of requests for 20% of data
- **Daily requests**: 4,000 × 24 × 3600 ≈ 350 million/day
- **Cache memory**: 20% × 350 million × 500 bytes = 35 GB/day

#### Summary Table
| Type | Estimate |
|------|----------|
| Writes (New URLs) | 40/s |
| Reads (Redirection) | 4K/s |
| Bandwidth (Incoming) | 20 KB/s |
| Bandwidth (Outgoing) | 2 MB/s |
| Storage (10 years) | 6 TB |
| Memory (Caching) | ~35 GB/day |

### Data Model Design

#### Database Schema

**Users Table:**
- Stores user details (name, email, createdAt, etc.)

**URLs Table:**
- Contains short URL properties
- Fields: expiration, hash, originalURL, userID
- Hash column as index for performance

#### Database Choice
- **NoSQL preferred**: Amazon DynamoDB, Apache Cassandra, MongoDB
- **SQL alternative**: Azure SQL Database, Amazon RDS
- **Reasoning**: Data not strongly relational

### API Design

#### Create URL
```typescript
createURL(apiKey: string, originalURL: string, expiration?: Date): string
```
- **Parameters**: API key, original URL, optional expiration
- **Returns**: Short URL
- **Purpose**: Create new short URL

#### Get URL
```typescript
getURL(apiKey: string, shortURL: string): string
```
- **Parameters**: API key, short URL
- **Returns**: Original URL
- **Purpose**: Retrieve original URL for redirection

#### Delete URL
```typescript
deleteURL(apiKey: string, shortURL: string): boolean
```
- **Parameters**: API key, short URL
- **Returns**: Success status
- **Purpose**: Delete short URL

#### API Key Purpose
- **Prevent abuse**: Rate limiting per user
- **Standard practice**: Common in developer APIs
- **Security**: Covers extended requirements

### URL Encoding Approaches

#### 1. Base62 Approach
- **Characters**: A-Z, a-z, 0-9 (62 total)
- **Formula**: Number of URLs = 62^N (N = characters)
- **Examples**:
  - 5 chars: ~916 million URLs
  - 6 chars: ~56.8 billion URLs
  - 7 chars: ~3.5 trillion URLs
- **Pros**: Simple implementation
- **Cons**: No collision resistance guarantee

#### 2. MD5 Approach
- **Process**: MD5(original_url) → base62_encode → hash
- **Issue**: Duplication and collision problems
- **Solution**: Re-compute until unique (increases overhead)

#### 3. Counter Approach
- **Process**: Counter(0-3.5 trillion) → base62_encode → hash
- **Problem**: Single point of failure
- **Solution**: Distributed system with Zookeeper
- **Ranges**: Each server gets unique counter range

#### 4. Key Generation Service (KGS) - Recommended
- **Standalone service** generating unique keys ahead of time
- **Pre-generated keys** stored in separate database
- **Concurrent access handling**: Two-table approach with locking
- **Memory optimization**: Keep some keys in memory

#### KGS Database Estimations
- **6-character keys**: ~56.8 billion unique keys
- **Storage needed**: 6 chars × 56.8 billion ≈ 390 GB
- **Lifetime storage**: One-time setup, doesn't grow like main DB

### High-Level System Design

#### Core Components
1. **API Servers**: Handle user requests
2. **Key Generation Service (KGS)**: Generate unique keys
3. **Database**: Store URL mappings
4. **Cache**: Redis/Memcached for performance
5. **Load Balancer**: Distribute traffic

#### URL Creation Flow
1. User creates new URL via API
2. API server requests unique key from KGS
3. KGS provides key and marks as used
4. API server writes to database and cache
5. Return HTTP 201 (Created) response

#### URL Access Flow
1. Client navigates to short URL
2. Request hits cache first
3. If cache miss, retrieve from database
4. Issue HTTP 301 (Redirect) to original URL
5. If not found, return HTTP 404

### Detailed Design Considerations

#### Data Partitioning
**Horizontal partitioning (sharding) approaches:**
- Hash-Based Partitioning
- List-Based Partitioning
- Range-Based Partitioning
- Composite Partitioning
- **Solution**: Consistent hashing for even distribution

#### Database Cleanup Strategies

**Active Cleanup:**
- Separate cleanup service (cron job)
- Periodically remove expired links
- Lightweight background process

**Passive Cleanup:**
- Remove expired entries on access
- Lazy cleanup approach
- Reduces background processing

#### Caching Strategy

**Cache Eviction Policy:**
- **LRU (Least Recently Used)**: Discard least recently used keys first
- **Implementation**: Redis or Memcached

**Cache Miss Handling:**
- Direct database hit on miss
- Update cache with new entries
- Maintain cache consistency

#### Metrics and Analytics
- Store metadata: visitor country, platform, view count
- Update alongside URL entries
- Support extended requirements

#### Security Considerations
- **Private URLs**: Authorization system
- **Permission table**: Store user access rights
- **API Gateway**: Built-in authorization, rate limiting, load balancing
- **Error handling**: HTTP 401 for unauthorized access

### Bottleneck Resolution

#### Single Points of Failure
**Problems:**
- API service crashes
- Key Generation Service failure
- Database failures
- Cache unavailability

**Solutions:**
1. **Multiple instances** of all services
2. **Load balancers** between all components
3. **Database read replicas** (read-heavy system)
4. **Standby replicas** for key database
5. **Distributed cache** with multiple instances

#### Advanced Design Improvements
- **Horizontal scaling** for all components
- **Geographic distribution** for global access
- **CDN integration** for static content
- **Monitoring and alerting** systems
- **Automated failover** mechanisms

### Key Takeaways

1. **Always start with requirements clarification**
2. **Make reasonable assumptions and state them**
3. **Consider scale from the beginning**
4. **Design for failure** (no single points of failure)
5. **Cache strategically** for performance
6. **Security is not an afterthought**
7. **Monitor and measure** everything
8. **Be technology-agnostic** when possible
9. **Explain trade-offs** clearly
10. **Iterate and improve** the design

### Common Interview Mistakes

1. **Jumping into solutions** without clarifying requirements
2. **Ignoring scale considerations**
3. **Not considering failure scenarios**
4. **Being too opinionated** about specific technologies
5. **Not explaining trade-offs**
6. **Forgetting about security and monitoring**
7. **Not asking clarifying questions**
8. **Rushing through the design process**

### Preparation Tips

1. **Practice with real systems**: Design existing services
2. **Read engineering blogs**: Understand real-world implementations
3. **Study system design patterns**: Load balancing, caching, sharding
4. **Understand trade-offs**: CAP theorem, consistency vs availability
5. **Practice estimation**: Back-of-envelope calculations
6. **Learn from failures**: Study system outages and their causes
7. **Stay updated**: New technologies and approaches
8. **Mock interviews**: Practice with peers or mentors
