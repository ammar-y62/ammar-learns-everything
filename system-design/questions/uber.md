# Uber System Design

## Problem Statement
Design a ride-hailing platform similar to Uber that allows customers to book rides with nearby drivers, track real-time locations, process payments, and manage ride experiences for over 100 million users worldwide.

**Mini Example**: Design a ride-hailing platform like Uber

---

## 1. Requirements Clarification

### Functional Requirements
*[What the system must do]*
- **Customer Features**:
  - View nearby drivers with ETA and pricing
  - Book rides to destinations
  - Track driver location in real-time
  - Rate and provide feedback after trips
  - Cancel rides before pickup
- **Driver Features**:
  - Accept or deny ride requests
  - View pickup and destination locations
  - Start and end trips
  - Update real-time location
  - View earnings and trip history
- **Edge Cases**:
  - Handle surge pricing during high demand
  - Manage driver availability and ratings
  - Deal with ride cancellations
  - Handle payment failures

**Mini Example**:
- Customer books ride from home to airport
- Driver accepts ride and navigates to pickup
- Real-time location tracking during trip
- Payment processing and rating after completion

### Non-Functional Requirements
*[Quality constraints]*
- **Performance**:
  - < 2 seconds for ride booking
  - Real-time location updates (< 5 seconds)
  - Support 12K requests per second
- **Scalability**:
  - Handle 100M daily active users
  - Support 10M rides per day
  - Scale to 1.4 PB storage over 10 years
- **Availability**: 99.9% uptime
- **Reliability**: No ride requests lost, accurate location tracking

**Mini Example**:
- 99.9% uptime requirement
- < 2 seconds ride booking time
- Handle 12K requests/second peak load

### Extended Requirements
*[Nice-to-have features]*
- **Analytics**:
  - Trip metrics and driver performance
  - Revenue and demand analytics
  - User behavior tracking
- **Security**:
  - Driver and customer verification
  - Payment security and fraud detection
  - Location data privacy
- **Additional Features**:
  - Surge pricing during high demand
  - Multiple payment methods
  - Driver earnings management

**Mini Example**:
- Track trip completion rates and driver ratings
- Implement surge pricing during peak hours
- Process payments via multiple gateways

---

## 2. Estimation and Constraints

### Scale Estimation
*[Back-of-envelope calculations]*

**Traffic Assumptions**:
- **Total Users**: 100 million daily active users
- **Drivers**: 1 million active drivers
- **Rides per day**: 10 million
- **Actions per user per day**: 10
- **Total requests per day**: 1 billion

**Mini Example**:
- 100M users × 10 actions = 1B requests/day
- 10M rides completed daily
- 12K requests/second peak

**Storage Requirements**:
- **Request data**: 400 bytes per request
- **Daily storage**: 1B × 400 bytes = 400 GB/day
- **10-year storage**: 400 GB × 365 × 10 = 1.4 PB

**Mini Example**:
- 400 GB/day for request data
- 1.4 PB total over 10 years
- Location data and trip history storage

**Bandwidth Requirements**:
- **Daily ingress**: 400 GB
- **Bandwidth needed**: 400 GB ÷ (24 × 3600) ≈ 5 MB/second

**Mini Example**:
- 5 MB/s bandwidth requirement
- Handles 400 GB daily data ingress

### Summary Table
| Metric | Estimate | Notes |
|--------|----------|-------|
| Total Users | 100M | Daily active users |
| Drivers | 1M | Active drivers |
| Rides | 10M/day | Total rides completed |
| Requests | 1B/day | Total API requests |
| RPS | 12K/s | Peak requests per second |
| Storage | 400 GB/day | Daily storage requirement |
| Bandwidth | 5 MB/s | Required bandwidth |
| 10-Year Storage | 1.4 PB | Total storage needed |

---

## 3. Data Model Design

### Database Schema
*[Define entities and relationships]*

**Core Tables**:
- **Customers**:
  - Fields: id, name, email, phone, rating, created_at, last_login
  - Indexes: email (unique), phone (unique), rating, created_at
- **Drivers**:
  - Fields: id, name, email, phone, license_number, vehicle_id, rating, status, created_at
  - Indexes: email (unique), phone (unique), license_number (unique), status, rating
- **Vehicles**:
  - Fields: id, registration_number, model, type, year, driver_id
  - Indexes: registration_number (unique), driver_id, type
- **Trips**:
  - Fields: id, customer_id, driver_id, source_lat, source_lng, dest_lat, dest_lng, status, fare, created_at, started_at, completed_at
  - Indexes: customer_id, driver_id, status, created_at
- **Locations**:
  - Fields: id, user_id, user_type, latitude, longitude, timestamp, geohash
  - Indexes: user_id, user_type, geohash, timestamp
- **Ratings**:
  - Fields: id, trip_id, customer_id, driver_id, rating, feedback, created_at
  - Indexes: trip_id, customer_id, driver_id, rating
- **Payments**:
  - Fields: id, trip_id, amount, payment_method, status, transaction_id, created_at
  - Indexes: trip_id, payment_method, status, created_at

**Mini Example**:
- **Customers**: id, name, email, phone, rating
- **Drivers**: id, name, email, license_number, vehicle_id, status
- **Trips**: id, customer_id, driver_id, source_lat, source_lng, dest_lat, dest_lng, status, fare
- **Locations**: user_id, user_type, latitude, longitude, geohash

### Database Choice
*[SQL vs NoSQL decision]*
- **Microservices approach**: Split data across different services
- **User Service**: PostgreSQL for customer and driver data
- **Trip Service**: Apache Cassandra for trip data and scalability
- **Location Service**: Redis for real-time location data
- **Payment Service**: PostgreSQL for payment transactions (ACID compliance)
- **Analytics Service**: ClickHouse for analytics and metrics
- **Reasoning**: Different data types and access patterns require specialized storage

**Mini Example**:
- **PostgreSQL**: User data and payments (ACID compliance)
- **Cassandra**: Trip data (high write throughput, horizontal scaling)
- **Redis**: Real-time location data (fast access, geospatial queries)
- **ClickHouse**: Analytics (columnar storage, fast queries)

---

## 4. API Design

### Core APIs
*[Define system interfaces]*

```typescript
// Request a ride
requestRide(customerID: UUID, source: Location, destination: Location, cabType: string, paymentMethod: string): Ride
// Example: requestRide("user123", {lat: 37.7749, lng: -122.4194}, {lat: 37.7849, lng: -122.4094}, "UberX", "credit_card")

// Cancel ride
cancelRide(customerID: UUID, rideID: UUID, reason?: string): boolean
// Example: cancelRide("user123", "ride456", "Changed plans")

// Accept/deny ride (driver)
acceptRide(driverID: UUID, rideID: UUID): boolean
denyRide(driverID: UUID, rideID: UUID): boolean
// Example: acceptRide("driver789", "ride456")

// Start/end trip (driver)
startTrip(driverID: UUID, tripID: UUID): boolean
endTrip(driverID: UUID, tripID: UUID): boolean
// Example: startTrip("driver789", "trip123")

// Update location
updateLocation(userID: UUID, userType: "customer" | "driver", latitude: number, longitude: number): boolean
// Example: updateLocation("driver789", "driver", 37.7749, -122.4194)

// Rate trip
rateTrip(customerID: UUID, tripID: UUID, rating: number, feedback?: string): boolean
// Example: rateTrip("user123", "trip456", 5, "Great driver!")

// Get nearby drivers
getNearbyDrivers(customerID: UUID, latitude: number, longitude: number, radius: number): Driver[]
// Example: getNearbyDrivers("user123", 37.7749, -122.4194, 5000): [driver1, driver2, ...]

// Get trip status
getTripStatus(tripID: UUID): TripStatus
// Example: getTripStatus("trip123"): {status: "in_progress", driver_location: {...}}
```

### API Considerations
- **Authentication**: OAuth 2.0 with JWT tokens
- **Rate Limiting**: 1000 API calls/hour per user
- **Error Handling**: Standard HTTP status codes with detailed error messages
- **Real-time Updates**: WebSocket connections for location tracking
- **Geolocation**: Location-based services and geofencing

**Mini Example**:
- OAuth 2.0 authentication for all API calls
- 1000 API calls/hour rate limit per user
- WebSocket connections for real-time location updates

---

## 5. High-Level Architecture

### System Components
*[Core building blocks]*

1. **Client Layer**: iOS/Android mobile apps, Web app
2. **API Gateway**: Request routing, authentication, rate limiting
3. **Load Balancer**: Traffic distribution across services
4. **Customer Service**: Customer management, authentication, profiles
5. **Driver Service**: Driver management, authentication, vehicle info
6. **Ride Service**: Ride matching, geospatial queries, pricing
7. **Trip Service**: Trip lifecycle management, status tracking
8. **Location Service**: Real-time location tracking, geospatial data
9. **Payment Service**: Payment processing, transaction management
10. **Notification Service**: Push notifications for ride updates
11. **Analytics Service**: Metrics collection and analysis
12. **Database Layer**: PostgreSQL, Cassandra, Redis, ClickHouse
13. **Message Queue**: Kafka for event streaming
14. **Geospatial Engine**: Quadtree/Geohash for location queries

**Mini Example**:
- **API Gateway**: Route requests to appropriate services
- **Ride Service**: Handle ride matching and geospatial queries
- **Location Service**: Manage real-time location tracking
- **Payment Service**: Process ride payments

### Data Flow
*[How data moves through the system]*

**Ride Booking Flow**:
1. Customer → API Gateway → Ride Service
2. Ride Service → Location Service (find nearby drivers)
3. Ride Service → Driver Service (check driver availability)
4. Ride Service → Notification Service (notify drivers)
5. Driver accepts → Trip Service (create trip)
6. Response to Customer

**Location Tracking Flow**:
1. Driver/Customer updates location
2. Client → Location Service (update coordinates)
3. Location Service → Geospatial Engine (update quadtree)
4. Location Service → Trip Service (update trip status)
5. Trip Service → Notification Service (notify other party)

**Mini Example**:
- **Ride Booking**: Customer → API → Ride Service → Location Service → Driver Notification
- **Location Tracking**: Driver → Location Service → Geospatial Engine → Customer Update

---

## 6. Detailed Design

### Location Tracking & Geospatial Queries
*[Real-time location management]*

**Geohashing**:
- Encode lat/lng coordinates into short alphanumeric strings
- Hierarchical spatial indexing for efficient queries
- Base-32 encoding for compact representation
- Example: San Francisco (37.7564, -122.4016) → "9q8yy9mf"

**Quadtree Implementation**:
- Recursive subdivision of 2D space into quadrants
- Efficient range queries for nearby drivers
- In-memory storage in Redis for fast access
- Hilbert curve mapping for spatial locality

**Real-time Updates**:
- WebSocket connections for live location streaming
- Background GPS pinging in mobile apps
- 5-second update intervals for active trips
- Geofencing for pickup/drop-off detection

**Mini Example**:
- **Geohash**: Convert coordinates to "9q8yy9mf" for efficient storage
- **Quadtree**: Find all drivers within 5km radius efficiently
- **WebSocket**: Real-time location updates every 5 seconds

### Ride Matching Algorithm
*[Driver-customer matching logic]*

**Proximity Search**:
1. Customer location → Geohash lookup
2. Query quadtree for nearby drivers
3. Filter by driver availability and rating
4. Rank drivers by distance, rating, and vehicle type
5. Send ride request to top drivers

**Driver Ranking Factors**:
- **Distance**: Closest drivers prioritized
- **Rating**: Higher-rated drivers preferred
- **Vehicle Type**: Match customer preference
- **Availability**: Currently available drivers
- **Past Performance**: Completion rate and reliability

**Race Condition Handling**:
- Mutex locks for ride request processing
- Transactional operations for ride acceptance
- Atomic updates for driver availability
- Retry mechanisms for failed matches

**Mini Example**:
- **Proximity**: Find drivers within 5km of customer
- **Ranking**: Sort by distance (60%), rating (30%), availability (10%)
- **Mutex**: Prevent multiple drivers accepting same ride

### Surge Pricing
*[Dynamic pricing during high demand]*

**Demand Calculation**:
- Monitor ride requests per area per time
- Track driver availability in real-time
- Calculate demand/supply ratio
- Apply surge multiplier based on ratio

**Pricing Factors**:
- **Base Fare**: Distance × time × base rate
- **Surge Multiplier**: 1.0x to 5.0x based on demand
- **Time Factors**: Peak hours, events, weather
- **Location Factors**: Airport, downtown, events

**Implementation**:
- Real-time demand monitoring
- Dynamic pricing updates every 5 minutes
- Customer notification of surge pricing
- Driver incentive adjustments

**Mini Example**:
- **Demand Ratio**: 10 requests, 2 available drivers = 5.0x surge
- **Pricing**: Base $20 + 3.0x surge = $60 total fare
- **Updates**: Recalculate every 5 minutes

### Caching Strategy
*[Performance optimization]*

**Cache Levels**:
- **Application Cache**: In-memory caching for user sessions
- **Distributed Cache**: Redis for location data and ride status
- **CDN**: Static content delivery for mobile apps
- **Browser Cache**: Client-side caching for maps and UI

**Cache Policies**:
- **Eviction**: LRU for location data, TTL for ride status
- **Consistency**: Cache-aside for location, write-through for payments

**Mini Example**:
- **Redis**: Cache driver locations and ride status
- **LRU eviction**: Remove least recently accessed locations
- **TTL**: 30 seconds for location data, 5 minutes for ride status

### Data Partitioning
*[Scalability strategy]*

**Partitioning Strategies**:
- **Geographic**: Partition by city/region for location data
- **Hash-based**: Partition trips by trip_id for even distribution
- **Time-based**: Partition by date for historical data

**Mini Example**:
- **Geographic**: Partition by city for location queries
- **Trip partitioning**: Hash by trip_id for even distribution
- **Analytics**: Shard by date for time-series data

### Security Considerations
*[Protection mechanisms]*

**Authentication & Authorization**:
- **OAuth 2.0**: Third-party authentication
- **JWT Tokens**: Stateless authentication for API access
- **Driver Verification**: License and background checks

**Data Protection**:
- **Location Privacy**: Anonymize location data when possible
- **Payment Security**: PCI compliance for payment processing
- **Fraud Detection**: ML-powered fraud detection system

**Mini Example**:
- **OAuth 2.0**: Secure third-party authentication
- **Location Privacy**: Only share location during active trips
- **Fraud Detection**: Flag suspicious payment patterns

---

## 7. Bottleneck Analysis & Resolution

### Single Points of Failure
*[Identify and resolve]*

**Potential Issues**:
- **Ride Service**: Single service handling all ride matching
- **Location Service**: Single service for geospatial queries
- **Database**: Single database instance
- **Payment Service**: Single payment processor
- **API Gateway**: Single entry point

**Solutions**:
- **Multiple Ride Service instances**: Load balanced across regions
- **Location Service clustering**: Multiple quadtree instances
- **Database clustering**: Primary + read replicas with failover
- **Multiple payment processors**: Stripe + PayPal fallback
- **Multiple API Gateways**: Active-passive configuration

**Mini Example**:
- **Ride Service**: 5 instances with load balancer
- **Location Service**: 3 quadtree instances with Redis clustering
- **Database**: Primary + 3 read replicas
- **API Gateway**: Active-passive with health checks

### Scalability Improvements
*[Handle growth]*

**Horizontal Scaling**:
- **Ride Service**: Auto-scaling based on request volume
- **Location Service**: Multiple quadtree instances per region
- **Trip Service**: Multiple instances for trip management
- **Payment Service**: Multiple payment processor integrations

**Vertical Scaling**:
- **Database optimization**: Query optimization, proper indexing
- **Connection pooling**: Efficient database connections
- **Caching optimization**: Multi-level caching strategy

**Mini Example**:
- **Auto-scaling**: Add ride service instances based on request count
- **Geographic scaling**: Separate quadtree instances per major city
- **Payment redundancy**: Multiple payment gateways for reliability

---

## 8. Monitoring & Analytics

### Key Metrics
*[What to measure]*

**Performance Metrics**:
- **Ride Booking Time**: < 2 seconds for 95% of requests
- **Location Update Latency**: < 5 seconds for 95% of updates
- **Payment Processing**: < 10 seconds for 95% of payments
- **Availability**: 99.9% uptime

**Business Metrics**:
- **Daily Active Users**: 100M target
- **Rides per Day**: 10M target
- **Driver Utilization**: Average rides per driver per day
- **Customer Satisfaction**: Average rating per trip

**Mini Example**:
- **Response Time**: < 2 seconds for 95% of ride bookings
- **Satisfaction**: 4.5+ average rating target
- **Uptime**: 99.9% availability target

### Monitoring Tools
*[How to monitor]*

**Infrastructure Monitoring**:
- **APM**: New Relic for application performance
- **Logging**: ELK Stack for centralized logging
- **Alerting**: PagerDuty for incident management

**Mini Example**:
- **New Relic**: Monitor ride booking performance
- **ELK Stack**: Aggregate logs from all services
- **PagerDuty**: Alert on service failures

---

## 9. Trade-offs & Decisions

### Technology Choices
*[Why specific technologies]*

**Database**:
- **PostgreSQL**: User data and payments (ACID compliance)
- **Cassandra**: Trip data (high write throughput, horizontal scaling)
- **Redis**: Location data (fast access, geospatial queries)
- **ClickHouse**: Analytics (columnar storage, fast queries)

**Geospatial**:
- **Quadtree**: Efficient 2D spatial queries
- **Geohashing**: Compact location encoding
- **WebSockets**: Real-time bidirectional communication

**Mini Example**:
- **Cassandra**: Chosen for high trip data write throughput
- **Redis**: Chosen for fast geospatial queries and real-time data
- **Quadtree**: Chosen for efficient nearby driver searches

### Design Decisions
*[Architecture choices]*

**Microservices vs Monolith**:
- **Microservices**: Independent scaling, technology diversity, fault isolation
- **Monolith**: Simpler deployment, easier debugging, lower latency

**Synchronous vs Asynchronous**:
- **Sync**: Ride booking (immediate response)
- **Async**: Location updates, notifications (eventual consistency)

**Mini Example**:
- **Microservices**: Chosen for independent scaling of ride, location, payment services
- **Async**: Location updates sent asynchronously via message queues

---

## 10. Future Considerations

### Scalability Roadmap
*[Growth plans]*

**Short-term** (3-6 months):
- **Performance**: Optimize ride matching algorithm
- **Monitoring**: Improve real-time monitoring and alerting
- **Geospatial**: Enhance quadtree performance

**Long-term** (6-12 months):
- **Architecture**: Consider event-driven architecture
- **Global**: Multi-region deployment for global users
- **Advanced**: Self-driving integration, ride pooling optimization

**Mini Example**:
- **Short-term**: Reduce ride booking time to < 1 second
- **Long-term**: Add self-driving vehicle integration

### Potential Challenges
*[Anticipate problems]*

**Technical Challenges**:
- **Geospatial Scaling**: Managing location data at global scale
- **Real-time Performance**: Sub-second response times for ride matching
- **Payment Processing**: Handling millions of transactions daily
- **Driver Availability**: Managing driver supply and demand

**Business Challenges**:
- **Regulatory Compliance**: Local transportation regulations
- **Driver Retention**: Maintaining driver supply
- **Competition**: Feature parity with other ride-hailing platforms

**Mini Example**:
- **Geospatial optimization**: Use quadtree for efficient location queries
- **Driver incentives**: Dynamic pricing and bonus programs

---

## Summary

### Key Design Decisions
1. **Microservices Architecture**: Independent scaling of ride, location, payment services
2. **Geospatial Engine**: Quadtree and geohashing for efficient location queries
3. **Multi-database Approach**: PostgreSQL for users, Cassandra for trips, Redis for locations
4. **Real-time Location Tracking**: WebSocket connections for live updates
5. **Surge Pricing**: Dynamic pricing based on demand/supply ratio

### Estimated Resources
- **Ride Service**: 10 instances (auto-scaling)
- **Location Service**: 5 quadtree instances per region
- **Database**: 3 Cassandra clusters, 3 PostgreSQL instances, 5 Redis clusters
- **Storage**: 1.4 PB over 10 years
- **Bandwidth**: 5 MB/s peak
- **Cost**: $2-5M/month for infrastructure

### Success Metrics
- **Performance**: < 2 seconds ride booking, 99.9% uptime
- **Scalability**: Support 100M DAU, 10M rides/day
- **Reliability**: Accurate location tracking, no ride losses

---

## Notes

### Assumptions
- 100M daily active users, 1M active drivers
- 10 rides per day per driver
- 400 bytes per request average
- 10-year data retention period

### Limitations
- No ride pooling in initial design
- Limited autonomous vehicle integration
- Basic surge pricing algorithm
- No advanced fraud detection

### Alternatives Considered
- **Monolithic architecture**: Rejected for scaling limitations
- **Single database**: Rejected for performance bottlenecks
- **Pull-based location updates**: Rejected for latency issues
- **Client-side ride matching**: Rejected for security and performance

### References
- Uber Engineering Blog
- Apache Cassandra documentation
- Redis geospatial documentation
- Quadtree algorithm implementation
- Stripe payment processing documentation