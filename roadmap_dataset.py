data_dict = {
  "dataset_name": "Developer Learning Roadmaps",
  "dataset_description": "A collection of prompt-response pairs for generating comprehensive developer roadmaps using PlantUML mind maps. Each entry includes a detailed learning path for a specific technology.",
  "data": [
    {
      "prompt": "Generate a complete PlantUML roadmap for learning Python, from fundamentals to advanced specializations.",
      "response": """@startmindmap
      title Comprehensive Python Learning Roadmap
      
      <style>
      mindmapDiagram {
        .beginner {
          BackgroundColor #C8E6C9
        }
        .intermediate {
          BackgroundColor #FFF9C4
        }
        .advanced {
          BackgroundColor #FFCCBC
        }
        .ecosystem {
           BackgroundColor #BBDEFB
        }
        .tools {
          BackgroundColor #F5F5F5
        }
      }
      </style>
      
      * **Python Mastery**
      
      **_ 1. Python Fundamentals <<beginner>>
      *** Setup & Environment
      **** Installing Python
      **** Using the Python Interpreter (REPL)
      **** Code Editors (VS Code, PyCharm)
      **** PEP 8 Style Guide
      *** Basic Syntax & Data Types
      **** Variables and Assignments
      **** Numbers (Integers, Floats)
      **** Strings (Formatting, Slicing, Methods)
      **** Booleans and `None`
      *** Core Data Structures
      **** Lists (Indexing, Methods, Mutability)
      **** Tuples (Immutability)
      **** Dictionaries (Key-Value Pairs)
      **** Sets (Unique Elements)
      *** Control Flow
      **** Conditional Statements (`if`, `elif`, `else`)
      **** `for` Loops (Iterating over sequences)
      **** `while` Loops
      **** `break`, `continue`, `pass`
      *** Functions
      **** Defining Functions (`def`)
      **** Arguments & Parameters (*args, **kwargs)
      **** Return Values
      **** Scope (Local vs. Global)
      **** Lambda Functions
      *** File I/O
      **** Reading from Files
      **** Writing to Files
      **** Using the `with` statement
      
      **_ 2. Intermediate Python <<intermediate>>
      *** Object-Oriented Programming (OOP)
      **** Classes and Objects
      **** Attributes and Methods
      **** `__init__` constructor
      **** Inheritance & Polymorphism
      **** Encapsulation (Public/Private)
      **** Dunder Methods (e.g., `__str__`, `__repr__`)
      *** Modules and Packages
      **** `import` statement
      **** Creating your own modules
      **** Standard Library Overview
      **** Package Management with `pip`
      *** Virtual Environments
      **** Why they are important
      **** Using `venv`
      *** Error and Exception Handling
      **** `try`, `except`, `else`, `finally`
      **** Raising custom exceptions
      *** Advanced Data Structures & Techniques
      **** List Comprehensions
      **** Dictionary and Set Comprehensions
      **** The `collections` Module
      ***** `defaultdict`, `Counter`, `deque`
      
      **_ 3. Advanced Python <<advanced>>
      *** Generators and Iterators
      **** The `yield` keyword
      **** Building custom iterators
      *** Decorators
      **** Understanding functions as objects
      **** Creating and using decorators
      *** Context Managers
      **** Building your own with `__enter__` and `__exit__`
      **** `contextlib` module
      *** Concurrency and Parallelism
      **** Threading (`threading`)
      **** Multiprocessing (`multiprocessing`)
      **** Asynchronous Programming (`asyncio`, `async`/`await`)
      
      **_ 4. Specializations & Ecosystem <<ecosystem>>
      *** Web Development
      **** Frameworks
      ***** Flask (Micro-framework)
      ***** Django (Full-stack)
      ***** FastAPI (Modern, high-performance)
      **** Key Concepts
      ***** APIs & REST
      ***** ORMs (e.g., SQLAlchemy)
      *** Data Science & Machine Learning
      **** Core Libraries
      ***** NumPy (Numerical computing)
      ***** Pandas (Data manipulation/analysis)
      ***** Matplotlib & Seaborn (Data visualization)
      **** Machine Learning
      ***** Scikit-learn (General ML)
      ***** TensorFlow / PyTorch (Deep Learning)
      *** Automation and Scripting
      **** Interacting with the OS (`os`, `sys`, `subprocess`)
      **** Web Scraping (`requests`, `BeautifulSoup`)
      **** Working with APIs (`requests`)
      
      **_ 5. Essential Tools & Best Practices <<tools>>
      *** Version Control
      **** Git & GitHub/GitLab
      *** Testing
      **** Why testing matters
      **** `unittest` (Built-in)
      **** `pytest` (Community standard)
      *** Linting and Formatting
      **** Flake8 (Linter)
      **** Black (Code Formatter)
      *** Debugging
      **** Using `print()` statements
      **** Python Debugger (`pdb`)
      **** Debugger in your IDE
      
      legend right
        | Category | Color |
        |<#C8E6C9>| Beginner Topics |
        |<#FFF9C4>| Intermediate Topics |
        |<#FFCCBC>| Advanced Topics |
        |<#BBDEFB>| Specializations |
        |<#F5F5F5>| Tools & Best Practices|
      end legend
      
      @endmindmap"""
    },
    {
      "prompt": "Generate a PlantUML mind map for a complete Java learning roadmap.",
      "response": """@startmindmap
      title Comprehensive Java Learning Roadmap
      
      <style>
      mindmapDiagram {
        .beginner {
          BackgroundColor #C8E6C9
        }
        .intermediate {
          BackgroundColor #FFF9C4
        }
        .advanced {
          BackgroundColor #FFCCBC
        }
        .ecosystem {
           BackgroundColor #BBDEFB
        }
        .tools {
          BackgroundColor #F5F5F5
        }
      }
      </style>
      
      * **Java Mastery**
      
      **_ 1. Core Java <<beginner>>
      *** Environment Setup
      **** JDK vs JRE vs JVM
      **** Installing Java (OpenJDK)
      **** IDEs (IntelliJ IDEA, Eclipse)
      *** Basic Syntax
      **** Variables & Primitive Data Types
      **** Operators
      **** Control Flow (if, for, while, switch)
      **** Methods
      *** Object-Oriented Programming (OOP) Fundamentals
      **** Classes and Objects
      **** Constructors
      **** `this` keyword
      **** Four Pillars: Encapsulation, Inheritance, Abstraction, Polymorphism
      *** Core APIs
      **** String, StringBuilder, StringBuffer
      **** Arrays
      **** Wrapper Classes
      **** Basic Exception Handling (try-catch-finally)
      **** File I/O (java.io)
      
      **_ 2. Intermediate Java <<intermediate>>
      *** Advanced OOP
      **** Abstract Classes and Interfaces
      **** `static` and `final` keywords
      **** Packages and `import`
      **** Enums
      *** Java Collections Framework
      **** `List` (ArrayList, LinkedList)
      **** `Set` (HashSet, TreeSet)
      **** `Map` (HashMap, TreeMap)
      **** `Queue` and `Deque`
      *** Generics
      **** Generic Classes and Methods
      **** Wildcards (`? extends`, `? super`)
      *** Exception Handling
      **** Checked vs Unchecked Exceptions
      **** Creating Custom Exceptions
      *** Java 8+ Features
      **** Lambda Expressions
      **** Functional Interfaces
      **** Stream API
      **** `Optional`
      
      **_ 3. Advanced Java <<advanced>>
      *** Concurrency & Multithreading
      **** `Thread` class and `Runnable` interface
      **** Synchronization and Locks
      **** `ExecutorService` and Thread Pools
      **** `java.util.concurrent` package
      *** JVM & Performance
      **** Memory Management (Heap, Stack)
      **** Garbage Collection
      **** Class Loaders
      **** Reflection API
      *** Networking
      **** Sockets (`java.net`)
      **** HTTP Clients
      *** New I/O (NIO)
      **** Buffers and Channels
      
      **_ 4. The Java Ecosystem <<ecosystem>>
      *** Build Tools
      **** Maven
      **** Gradle
      *** Web Development & Frameworks
      **** Servlets & JSP (Foundational)
      **** Spring Framework / Spring Boot <<reco>>
      **** Jakarta EE (formerly Java EE)
      **** Microservices Frameworks (Quarkus, Micronaut)
      *** Database Connectivity
      **** JDBC
      **** JPA / Hibernate (ORM)
      *** Testing
      **** JUnit 5
      **** Mockito
      *** Cloud & DevOps
      **** Containerization (Docker)
      **** Spring Cloud
      
      **_ 5. Best Practices & Tools <<tools>>
      *** Version Control
      **** Git / GitHub
      *** Design Patterns
      **** Singleton, Factory, Observer, etc.
      *** SOLID Principles
      *** Logging
      **** SLF4J & Logback
      *** Code Quality
      **** SonarLint / SonarQube
      
      legend right
        | Category | Color |
        |<#C8E6C9>| Core / Beginner |
        |<#FFF9C4>| Intermediate |
        |<#FFCCBC>| Advanced |
        |<#BBDEFB>| Ecosystem & Frameworks |
        |<#F5F5F5>| Tools & Best Practices|
      end legend
      
      @endmindmap"""
    },
    {
      "prompt": "Create a detailed PlantUML roadmap for learning SQL, from basic syntax to advanced query optimization.",
      "response": """@startmindmap
      title SQL Learning Roadmap
      
      <style>
      mindmapDiagram {
        .topic {
          BackgroundColor #BBDEFB
        }
        .ddl {
          BackgroundColor #FFCDD2
        }
        .dml {
          BackgroundColor #C8E6C9
        }
        .advanced {
          BackgroundColor #F8BBD0
        }
        .concept {
           BackgroundColor #FFF9C4
        }
      }
      </style>
      
      * **SQL Mastery**
      
      **_ 1. SQL Basics <<topic>>
      *** What are Relational Databases?
      *** RDBMS Concepts
      *** SQL vs NoSQL
      
      **_ 2. Basic SQL Syntax <<concept>>
      *** SQL Keywords
      *** Data Types
      *** Operators
      
      **_ 3. Data Definition Language (DDL) <<ddl>>
      *** CREATE Table
      *** ALTER Table
      *** DROP Table
      *** TRUNCATE Table
      
      **_ 4. Data Manipulation Language (DML) <<dml>>
      *** SELECT (FROM, WHERE)
      *** INSERT
      *** UPDATE
      *** DELETE
      *** Aggregate Queries
      **** SUM, COUNT, AVG, MIN, MAX
      **** GROUP BY, HAVING
      
      **_ 5. Intermediate Concepts <<topic>>
      *** Data Constraints <<concept>>
      **** Primary Key, Foreign Key
      **** Unique, NOT NULL, CHECK
      *** JOIN Queries <<concept>>
      **** INNER, LEFT, RIGHT, FULL OUTER
      **** Self Join, Cross Join
      *** Subqueries <<concept>>
      **** Nested & Correlated
      *** Views <<concept>>
      **** Creating, Modifying, Dropping
      *** Indexes <<concept>>
      **** Managing & Optimizing
      
      **_ 6. Advanced Functions <<advanced>>
      *** String Functions
      **** CONCAT, SUBSTRING, UPPER...
      *** Numeric Functions
      **** ROUND, CEILING, FLOOR...
      *** Date and Time Functions
      **** DATEADD, DATEPART, NOW...
      *** Conditional Logic
      **** CASE, NULLIF, COALESCE
      
      **_ 7. Advanced SQL & Security <<topic>>
      *** Data Integrity & Security
      **** Transactions (ACID)
      ***** BEGIN, COMMIT, ROLLBACK
      **** Stored Procedures & Functions
      **** DB Security Best Practices (GRANT, REVOKE)
      *** Advanced Querying <<advanced>>
      **** Window Functions
      ***** rank, lead, lag, Row_number
      **** Common Table Expressions (CTEs)
      **** Recursive Queries
      **** Pivot / Unpivot Operations
      *** Performance Optimization <<concept>>
      **** Query Analysis (EXPLAIN)
      **** Indexing Strategies
      **** Optimizing Joins
      
      legend right
        | Category | Color |
        |<#BBDEFB>| Topic Area |
        |<#FFF9C4>| Core Concept |
        |<#FFCDD2>| DDL Command |
        |<#C8E6C9>| DML Command |
        |<#F8BBD0>| Advanced Feature |
      end legend
      
      @endmindmap"""
    },
    {
      "prompt": "I need a PlantUML mind map for the React developer roadmap, including the modern ecosystem.",
      "response": """@startmindmap
      title Modern React Developer Roadmap
      
      <style>
      mindmapDiagram {
        .reco {
          BackgroundColor #D8BFD8
          FontColor #000000
          LineColor #800080
        }
        .alt {
          BackgroundColor #C8E6C9
          FontColor #000000
          LineColor #2E7D32
        }
        .core {
          BackgroundColor #FFF9C4
        }
        .category {
          BackgroundColor #E1F5FE
        }
      }
      </style>
      
      * **React**
      **_ **Note:** First, master JavaScript fundamentals!
      
      **_ 1. Core React Concepts <<core>>
      *** Components
      **** Functional Components <<reco>>
      **** JSX & Props vs State
      **** Conditional Rendering & Composition
      *** Rendering
      **** Component Lifecycle
      **** Lists and Keys
      **** Refs & Events
      *** Hooks
      **** Basic: useState, useEffect, useContext <<reco>>
      **** Advanced: useReducer, useCallback, useMemo, useRef <<reco>>
      **** Creating Custom Hooks
      
      **_ 2. React Ecosystem <<category>>
      *** Component Libraries
      **** Material UI <<reco>>
      **** Chakra UI <<alt>>
      **** Headless: Radix UI <<reco>>
      *** Writing CSS
      **** Tailwind CSS <<reco>>
      **** CSS Modules <<alt>>
      **** Styled-Components
      *** State Management
      **** Zustand <<reco>>
      **** Context API (for simple state) <<core>>
      **** Jotai <<alt>>
      **** Redux Toolkit (for large-scale apps) <<alt>>
      *** Routers
      **** React Router <<reco>>
      **** Tanstack Router <<alt>>
      *** API Calls (Data Fetching)
      **** REST: React Query, SWR <<reco>>
      **** GraphQL: Apollo Client <<reco>>
      *** Testing
      **** Vitest / Jest <<reco>>
      **** React Testing Library <<reco>>
      **** Cypress / Playwright (E2E) <<alt>>
      
      **_ 3. Frameworks & Advanced Topics <<category>>
      *** Frameworks
      **** Next.js <<reco>>
      **** Astro <<alt>>
      *** Forms
      **** React Hook Form <<reco>>
      **** Formik <<alt>>
      *** Types & Validation
      **** TypeScript <<reco>>
      **** Zod <<reco>>
      *** Advanced Rendering & Performance
      **** Error Boundaries
      **** Suspense & Portals
      **** Memoization & Code Splitting
      *** Mobile Applications
      **** React Native <<reco>>
      
      legend right
        | Technology Type | Color |
        |<#D8BFD8>| Personal Recommendation |
        |<#C8E6C9>| Alternative Option |
        |<#FFF9C4>| Core React Skill |
        |<#E1F5FE>| Ecosystem Category |
      end legend
      
      @endmindmap"""
    },
    {
      "prompt": "Can you generate the PlantUML code for a complete frontend developer roadmap?",
      "response": """@startmindmap
      title Front-end Developer Roadmap
      
      <style>
      mindmapDiagram {
        .reco {
          BackgroundColor #D8BFD8
          FontColor #000000
          LineColor #800080
        }
        .alt {
          BackgroundColor #C8E6C9
          FontColor #000000
          LineColor #2E7D32
        }
        .core {
          BackgroundColor #FFF9C4
        }
        .category {
          BackgroundColor #E1F5FE
        }
      }
      </style>
      
      * **Front-end Development**
      
      **_ 1. Foundations <<core>>
      *** Internet Basics
      **** How does the internet work?
      **** HTTP/HTTPS
      **** Domain Name, DNS, Hosting
      **** How Browsers work
      *** HTML
      **** Writing Semantic HTML
      **** Forms and Validations
      **** Accessibility (a11y)
      **** SEO Basics
      *** CSS
      **** Making Layouts (Flexbox, Grid)
      **** Responsive Design & Media Queries
      **** CSS Variables, Pseudo-classes
      *** JavaScript
      **** Core Language (Variables, Types, Functions, Scope)
      **** DOM Manipulation & Events
      **** Asynchronous JS (Promises, async/await)
      **** ES6+ Features
      **** Fetch API / AJAX
      
      **_ 2. Tools & Workflow <<category>>
      *** Version Control
      **** Git & GitHub <<reco>>
      *** Package Managers
      **** npm
      **** yarn
      *** Build Tools
      **** Linters & Formatters (ESLint, Prettier) <<reco>>
      **** Module Bundlers (Vite, Webpack) <<reco>>
      
      **_ 3. CSS Architecture & Frameworks <<category>>
      *** CSS Methodologies
      **** BEM
      *** CSS Preprocessors
      **** Sass <<reco>>
      *** CSS Frameworks
      **** Tailwind CSS <<reco>>
      **** Bootstrap <<alt>>
      
      **_ 4. JavaScript Frameworks <<category>>
      *** Pick a Framework
      **** React <<reco>>
      **** Vue.js <<alt>>
      **** Angular <<alt>>
      **** Svelte <<alt>>
      
      **_ 5. Advanced Topics & Specializations <<category>>
      *** Type Checkers
      **** TypeScript <<reco>>
      *** Testing
      **** Unit, Integration, End-to-End
      **** Jest, Vitest, Cypress, Playwright
      *** Web Security Basics
      **** CORS, HTTPS, CSP, OWASP Top 10
      *** Performance
      **** Measuring Metrics (Lighthouse)
      **** Optimizing Assets (Images, Code Splitting)
      *** Web Components
      *** Progressive Web Apps (PWAs)
      *** Server-Side Rendering (SSR)
      **** Next.js (React) <<reco>>
      **** Nuxt.js (Vue) <<alt>>
      *** GraphQL
      **** Apollo Client
      
      legend right
        | Technology Type | Color |
        |<#D8BFD8>| Personal Recommendation |
        |<#C8E6C9>| Alternative Option |
        |<#FFF9C4>| Core Skill / Concept |
        |<#E1F5FE>| General Category |
      end legend
      
      @endmindmap"""
    },
    {
      "prompt": "Generate a PlantUML roadmap for learning AI and Machine Learning using Python.",
      "response": """@startmindmap
      title AI & Machine Learning with Python Roadmap
      
      <style>
      mindmapDiagram {
        .foundation {
          BackgroundColor #E1F5FE
        }
        .core_ml {
          BackgroundColor #C8E6C9
        }
        .deep_learning {
          BackgroundColor #FFF9C4
        }
        .specialization {
           BackgroundColor #FFCCBC
        }
        .tools {
          BackgroundColor #F5F5F5
        }
      }
      </style>
      
      * **AI & Machine Learning Mastery**
      
      **_ 1. Foundations <<foundation>>
      *** Math Prerequisites
      **** Linear Algebra (Vectors, Matrices, Eigenvalues)
      **** Calculus (Derivatives, Gradients)
      **** Probability & Statistics (Mean, Median, Variance, Distributions)
      *** Python for Data Science
      **** NumPy for numerical operations & arrays
      **** Pandas for data manipulation & DataFrames
      **** Matplotlib & Seaborn for data visualization
      
      **_ 2. Core Machine Learning <<core_ml>>
      *** ML Concepts
      **** Supervised vs Unsupervised vs Reinforcement Learning
      **** Overfitting vs Underfitting (Bias-Variance Tradeoff)
      **** Feature Engineering & Selection
      **** Model Evaluation Metrics (Accuracy, Precision, Recall, F1, MSE)
      *** Supervised Learning
      **** Regression (Linear, Polynomial)
      **** Classification (Logistic Regression, k-NN, SVM, Decision Trees, Random Forests)
      *** Unsupervised Learning
      **** Clustering (K-Means, Hierarchical)
      **** Dimensionality Reduction (PCA, t-SNE)
      
      **_ 3. Deep Learning <<deep_learning>>
      *** Neural Network Fundamentals
      **** Neurons, Layers, Activation Functions
      **** Backpropagation & Gradient Descent
      **** Loss Functions & Optimizers
      *** Deep Learning Frameworks
      **** TensorFlow & Keras
      **** PyTorch
      *** Architectures
      **** Convolutional Neural Networks (CNNs) for Computer Vision
      **** Recurrent Neural Networks (RNNs) & LSTMs for Sequential Data
      **** Transformers (Attention Mechanism)
      
      **_ 4. Specializations <<specialization>>
      *** Natural Language Processing (NLP)
      **** Text Preprocessing (Tokenization, Stemming)
      **** Word Embeddings (Word2Vec, GloVe)
      **** Libraries: NLTK, spaCy, Hugging Face Transformers
      *** Computer Vision (CV)
      **** Image Processing & Augmentation
      **** Object Detection & Segmentation
      **** Libraries: OpenCV, Pillow
      *** Reinforcement Learning (RL)
      **** Concepts: Agents, Environments, Rewards
      **** Libraries: OpenAI Gym
      *** MLOps (Machine Learning Operations)
      **** Model Deployment (Flask, FastAPI)
      **** Containerization (Docker)
      **** Model Monitoring & Versioning
      
      **_ 5. Essential Tools & Platforms <<tools>>
      *** Development Environment
      **** Jupyter Notebooks / JupyterLab
      **** Google Colab
      *** Version Control
      **** Git & GitHub
      *** Cloud Platforms
      **** AWS SageMaker
      **** Google AI Platform
      **** Azure Machine Learning
      
      legend right
        | Category | Color |
        |<#E1F5FE>| Foundations |
        |<#C8E6C9>| Core Machine Learning |
        |<#FFF9C4>| Deep Learning |
        |<#FFCCBC>| Specializations |
        |<#F5F5F5>| Tools & Platforms|
      end legend
      
      @endmindmap"""
    },
    {
      "prompt": "Create a PlantUML mind map for a Data Structures & Algorithms (DSA) learning path.",
      "response": """@startmindmap
      title Data Structures & Algorithms (DSA) Roadmap
      
      <style>
      mindmapDiagram {
          .prereq {
            BackgroundColor #F5F5F5
        }
        .ds {
            BackgroundColor #C8E6C9
        }
        .algo {
            BackgroundColor #BBDEFB
        }
        .practice {
             BackgroundColor #FFF9C4
        }
      }
      </style>
      
      * **DSA Mastery**
      
      **_ 1. Prerequisites <<prereq>>
      *** Choose a Programming Language
      **** Python (Easy syntax)
      **** C++ (Performance)
      **** Java (Widely used)
      *** Algorithmic Complexity
      **** Big O Notation
      **** Time Complexity
      **** Space Complexity
      
      **_ 2. Data Structures <<ds>>
      *** Linear Data Structures
      **** Arrays / Lists
      **** Linked Lists (Singly, Doubly, Circular)
      **** Stacks (LIFO)
      **** Queues (FIFO)
      **** Deques
      *** Non-Linear Data Structures
      **** Hash Tables (Hash Maps, Hash Sets)
      **** Trees
      ***** Binary Trees & Binary Search Trees (BST)
      ***** Self-Balancing Trees (AVL, Red-Black)
      ***** Tries
      **** Heaps (Min-Heap, Max-Heap)
      **** Graphs
      ***** Directed vs Undirected
      ***** Adjacency Matrix vs Adjacency List
      
      **_ 3. Core Algorithms <<algo>>
      *** Searching
      **** Linear Search
      **** Binary Search (on sorted arrays)
      *** Sorting
      **** Simple Sorts (Bubble, Selection, Insertion) - O(n^2)
      **** Efficient Sorts (Merge Sort, Quick Sort, Heap Sort) - O(n log n)
      *** Graph Algorithms
      **** Traversal: Breadth-First Search (BFS), Depth-First Search (DFS)
      **** Shortest Path: Dijkstra's Algorithm, Bellman-Ford
      **** Minimum Spanning Tree: Prim's, Kruskal's
      *** Dynamic Programming (DP)
      **** Core Concepts: Memoization, Tabulation
      **** Common Problems: Fibonacci, Knapsack, Longest Common Subsequence
      *** Other Algorithm Paradigms
      **** Greedy Algorithms
      **** Divide and Conquer
      **** Backtracking
      **** Two Pointers
      **** Sliding Window
      
      **_ 4. Practice & Application <<practice>>
      *** Problem Solving Platforms
      **** LeetCode
      **** HackerRank
      **** Codeforces
      *** Common Problem Patterns
      **** Know your data structures
      **** Recognize algorithm patterns (e.g., when to use DP vs Greedy)
      *** Interview Preparation
      **** Practice explaining your solution
      **** Analyze complexity of your code
      
      legend right
        | Category | Color |
        |<#F5F5F5>| Prerequisites |
        |<#C8E6C9>| Data Structures |
        |<#BBDEFB>| Algorithms |
        |<#FFF9C4>| Practice & Application |
      end legend
      
      @endmindmap"""
    },
    {
      "prompt": "Generate a comprehensive PlantUML roadmap for learning Computer Networking.",
      "response": """@startmindmap
      title Computer Networking Roadmap
      
      <style>
      mindmapDiagram {
        .l1_physical {
          BackgroundColor #FFCDD2
        }
        .l2_datalink {
          BackgroundColor #F8BBD0
        }
        .l3_network {
          BackgroundColor #E1BEE7
        }
        .l4_transport {
          BackgroundColor #D1C4E9
        }
        .l5_application {
          BackgroundColor #C5CAE9
        }
        .security {
          BackgroundColor #FFCCBC
        }
        .tools {
          BackgroundColor #F5F5F5
        }
        .fundamentals {
          BackgroundColor #E0E0E0
        }
      }
      </style>
      
      * **Computer Networking Mastery**
      
      **_ 1. Networking Fundamentals <<fundamentals>>
      *** What is a Network?
      *** LAN, WAN, MAN
      *** Network Topologies (Bus, Star, Ring)
      *** Network Devices (Hub, Switch, Router)
      *** The OSI & TCP/IP Models
      
      **_ 2. The Network Layers**
      *** Layer 1: Physical Layer <<l1_physical>>
      **** Cabling (Ethernet, Fiber Optic)
      **** Hubs, Repeaters
      **** Bits
      *** Layer 2: Data Link Layer <<l2_datalink>>
      **** MAC Addresses
      **** Switches
      **** Ethernet Frames
      **** ARP (Address Resolution Protocol)
      *** Layer 3: Network Layer <<l3_network>>
      **** IP Addresses (IPv4 vs IPv6)
      **** Subnetting
      **** Routers & Routing Protocols (e.g., OSPF)
      **** ICMP (Ping, Traceroute)
      *** Layer 4: Transport Layer <<l4_transport>>
      **** TCP (Reliable, Connection-Oriented)
      ***** 3-Way Handshake
      **** UDP (Unreliable, Connectionless)
      **** Ports & Sockets
      *** Layer 5-7: Application Layer <<l5_application>>
      **** DNS (Domain Name System)
      **** HTTP & HTTPS (Web)
      **** FTP (File Transfer)
      **** SMTP, IMAP, POP3 (Email)
      **** SSH (Secure Shell)
      **** DHCP (Dynamic Host Configuration)
      
      **_ 3. Network Security <<security>>
      *** Firewalls & ACLs
      *** VPNs (Virtual Private Networks)
      *** Encryption (TLS/SSL)
      *** Common Attacks
      **** DDoS, Man-in-the-Middle, Phishing
      
      **_ 4. Modern Networking Concepts
      *** Wireless Networking (Wi-Fi)
      *** Cloud Networking
      **** VPC (Virtual Private Cloud)
      **** Load Balancers
      *** Software-Defined Networking (SDN)
      *** Content Delivery Networks (CDN)
      
      **_ 5. Essential Tools & Commands <<tools>>
      *** Command Line Utilities
      **** `ping`
      **** `traceroute` / `tracert`
      **** `ipconfig` / `ifconfig`
      **** `nslookup` / `dig`
      **** `netstat`
      *** Network Analysis
      **** Wireshark
      
      legend right
        | Category | Color |
        |<#E0E0E0>| Fundamentals|
        |<#FFCDD2>| Physical Layer |
        |<#F8BBD0>| Data Link Layer |
        |<#E1BEE7>| Network Layer |
        |<#D1C4E9>| Transport Layer |
        |<#C5CAE9>| Application Layer |
        |<#FFCCBC>| Security |
        |<#F5F5F5>| Tools |
      end legend
      
      @endmindmap"""
    }
  ]
}