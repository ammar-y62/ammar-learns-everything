# System Design Notes

## What is System Design?
- **Definition**: The process of defining the architecture, interfaces, and data for a system to meet specific requirements.
- **Purpose**: Builds coherent and efficient systems aligned with business or organizational needs.
- **Approach**: Requires systematic thinking, covering infrastructure to data storage.

## Importance of System Design
- Helps define solutions that meet business requirements.
- Early-stage decisions are critical and hard to change later.
- Facilitates better management of architectural changes as the system evolves.

## IP Addresses

### Definition
- A unique identifier for devices on the internet or local network.
- Governed by Internet Protocol (IP) rules for data format and transfer.

### Versions
1. **IPv4**:
   - 32-bit numeric dot-decimal notation.
   - Example: 102.22.192.181.
   - Limited to ~4 billion addresses.
2. **IPv6**:
   - 128-bit alphanumeric hexadecimal notation.
   - Example: 2001:0db8:85a3:0000:0000:8a2e:0370:7334.
   - Can provide ~340e+36 addresses.

### Types of IP Addresses
1. **Public**:
   - One primary address for a whole network.
   - Example: Router's IP address assigned by ISP.
2. **Private**:
   - Unique IP numbers assigned to devices within a network.
   - Example: Home devices assigned by a router.
3. **Static**:
   - Manually created, unchanging address.
   - Used for reliable services like server hosting.
4. **Dynamic**:
   - Assigned by DHCP, changes periodically.
   - Used for consumer equipment and personal use.

## OSI Model

### Definition
- A conceptual framework defining network communication between systems.
- Splits the communication system into seven abstraction layers.

### Importance
- Provides common networking terminology.
- Simplifies complex processes and facilitates troubleshooting.
- Encourages compatibility between hardware and systems.
- Promotes a security-first mindset.

### Layers (Top to Bottom)
1. **Application**:
   - Direct interaction with user data.
   - Protocols: HTTP, SMTP.
2. **Presentation**:
   - Translates, encrypts/decrypts, and compresses data.
   - Known as the translation layer.
3. **Session**:
   - Manages communication sessions (opening, maintaining, closing).
   - Synchronizes data with checkpoints.
4. **Transport**:
   - Responsible for end-to-end communication.
   - Breaks data into segments and reassembles on the receiving side.
5. **Network**:
   - Handles data transfer between different networks.
   - Breaks segments into packets and performs routing.
6. **Data Link**:
   - Facilitates data transfer within the same network.
   - Breaks packets into frames.
7. **Physical**:
   - Includes physical equipment (cables, switches).
   - Converts data into a bit stream (1s and 0s).

## TCP and UDP

### TCP (Transmission Control Protocol)
- **Type**: Connection-oriented protocol.
- **Features**:
  - Establishes a connection before transmitting data.
  - Guarantees ordered and error-checked delivery of data.
  - Reliable but involves larger overhead, using more network bandwidth.
- **Use Cases**:
  - HTTPS, HTTP, SMTP, POP, FTP.
  - Suitable for still images, data files, and web pages.

### UDP (User Datagram Protocol)
- **Type**: Connectionless protocol.
- **Features**:
  - No connection setup or teardown, minimal overhead.
  - No error-checking or guaranteed delivery.
  - Faster than TCP but less reliable.
- **Use Cases**:
  - Real-time communications like video streaming, DNS, VoIP.

### TCP vs. UDP

| Feature | TCP | UDP |
|---------|-----|-----|
| Connection | Requires established connection | Connectionless protocol |
| Guaranteed delivery | Yes | No |
| Re-transmission | Possible | Not possible |
| Speed | Slower | Faster |
| Broadcasting | Not supported | Supported |
| Use Cases | HTTPS, FTP, SMTP | Video streaming, DNS, VoIP |

## Domain Name System (DNS)

### Definition
- Translates human-readable domain names (e.g., google.com) into IP addresses (e.g., 122.250.192.232).
- Hierarchical and decentralized naming system.

### How DNS Works
1. Client enters a domain (e.g., example.com) in a browser.
2. Query sent to DNS resolver.
3. Resolver queries DNS root nameserver.
4. Root server refers to the TLD nameserver (e.g., .com).
5. TLD server responds with the IP address of the domain's nameserver.
6. Resolver queries the authoritative nameserver.
7. Authoritative server returns the IP address to the resolver.
8. Resolver sends the IP address to the browser, which accesses the website.

### DNS Infrastructure

#### Server Types
1. **DNS Resolver**:
   - First step in DNS lookup.
   - Queries root, TLD, and authoritative nameservers if needed.
2. **DNS Root Server**:
   - Directs resolvers to TLD nameservers.
   - Managed by ICANN.
3. **TLD Nameserver**:
   - Handles domain extensions (e.g., .com, .org).
   - Managed by IANA under ICANN.
4. **Authoritative DNS Server**:
   - Final step in DNS resolution.
   - Provides the IP address for the queried domain.

#### Query Types
1. **Recursive**:
   - DNS client expects resolver to return the requested record or an error.
2. **Iterative**:
   - Resolver refers the client to other servers for further queries.
3. **Non-Recursive**:
   - Resolver responds directly with cached or authoritative data.

### DNS Record Types

| Type | Description |
|------|-------------|
| A | Maps domain to an IPv4 address. |
| AAAA | Maps domain to an IPv6 address. |
| CNAME | Alias for another domain. Does not provide IP. |
| MX | Directs emails to the domain's mail server. |
| TXT | Stores text notes for the domain (e.g., email security). |
| NS | Specifies authoritative nameserver for the domain. |
| SOA | Stores administrative info about the domain. |
| SRV | Specifies a port for specific services. |
| PTR | Reverse-lookup pointer for resolving IP to domain name. |
| CERT | Stores public key certificates. |

### Additional DNS Concepts

#### Subdomains
- Logical divisions of a domain (e.g., blog.example.com, support.example.com).

#### DNS Zones
- A distinct part of the domain namespace managed by an organization.

#### DNS Caching
- Temporary storage of DNS lookups for faster resolution.
- Controlled by TTL (time-to-live) value.

#### Reverse DNS Lookup
- Resolves IP addresses to domain names using PTR records.
- Commonly used by email servers for verification.

### Examples of Managed DNS Solutions
- AWS Route53
- Cloudflare DNS
- Google Cloud DNS
- Azure DNS
- NS1

## Load Balancing Notes

### What is Load Balancing?
- **Definition**: Distributes incoming network traffic across multiple servers or resources.
- **Purpose**: Ensures high availability, reliability, and scalability.
- **Benefits**: Prevents server overloading, allows scaling up or down based on demand, and redirects traffic during server failures.

### Why Load Balancing?
- Modern high-traffic systems handle millions of requests.
- Adding servers is cost-effective for scaling.
- Load balancers:
  - Maximize speed and capacity utilization.
  - Avoid overworking any single server.
  - Handle server failures by redirecting traffic.

### Workload Distribution Types
1. **Host-based**: Routes based on the requested hostname.
2. **Path-based**: Uses the full URL for routing.
3. **Content-based**: Inspects request content (e.g., parameter values) to distribute requests.

### Layers of Load Balancing
1. **Network Layer (Layer 4)**:
   - Routes based on network information (e.g., IP addresses).
   - High speed but lacks content-based routing.
   - Example: Hardware load balancers.
2. **Application Layer (Layer 7)**:
   - Reads full requests for routing decisions (e.g., content-based routing).
   - Provides more advanced traffic management.

### Types of Load Balancers
1. **Software Load Balancers**:
   - Flexible, cost-effective, and configurable.
   - Used in software development and cloud environments.
   - Examples: Nginx, HAProxy, managed cloud services.
2. **Hardware Load Balancers**:
   - Physical devices with proprietary firmware.
   - Handle high traffic but are expensive and less flexible.
3. **DNS Load Balancers**:
   - Configures DNS to distribute traffic across multiple servers.
   - Limitations: Does not check server health or outages.

### Routing Algorithms
1. **Round-robin**: Cycles through servers sequentially.
2. **Weighted Round-robin**: Assigns weights based on server capacity.
3. **Least Connections**: Sends traffic to the server with the fewest active connections.
4. **Least Response Time**: Combines response time and active connections to route traffic.
5. **Least Bandwidth**: Routes based on the server with the least Mbps traffic.
6. **Hashing**: Uses a predefined key (e.g., client IP) to route traffic consistently.

### Advantages of Load Balancing
- **Scalability**: Supports traffic growth.
- **Redundancy**: Prevents downtime during failures.
- **Flexibility**: Easily add or remove resources.
- **Efficiency**: Optimizes resource utilization.

### Redundant Load Balancers
- A single load balancer can fail, becoming a single point of failure.
- Solution: Use multiple load balancers in a cluster.
  - Active-passive mode: Backup load balancer takes over if the active one fails.
  - Fault tolerance ensures system reliability.

### Features of Load Balancers
- **Autoscaling**: Adjust resources dynamically based on demand.
- **Sticky Sessions**: Keeps users connected to the same server for session consistency.
- **Health Checks**: Removes failing resources from the pool.
- **Persistent Connections**: Supports long-lived connections like WebSockets.
- **Encryption**: Manages TLS/SSL connections and certificates.
- **Compression**: Compresses responses to improve performance.
- **Caching**: Stores responses for faster delivery.
- **Logging**: Tracks request/response metadata for audits and analytics.
- **Request Tracing**: Assigns unique IDs for monitoring and troubleshooting.
- **Redirects**: Routes requests based on specific paths or conditions.
- **Fixed Responses**: Sends static responses (e.g., error messages).

### Examples of Load Balancing Solutions
- **Cloud Solutions**:
  - Amazon Elastic Load Balancing
  - Azure Load Balancing
  - Google Cloud Platform (GCP) Load Balancing
  - DigitalOcean Load Balancer
- **Software Solutions**:
  - Nginx
  - HAProxy

## Clustering Notes

### What is Clustering?
- **Definition**: A group of two or more computers (nodes) working in parallel to achieve a common goal.
- **Purpose**: Distributes high-volume tasks among nodes to leverage combined memory and processing power, improving overall performance.
- **Features**:
  - Nodes communicate via a network.
  - Typically includes a leader node to manage workload delegation and result aggregation.
  - Functions as a single system to the user, minimizing latency and avoiding communication bottlenecks.

### Types of Clusters
1. **Highly Available (Fail-Over)**: Ensures system availability by failing over to a backup node if the primary node fails.
2. **Load Balancing**: Distributes tasks across multiple active nodes to prevent overload and optimize resource utilization.
3. **High-Performance Computing**: Focuses on computational tasks that require significant processing power and parallelization.

### Cluster Configurations
1. **Active-Active**:
   - All nodes actively handle workloads simultaneously.
   - Ideal for load balancing and improving throughput and response times.
2. **Active-Passive**:
   - Only one node is active, while the others remain passive or standby.
   - Ensures high availability in case of failure.

### Advantages of Clustering
- **High Availability**: Minimizes downtime.
- **Scalability**: Easily add or remove nodes to handle changing demand.
- **Performance**: Optimizes resource utilization and workload distribution.
- **Cost-Effectiveness**: Uses commodity hardware for better processing power.

### Load Balancing vs. Clustering

| Feature | Load Balancing | Clustering |
|---------|----------------|------------|
| Redundancy | No | Yes |
| Awareness | Servers unaware of each other | Nodes collaborate for common goals |
| Use Cases | Independent servers sharing a purpose | Systems requiring redundancy and scalability |

### Challenges of Clustering
- **Complexity**: Requires consistent installation and updates across nodes.
- **Heterogeneity**: Variations in node configurations can complicate management.
- **Storage Management**: Prevent overwrites and synchronize distributed data stores.

### Examples of Clustering
- **Containers**: Kubernetes, Amazon ECS.
- **Databases**: Cassandra, MongoDB.
- **Caching**: Redis.

## Caching Notes

### What is Caching?
- **Definition**: A fast, temporary storage layer that improves data retrieval performance by reducing access to slower storage systems.
- **Principle**: Based on the locality of reference, where recently accessed data is likely to be accessed again.

### Cache Levels
- **L1**: Fastest but smallest capacity.
- **L2/L3**: Slower but larger than L1.
- **Process**: Searches data sequentially across levels (L1 → L2 → L3 → etc.) until found.

### Cache Hit vs. Cache Miss
- **Cache Hit**: Data is successfully retrieved from the cache.
  - Types:
    - Hot Cache: Data retrieved from L1 (fastest).
    - Warm Cache: Data retrieved from L2/L3.
    - Cold Cache: Data retrieved from lower cache levels.
- **Cache Miss**: Data is not found in the cache and must be fetched from the primary storage.

### Cache Invalidation
- **Definition**: The process of marking cache entries as invalid to ensure data consistency.
- **Types**:
  1. **Write-Through Cache**: Writes data to both cache and storage simultaneously.
     - Pro: Ensures consistency.
     - Con: Higher latency for write operations.
  2. **Write-Around Cache**: Writes data directly to storage, bypassing the cache.
     - Pro: Reduces write latency.
     - Con: Increased cache misses for frequently re-read data.
  3. **Write-Back Cache**: Writes data to the cache first and syncs to storage asynchronously.
     - Pro: High write throughput.
     - Con: Risk of data loss if the cache crashes.

### Eviction Policies
- **FIFO**: Removes the oldest data first.
- **LIFO**: Removes the most recently added data.
- **LRU**: Removes the least recently used data.
- **MRU**: Removes the most recently used data.
- **LFU**: Removes the least frequently used data.
- **RR**: Removes a random item.

### Distributed Cache
- Combines memory from multiple networked machines into a unified data store.
- Provides scalability and fault tolerance for large-scale systems.

### When Not to Use Caching?
- Low repetition of requests: Random data access patterns.
- Frequent data changes: Increases cache invalidation overhead.
- Cache performance equals primary storage: No significant speed improvement.

### Advantages of Caching
- Improves performance and reduces latency.
- Reduces database load and network costs.
- Increases read throughput.

### Examples of Caching Technologies
- Redis
- Memcached
- Amazon Elasticache
- Aerospike

## Content Delivery Network (CDN)

### Definition
- A geographically distributed group of servers that work together to deliver internet content quickly.
- Primarily used for static content like HTML/CSS/JS files, images, and videos.

### Why Use a CDN?
- **Increased Availability and Redundancy**: Content is served from multiple locations.
- **Reduced Latency**: Content is delivered from a nearby edge server, reducing travel time.
- **Improved Scalability**: Offloads traffic from the origin server.
- **Bandwidth Cost Reduction**: Reduces the load on the origin server.
- **Enhanced Security**: Protects against DDoS attacks and traffic spikes.

### How Does a CDN Work?
1. **Origin Server**: Stores the original content.
2. **Edge Servers**: Cache content and deliver it to users.
3. **Caching Mechanism**:
   - Stores content at edge locations.
   - Users are served from the closest edge location.
   - Minimizes requests to the origin server, reducing latency and load.

**Example**:
- A user in the UK requests a website hosted in the USA.
- Instead of the origin server, the user is served from a London edge server for faster delivery.

### Types of CDNs
1. **Push CDN**:
   - Content is uploaded to the CDN by the website owner.
   - The CDN delivers content to users until it expires or is updated.
   - Best for low-traffic websites with infrequently changing content.
2. **Pull CDN**:
   - Content is fetched from the origin server when requested.
   - The cache is updated dynamically as users access content.
   - Ideal for high-traffic websites with frequently changing content.

### Disadvantages of CDNs
1. **Extra Costs**: High traffic increases CDN expenses.
2. **Geographic Restrictions**: Some countries block CDN domains or IPs.
3. **Server Location**: Limited edge servers in certain regions can lead to higher latency.

### Examples of CDNs
- Amazon CloudFront
- Google Cloud CDN
- Cloudflare CDN
- Fastly

## Proxy

### Definition
- A proxy server acts as an intermediary between a client and a backend server.
- Functions include filtering, logging, transforming requests, or enhancing security.

### Types of Proxies

#### 1. Forward Proxy
- Sits between clients and the internet.
- Intercepts client requests and communicates with web servers on behalf of the clients.

**Advantages**:
- Blocks access to restricted content.
- Allows access to geo-restricted content.
- Provides anonymity.
- Avoids browsing restrictions.

#### 2. Reverse Proxy
- Sits between web servers and clients.
- Intercepts requests before they reach the origin server.

**Advantages**:
- **Improved Security**: Masks the origin server's IP address.
- **Caching**: Serves cached responses to reduce load.
- **SSL Encryption**: Handles encryption, offloading it from origin servers.
- **Load Balancing**: Distributes traffic across multiple servers.
- **Scalability and Flexibility**: Adds or removes servers easily.

**Key Difference (Forward vs. Reverse Proxy)**:
- Forward Proxy: Represents the client to servers.
- Reverse Proxy: Represents the server to clients.

### Load Balancer vs. Reverse Proxy

| Feature | Reverse Proxy | Load Balancer |
|---------|---------------|---------------|
| Number of Servers | Can work with a single server | Designed for multiple servers |
| Primary Function | Security, caching, SSL, transformations | Distributes traffic among servers |
| Utility | Acts as a gateway for clients | Balances workload between resources |

### Examples of Proxy Technologies
- Nginx
- HAProxy
- Traefik
- Envoy

## Availability

### Definition
- Availability measures the percentage of time a system remains operational to perform its required functions.
- Formula: Availability = (Uptime / (Uptime + Downtime)) × 100

### The Nines of Availability
- Expressed in terms of "nines," where higher nines indicate less downtime.

| Availability (%) | Downtime (Year) | Downtime (Month) | Downtime (Week) |
|------------------|-----------------|------------------|-----------------|
| 90% (1 nine) | 36.53 days | 72 hours | 16.8 hours |
| 99% (2 nines) | 3.65 days | 7.20 hours | 1.68 hours |
| 99.9% (3 nines) | 8.77 hours | 43.8 minutes | 10.1 minutes |
| 99.99% (4 nines) | 52.6 minutes | 4.32 minutes | 1.01 minutes |
| 99.999% (5 nines) | 5.25 minutes | 25.9 seconds | 6.05 seconds |

### Availability in Sequence vs. Parallel

#### Sequence:
- Total availability decreases when components are sequentially dependent.
- Formula: Total Availability = Availability₁ × Availability₂ × ... × Availabilityₙ
- Example: Two components, each 99.9% available: 99.9% × 99.9% = 99.8%

#### Parallel:
- Total availability increases when components operate in parallel.
- Formula: Total Availability = 1 - (1 - Availability₁) × (1 - Availability₂) × ... × (1 - Availabilityₙ)
- Example: Two components, each 99.9% available: 1 - (1 - 0.999) × (1 - 0.999) = 99.9999%

### Availability vs. Reliability
- **Reliability**: Measures how consistently a system performs its function over time.
- **Availability**: A system can be available but not reliable if frequent failures are resolved quickly.

### High Availability vs. Fault Tolerance

| Feature | High Availability | Fault Tolerance |
|---------|-------------------|-----------------|
| Uptime | Minimal service interruption | No service interruption |
| Redundancy | Some redundancy | Full hardware redundancy |
| Cost | Lower cost | Higher cost |

## Scalability

### Definition
- Measures a system's ability to handle increased or decreased workload by adding or removing resources.

### Types of Scaling

#### 1. Vertical Scaling (Scaling Up):
- Adds resources (e.g., CPU, RAM) to a single machine.
- **Advantages**:
  - Simple to implement.
  - Easier to manage.
  - Maintains data consistency.
- **Disadvantages**:
  - Downtime during upgrades.
  - Limited by hardware capacity.
  - Single point of failure.

#### 2. Horizontal Scaling (Scaling Out):
- Adds more machines to distribute the workload.
- **Advantages**:
  - Improved fault tolerance.
  - Increased redundancy.
  - Flexible and efficient.
- **Disadvantages**:
  - Increased complexity.
  - Potential for data inconsistency.
  - Higher load on downstream services.

## Storage

### RAID (Redundant Array of Independent Disks)

| Level | Description | Minimum Disks | Fault Tolerance | Capacity Utilization | Performance |
|-------|-------------|---------------|-----------------|---------------------|-------------|
| RAID 0 | Striping (No redundancy) | 2 | None | 100% | High Read/Write |
| RAID 1 | Mirroring | 2 | Single-drive failure | 50% | High Read |
| RAID 5 | Striping with Parity | 3 | Single-drive failure | 67%-94% | High Read/Write |
| RAID 6 | Striping with Double Parity | 4 | Two-drive failure | 50%-80% | High Read/Write |
| RAID 10 | Striping and Mirroring | 4 | One disk per sub-array | 50% | High Read/Write |

### Types of Storage
1. **File Storage**:
   - Stores data as files in a hierarchical structure.
   - Example: Amazon EFS, Google Filestore.
2. **Block Storage**:
   - Divides data into blocks with unique identifiers.
   - Example: Amazon EBS.
3. **Object Storage**:
   - Stores data as objects in a repository.
   - Example: Amazon S3, Azure Blob Storage.
4. **NAS (Network Attached Storage)**:
   - Centralized storage accessed over a network.
5. **HDFS (Hadoop Distributed File System)**:
   - Designed for large-scale, fault-tolerant data storage.


## Databases and DBMS Notes

### What is a Database?
- A database is an organized collection of structured data, typically stored electronically.
- It allows for efficient storage, retrieval, and management of data.

### What is DBMS?
- **DBMS (Database Management System)**: Software that acts as an interface between the database and its users/applications.
  - **Functions**:
    - Manage data storage and retrieval.
    - Optimize performance.
    - Provide administrative tools for backup, recovery, and monitoring.

### Components of a Database
1. **Schema**:
   - Defines the structure of the database (e.g., table layouts, relationships, types of data allowed).
2. **Table**:
   - Organizes data into rows and columns. Think of it as a spreadsheet.
3. **Column**:
   - Represents a specific attribute (e.g., "Name" or "Age") for all rows.
4. **Row**:
   - Represents a single record in the table (e.g., one person's data).

### Types of Databases
1. **SQL Databases (Relational)**:
   - Organize data into tables with fixed schemas.
   - Use SQL (Structured Query Language) for queries.
   - Examples: MySQL, PostgreSQL, Amazon Aurora.
2. **NoSQL Databases (Non-Relational)**:
   - Flexible and dynamic schemas.
   - Ideal for distributed and unstructured data.
   - Types:
     - Document: MongoDB, CouchDB.
     - Key-Value: Redis, DynamoDB.
     - Graph: Neo4j, Amazon Neptune.
     - Time-Series: InfluxDB, Apache Druid.
     - Wide Column: Apache Cassandra, BigTable.
     - Multi-Model: ArangoDB, CosmosDB.

### Challenges with Databases
1. Handling large data volumes from multiple sources (e.g., IoT, sensors).
2. Ensuring data security to prevent breaches.
3. Real-time access for quick decision-making.
4. Scalability to handle growing demands.
5. Balancing performance and costs.

### SQL Databases
- **Key Features**:
  - Data is stored in tables.
  - Relationships between data are represented using primary keys and foreign keys.
  - Supports ACID compliance for consistency and reliability.
- **Materialized Views**:
  - Pre-computed queries stored for faster access.
- **Common Challenges**:
  - N+1 Query Problem: Multiple unnecessary queries when data can be fetched in a single query.
- **Advantages**:
  - Structured and accurate.
  - Easy to query with SQL.
  - High data consistency.
- **Disadvantages**:
  - Expensive to maintain.
  - Scaling horizontally is difficult.

### NoSQL Databases
- **Key Features**:
  - Flexible schemas.
  - Horizontally scalable.
  - Not ACID compliant (follows BASE model).
- **Types and Use Cases**:

| Type | Description | Examples |
|------|-------------|----------|
| Document | Stores data as documents (e.g., JSON or BSON). | MongoDB, CouchDB |
| Key-Value | Stores key-value pairs, like a dictionary. | Redis, DynamoDB |
| Graph | Stores nodes and edges to represent relationships. | Neo4j, Amazon Neptune |
| Time-Series | Optimized for time-stamped data. | InfluxDB, Apache Druid |
| Wide Column | Stores data in columns instead of rows. | Cassandra, BigTable |
| Multi-Model | Combines multiple database types in one system. | ArangoDB, CosmosDB |

### SQL vs NoSQL

| Aspect | SQL (Relational) | NoSQL (Non-Relational) |
|--------|------------------|------------------------|
| Schema | Fixed (pre-defined). | Dynamic (can adapt as needed). |
| Scalability | Vertically scalable (add resources to one machine). | Horizontally scalable (add more machines). |
| Structure | Tables, rows, and columns. | Key-value, documents, graphs, etc. |
| Query Language | SQL (powerful and standardized). | Varies by database. |
| Consistency | ACID compliant (strong consistency). | BASE compliant (eventual consistency). |
| Performance | Slower for high-traffic workloads. | Optimized for high-traffic workloads. |
| Use Cases | Financial records, CRM. | Social networks, IoT, big data. |

### When to Use SQL vs NoSQL?
**Choose SQL if**:
- Data is structured with clear relationships.
- Need for strict consistency (e.g., financial transactions).
- Complex queries or joins are required.

**Choose NoSQL if**:
- Data is semi-structured or unstructured.
- Horizontal scalability is critical.
- High write performance is needed (e.g., IoT data).

### Database Replication
- **Replication**: Sharing data across multiple databases to ensure consistency, reliability, and fault tolerance.
- **Purpose**: Improves accessibility, performance, and fault tolerance by maintaining redundant copies of the data.

#### Master-Slave Replication
- **How It Works**:
  - The master handles writes and replicates those writes to one or more slaves.
  - Slaves handle read-only operations and can replicate to additional slaves in a tree-like structure.
  - If the master fails, a slave can be promoted to master to continue operations.
- **Advantages**:
  - Backups can be taken without impacting the master.
  - Reduces read load on the master by using slaves.
  - Slaves can be synced back to the master without downtime.
- **Disadvantages**:
  - Adds hardware and complexity.
  - Downtime and possible data loss if the master fails.
  - Increased replication lag with many slaves.

#### Master-Master Replication
- **How It Works**:
  - Both nodes act as masters, handling both reads and writes, and they synchronize data with each other.
- **Advantages**:
  - Balanced write loads between two nodes.
  - Automatic and quick failover.
  - Both masters can serve read/write requests simultaneously.
- **Disadvantages**:
  - More complex to configure and deploy.
  - Synchronization can lead to write latency or data conflicts as the system scales.

#### Synchronous vs. Asynchronous Replication

| Replication Type | Synchronous | Asynchronous |
|------------------|-------------|--------------|
| How It Works | Writes to both primary and replica at the same time. | Writes to the replica after completing the write on the primary. |
| Consistency | Always consistent. | May have slight delays (eventual consistency). |
| Performance | Slower due to waiting for the replica. | Faster as replication happens in the background. |
| Use Cases | Critical systems needing strong consistency (e.g., financial data). | Systems prioritizing performance over immediate consistency. |

### Indexes
- **Definition**: Data structures used to speed up read operations in databases.
- **How It Works**:
  - Acts like a table of contents, pointing to the location of data in a table.
  - When an index is created on a column, the database stores that column and a pointer to the row in the index.

#### Dense vs. Sparse Indexes

| Index Type | Dense | Sparse |
|------------|-------|--------|
| Definition | Index record for every row in the table. | Index record for some rows only. |
| Advantages | Faster reads, no need for scans. | Requires less memory, faster writes. |
| Disadvantages | More memory usage, slower writes. | Slower reads, requires data scanning. |
| Use Case | General-purpose searches. | Ordered datasets or large data ranges. |

### Normalization and Denormalization

#### Common Terms in Normalization and Denormalization

##### Keys in Databases
Keys help uniquely identify records and establish relationships between tables.
1. **Primary Key**
   - A column (or group of columns) that uniquely identifies each row.
   - Example: ID in a Users table.
2. **Composite Key**
   - A primary key made up of multiple columns.
   - Example: (StudentID, CourseID) in an Enrollments table.
3. **Super Key**
   - A set of columns that can uniquely identify all rows in a table.
   - Example: (ID, Email, PhoneNumber), where each can be unique.
4. **Candidate Key**
   - A minimal super key (i.e., no extra attributes).
   - Example: (ID) and (Email) can both be candidate keys.
5. **Foreign Key**
   - A column that references the primary key of another table.
   - Example: CustomerID in an Orders table referencing ID in a Customers table.
6. **Alternate Key**
   - Any candidate key that is not chosen as the primary key.
   - Example: If (ID) is the primary key, (Email) becomes an alternate key.
7. **Surrogate Key**
   - A system-generated unique value (often auto-incremented).
   - Example: OrderID in an Orders table.

##### Dependencies in Normalization
Dependencies describe how attributes relate to each other.
1. **Partial Dependency**
   - Occurs when a part of the primary key determines other attributes.
   - Example: In (StudentID, CourseID) → Grade, CourseID → CourseName creates a partial dependency.
2. **Functional Dependency**
   - When one column determines another.
   - Example: StudentID → StudentName means StudentID uniquely determines the student's name.
3. **Transitive Functional Dependency**
   - When a non-key attribute determines another non-key attribute.
   - Example: StudentID → AdvisorID and AdvisorID → AdvisorName
     - Here, StudentID → AdvisorName is a transitive dependency.

##### Database Anomalies
Anomalies occur when improper database design leads to inconsistent or redundant data.
1. **Insertion Anomaly**
   - Happens when inserting data requires unrelated attributes.
   - Example: If John is a new employee but has no assigned team, we can't insert him because Team is a required column.
2. **Update Anomaly**
   - Occurs when updating one record requires multiple changes to maintain consistency.
   - Example: If Hailey gets promoted, we must update multiple rows, which can cause inconsistencies.
3. **Deletion Anomaly**
   - Happens when deleting data unintentionally removes useful information.
   - Example: If we delete Team B, we also lose all employees in that team.

##### Example Table Before Normalization

| ID | Name | Role | Team |
|----|------|------|------|
| 1 | Peter | Software Engineer | A |
| 2 | Brian | DevOps Engineer | B |
| 3 | Hailey | Product Manager | C |
| 4 | Hailey | Product Manager | C |
| 5 | Steve | Frontend Engineer | D |

**Problems in the Above Table**
- Insertion Anomaly: If John joins but has no team yet, we can't insert him.
- Update Anomaly: If Hailey is promoted, we need to update multiple rows.
- Deletion Anomaly: If Team B is removed, we also lose Brian's information.

##### Solution: Normalized Tables

1. **Employees Table**
| EmployeeID | Name | RoleID |
|------------|------|--------|
| 1 | Peter | 101 |
| 2 | Brian | 102 |
| 3 | Hailey | 103 |
| 4 | Steve | 104 |

2. **Roles Table**
| RoleID | Role |
|--------|------|
| 101 | Software Engineer |
| 102 | DevOps Engineer |
| 103 | Product Manager |
| 104 | Frontend Engineer |

3. **Teams Table**
| TeamID | TeamName |
|--------|----------|
| A | Team A |
| B | Team B |
| C | Team C |
| D | Team D |

4. **Employee-Team Mapping Table**
| EmployeeID | TeamID |
|------------|--------|
| 1 | A |
| 2 | B |
| 3 | C |
| 4 | C |
| 5 | D |

#### Normalization
- **Definition**: Organizing data to eliminate redundancy and ensure consistency.
- **Goal**: Reduce duplication, increase data consistency, and simplify database updates.
- **Normal Forms**:
  - 1NF: No repeating groups; each column holds atomic data.
  - 2NF: Meets 1NF and eliminates partial dependencies.
  - 3NF: Meets 2NF and eliminates transitive dependencies.
  - BCNF: A stricter version of 3NF to resolve specific anomalies.
- **Advantages**:
  - Reduces redundancy.
  - Improves data consistency.
  - Makes schema changes less disruptive.
- **Disadvantages**:
  - Complex data design.
  - Slower performance for reads.
  - Requires more joins in queries.

#### Denormalization
- **Definition**: Adding redundancy (duplicating data) to optimize read performance and simplify queries.
- **Goal**: Speed up data retrieval and reduce the complexity of queries by avoiding joins.
- **Advantages**:
  - Faster data retrieval.
  - Simplifies query writing.
  - Reduces the number of tables.
- **Disadvantages**:
  - Expensive inserts/updates.
  - Increases redundancy.
  - Greater risk of data inconsistency.

#### Replication vs. Normalization/Denormalization
- **Replication**: Involves duplicating databases to ensure reliability and availability.
- **Normalization/Denormalization**: Deals with structuring the data model within a database to balance performance and consistency.

### ACID and BASE Consistency Models
Databases follow different consistency models depending on their design goals. Two of the most common models are ACID (used in relational databases) and BASE (common in NoSQL databases).

#### ACID Model (Relational Databases)
ACID properties ensure data integrity during transaction processing. These properties are essential for high-reliability systems, like banking and financial applications.

| Property | Definition |
|----------|------------|
| Atomicity | All operations in a transaction succeed, or none are applied. If one part fails, the entire transaction is rolled back. |
| Consistency | The database remains structurally sound before and after a transaction. No invalid or corrupt data can be written. |
| Isolation | Transactions execute independently, preventing interference. Even if multiple transactions run in parallel, their effects must be the same as if they were executed sequentially. |
| Durability | Once a transaction is committed, it remains in the system even if the system crashes. |

**Example: Banking Transaction (ACID)**
- Scenario: Transferring $500 from Account A to Account B.
1. Atomicity: Either both debit and credit operations complete, or none happen.
2. Consistency: The total balance in the system remains the same.
3. Isolation: If multiple users transfer money at the same time, transactions don't mix.
4. Durability: If power goes out after a commit, the transaction is still recorded.

#### BASE Model (NoSQL Databases)
The BASE consistency model sacrifices strong consistency in favor of scalability, availability, and performance. It is widely used in distributed NoSQL databases.

| Property | Definition |
|----------|------------|
| Basic Availability | The system appears to work most of the time, even during failures. |
| Soft-State | Data may change over time, even without new input, due to background updates and replications. |
| Eventual Consistency | Data is not always immediately consistent across all nodes but will become consistent eventually. |

**Example: NoSQL Database (BASE)**
- Scenario: A social media app with millions of users.
1. Basic Availability: Even during downtime, the system still serves data.
2. Soft-State: A user's profile updates may take a few seconds to propagate.
3. Eventual Consistency: Different users may see different profile versions temporarily, but after some time, all nodes show the same version.

#### ACID vs BASE Trade-offs

| Aspect | ACID (SQL Databases) | BASE (NoSQL Databases) |
|--------|----------------------|------------------------|
| Consistency | Strong consistency | Eventual consistency |
| Scalability | Harder to scale horizontally | Easily scales across nodes |
| Performance | Slower due to strict rules | Faster due to relaxed consistency |
| Use Case | Banking, financial apps | Social media, real-time analytics |

### CAP Theorem
The CAP theorem states that in a distributed database, you can only achieve two of the three guarantees:
Consistency (C), Availability (A), and Partition Tolerance (P).

| Concept | Definition |
|---------|------------|
| Consistency (C) | All clients see the same data at the same time, no matter which node they connect to. |
| Availability (A) | The system always responds, even if some nodes are down. |
| Partition Tolerance (P) | The system continues to function despite network failures or node crashes. |

**Trade-off: You must choose P + (C or A)**
1. **CA (Consistency + Availability, No Partition Tolerance)**
   - If a network partition occurs, the system stops functioning.
   - Example: Traditional relational databases (PostgreSQL, MySQL).
2. **CP (Consistency + Partition Tolerance, No Availability)**
   - Some requests may fail or timeout to maintain consistency.
   - Example: MongoDB, Apache HBase.
3. **AP (Availability + Partition Tolerance, No Strong Consistency)**
   - Nodes remain available but may serve slightly outdated data.
   - Example: Apache Cassandra, CouchDB.

#### PACELC Theorem (Extends CAP Theorem)
PACELC extends CAP by adding a new factor: latency (L).
- CAP theorem only applies when a partition (P) occurs.
- PACELC states that even when there is no partition, a system must choose between latency (L) and consistency (C).

| Scenario | Choice |
|----------|--------|
| During Partition (P) | Choose C or A (like CAP theorem). |
| Else (E), No Partition | Choose L (Low Latency) or C (Strong Consistency). |

**Example**
- Amazon DynamoDB: AP under partitioning, but chooses low latency (L) when partitions do not exist.
- Google Spanner: CP under partitioning, but prefers consistency (C) over low latency.

### Database Transactions
A transaction is a set of operations performed together as a single unit.

| State | Description |
|-------|-------------|
| Active | Transaction is executing. |
| Partially Committed | All operations executed, but not written to disk yet. |
| Committed | Data is permanently saved. |
| Failed | A transaction fails due to an error. |
| Aborted | Changes are rolled back. |
| Terminated | Transaction is complete. |

#### Distributed Transactions
A distributed transaction operates across multiple databases or nodes, requiring coordination.

**Why do we need distributed transactions?**
- In microservices, each service may use a separate database.
- Transactions must either succeed entirely or fail entirely across all services.

**Solutions for Distributed Transactions**

1. **Two-Phase Commit (2PC)**
   A coordinator node ensures all nodes agree before committing.
   **Phases**:
   1. Prepare Phase: Nodes respond if they can commit.
   2. Commit Phase: If all nodes agree, the transaction is committed.
   **Problems**:
   - If the coordinator crashes, transactions are blocked.
   - Slow due to waiting for consensus.

2. **Three-Phase Commit (3PC)**
   Extends 2PC by adding a Pre-Commit Phase to reduce blocking.
   **Phases**:
   1. Prepare Phase: Nodes respond if they are ready.
   2. Pre-Commit Phase: Ensures all nodes have received the commit request.
   3. Commit Phase: Final commit.
   **Advantage**: Prevents indefinite waits.

3. **Sagas (Compensating Transactions)**
   A Saga is a sequence of independent transactions, each with a compensating transaction.
   **Types**:
   1. Choreography: Each transaction triggers the next one.
   2. Orchestration: A central Saga Orchestrator directs transactions.
   **Example: Flight Booking System**
   1. Book a flight ✈️.
   2. Reserve a hotel 🏨.
   3. If the hotel is unavailable, the system rolls back the flight booking.
   **Challenges**:
   - Hard to debug.
   - Can create cyclic dependencies.

#### Final Takeaways

| Concept | Use Case |
|---------|----------|
| ACID Transactions | Banking, e-commerce checkout, critical financial applications. |
| BASE Transactions | Social media, analytics, real-time search. |
| CAP Theorem | Choose between CP (MongoDB), AP (Cassandra), or CA (SQL). |
| PACELC Theorem | Balances latency vs. consistency. |
| Distributed Transactions | Needed in microservices and multi-database environments. |

### Sharding & Data Partitioning

#### Data Partitioning
Partitioning is the technique of splitting a large database into smaller, manageable pieces for better performance and scalability.

**Partitioning Methods**
1. **Horizontal Partitioning (Sharding)**
   - Splitting a table row-wise across multiple databases.
   - Each shard contains a subset of rows but has the same schema.
   - Example: Users with ID < 1000 go to DB1, ID >= 1000 go to DB2.
2. **Vertical Partitioning**
   - Splitting a table column-wise.
   - Frequently accessed columns go to DB1, less-used ones to DB2.
   - Example: A Users table split into UserCredentials (ID, username, password) and UserProfiles (ID, bio, profile_picture).

#### Sharding (Horizontal Partitioning)
Sharding distributes database rows across multiple machines to improve performance and scalability.

**How It Works**
- Each shard contains a subset of data.
- The system routes queries to the correct shard.
- Example: Instead of one large users table, we have users_shard_1, users_shard_2, etc.

**Partitioning Criteria for Sharding**
1. **Hash-Based Sharding**
   - Uses a hash function to determine which shard a row belongs to.
   - Example: UserID % 4 sends users to one of 4 shards.
   - Problem: Adding/removing shards disrupts the hashing.
2. **List-Based Sharding**
   - Assigns specific value ranges to shards.
   - Example:
     - Users from USA → Shard 1
     - Users from Europe → Shard 2
3. **Range-Based Sharding**
   - Uses ranges of values.
   - Example: Users with ID 1-1000 → Shard 1, 1001-2000 → Shard 2.
   - Problem: Uneven distribution if some ranges are more popular.
4. **Composite Sharding**
   - Combines two or more methods.
   - Example: First, range partitioning → then within each range, hash partitioning.

**Pros & Cons of Sharding**
✅ **Advantages**
- Scalability → Can add more shards to handle more data.
- Performance Boost → Queries hit smaller databases.
- Availability → If one shard fails, the others still work.

❌ **Disadvantages**
- Complexity → More difficult to manage and maintain.
- Joins Across Shards → Querying data from multiple shards is slow.
- Rebalancing → If shards become unevenly distributed, they need rebalancing.

#### Consistent Hashing
**Problem with Traditional Hashing**
- Uses Hash(key) % N, where N = number of nodes.
- Issue: Adding or removing a node changes N, breaking the hash mapping.

**Solution: Consistent Hashing**
- Maps data to a circular "hash ring".
- Nodes are also placed on the ring.
- When a request comes, it maps to the closest node clockwise.

**Benefits**
✅ Only a small portion of keys need reallocation when adding/removing nodes.
✅ Prevents massive remapping of data like traditional hashing.

**Virtual Nodes (VNodes)**
To ensure even distribution, each physical node is assigned multiple virtual nodes on the hash ring.

**Advantages**
- Fixes load imbalance (hotspots).
- Speeds up rebalancing after adding/removing nodes.

**Data Replication**
To increase durability and availability, each data item is replicated across multiple nodes (replication factor = N).

#### Database Federation
A federated database appears as a single logical database, but is split across multiple physical databases.

**Characteristics**
- Transparency → Users don't see the partitioning.
- Heterogeneity → Works with different databases.
- Extensibility → Easy to add new databases.
- Autonomy → Each database works independently.
- Data Integration → Combines multiple databases.

**Pros & Cons**
✅ **Advantages**
- Flexible data sharing.
- Integrates heterogeneous data sources.
- Legacy systems can remain unchanged.

❌ **Disadvantages**
- Complex to manage.
- Query performance can be slow.
- Joining data from different databases is difficult.

**Use Cases**
- Sharding → Used in high-traffic applications (e.g., Twitter, Facebook).
- Federation → Used when integrating multiple databases across different systems.

#### Summary

| Concept | Purpose |
|---------|---------|
| Sharding | Splits rows across multiple databases for scalability. |
| Consistent Hashing | Ensures minimal data redistribution when adding/removing nodes. |
| Federation | Makes multiple databases look like one logical system. |
| Replication | Stores copies of data on multiple nodes for redundancy. |

**Key Takeaways**
- Sharding → Best for scalability & performance, but complex.
- Consistent Hashing → Fixes rebalancing issues in distributed systems.
- Federation → Helps integrate multiple databases seamlessly.

