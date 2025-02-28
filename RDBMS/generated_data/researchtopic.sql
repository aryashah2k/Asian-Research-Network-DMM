-- Inserting data into ResearchTopic
INSERT INTO
    ResearchTopic (
        TopicID,
        `Name`,
        `Description`,
        ParentTopic,
        PopularityScore,
        TrendIndex
    )
VALUES
    (
        1,
        'Quantum Computing',
        'Study of quantum-mechanical phenomena for computation.',
        NULL,
        0.92,
        0.75
    ),
    (
        2,
        'Artificial Intelligence',
        'Simulation of human intelligence in machines.',
        NULL,
        0.98,
        0.85
    ),
    (
        3,
        'Machine Learning',
        'Subset of AI focused on data-driven model training.',
        1,
        0.95,
        0.9
    ),
    (
        4,
        'Blockchain Technology',
        'Decentralized digital ledger for recording transactions.',
        NULL,
        0.87,
        0.6
    ),
    (
        5,
        'Cybersecurity',
        'Protection of computer systems from theft or damage.',
        NULL,
        0.91,
        0.7
    ),
    (
        6,
        'Nanotechnology',
        'Manipulation of matter on an atomic, molecular scale.',
        NULL,
        0.83,
        0.5
    ),
    (
        7,
        'Renewable Energy',
        'Energy from natural sources that are constantly replenished.',
        NULL,
        0.89,
        0.8
    ),
    (
        8,
        'Biotechnology',
        'Use of living systems and organisms to develop products.',
        NULL,
        0.88,
        0.65
    ),
    (
        9,
        'Internet of Things',
        'Network of physical objects connected to the internet.',
        NULL,
        0.9,
        0.78
    ),
    (
        10,
        '5G Technology',
        'Fifth generation mobile network technology.',
        NULL,
        0.86,
        0.72
    ),
    (
        11,
        'Augmented Reality',
        'Interactive experience of a real-world environment enhanced by computer-generated information.',
        NULL,
        0.82,
        0.6
    ),
    (
        12,
        'Virtual Reality',
        'Computer-generated simulation of a three-dimensional environment.',
        NULL,
        0.84,
        0.7
    ),
    (
        13,
        'Robotics',
        'Design, construction, operation, and use of robots.',
        NULL,
        0.88,
        0.65
    ),
    (
        14,
        'Gene Editing',
        'Genetic engineering technique for modifying DNA sequences.',
        NULL,
        0.85,
        0.55
    ),
    (
        15,
        'Climate Change',
        'Long-term alteration of temperature and typical weather patterns.',
        NULL,
        0.93,
        0.8
    ),
    (
        16,
        'Big Data',
        'Large and complex data sets that require advanced data processing applications.',
        NULL,
        0.9,
        0.75
    ),
    (
        17,
        'Autonomous Vehicles',
        'Vehicles capable of sensing their environment and operating without human involvement.',
        NULL,
        0.87,
        0.7
    ),
    (
        18,
        'Space Exploration',
        'Investigation of outer space through astronomy and space technology.',
        NULL,
        0.84,
        0.6
    ),
    (
        19,
        'Smart Cities',
        'Urban areas that use different types of electronic methods and sensors to collect data.',
        NULL,
        0.83,
        0.65
    ),
    (
        20,
        'Wearable Technology',
        'Electronic devices worn as accessories or embedded in clothing.',
        NULL,
        0.81,
        0.55
    ),
    (
        21,
        'Digital Health',
        'Use of digital technologies to improve health and healthcare services.',
        NULL,
        0.89,
        0.7
    ),
    (
        22,
        'Synthetic Biology',
        'Design and construction of new biological parts and systems.',
        NULL,
        0.8,
        0.5
    ),
    (
        23,
        'Smart Grids',
        'Electrical grid that uses information and communication technology to gather and act on information.',
        NULL,
        0.82,
        0.6
    ),
    (
        24,
        'Agricultural Technology',
        'Use of technology in agriculture to improve yield, efficiency, and profitability.',
        NULL,
        0.85,
        0.7
    ),
    (
        25,
        'Fintech',
        'Integration of technology into offerings by financial services companies.',
        NULL,
        0.88,
        0.75
    ),
    (
        26,
        'E-commerce',
        'Buying and selling of goods and services over the internet.',
        NULL,
        0.9,
        0.8
    ),
    (
        27,
        'Social Media Analysis',
        'Study of social media data to understand user behavior and trends.',
        NULL,
        0.86,
        0.65
    ),
    (
        28,
        'Digital Marketing',
        'Promotion of products or brands via electronic media.',
        NULL,
        0.87,
        0.7
    ),
    (
        29,
        'Telemedicine',
        'Remote diagnosis and treatment of patients using telecommunications technology.',
        NULL,
        0.89,
        0.75
    ),
    (
        30,
        '3D Printing',
        'Additive manufacturing process of making three-dimensional objects.',
        NULL,
        0.83,
        0.6
    ),
    (
        31,
        'Smart Home Technology',
        'Home devices that are connected to the internet and can be controlled remotely.',
        NULL,
        0.82,
        0.55
    ),
    (
        32,
        'Biometrics',
        'Measurement and statistical analysis of people''s physical and behavioral characteristics.',
        NULL,
        0.84,
        0.6
    ),
    (
        33,
        'Cloud Computing',
        'Delivery of computing services over the internet.',
        NULL,
        0.91,
        0.8
    ),
    (
        34,
        'Edge Computing',
        'Processing data near the edge of the network, where it is generated.',
        NULL,
        0.85,
        0.65
    ),
    (
        35,
        'Data Privacy',
        'Protection of personal data from unauthorized access.',
        NULL,
        0.9,
        0.75
    ),
    (
        36,
        'Digital Twins',
        'Virtual models of physical objects or systems.',
        NULL,
        0.81,
        0.55
    ),
    (
        37,
        'Natural Language Processing',
        'Branch of AI focused on interaction between computers and humans using natural language.',
        NULL,
        0.88,
        0.7
    ),
    (
        38,
        'Quantum Cryptography',
        'Use of quantum mechanics to secure communication.',
        NULL,
        0.83,
        0.6
    ),
    (
        39,
        'Renewable Materials',
        'Materials derived from renewable resources.',
        NULL,
        0.82,
        0.55
    ),
    (
        40,
        'Circular Economy',
        'Economic system aimed at eliminating waste and the continual use of resources.',
        NULL,
        0.87,
        0.7
    ),
    (
        41,
        'Smart Manufacturing',
        'Use of advanced information and manufacturing technologies to optimize production.',
        NULL,
        0.85,
        0.65
    ),
    (
        42,
        'Bioinformatics',
        'Application of computer technology to the management of biological information.',
        NULL,
        0.84,
        0.6
    ),
    (
        43,
        'Sustainable Development',
        'Development that meets the needs of the present without compromising future generations.',
        NULL,
        0.9,
        0.8
    ),
    (
        44,
        'Personalized Medicine',
        'Medical model using characterization of individuals'' phenotypes and genotypes.',
        NULL,
        0.88,
        0.75
    ),
    (
        45,
        'Human-Computer Interaction',
        'Design and use of computer technology, focusing on the interfaces between people and computers.',
        NULL,
        0.86,
        0.7
    ),
    (
        46,
        'Cryptocurrency',
        'Digital or virtual currency that uses cryptography for security.',
        NULL,
        0.89,
        0.75
    ),
    (
        47,
        'Virtual Assistants',
        'Software agents that can perform tasks or services for an individual.',
        NULL,
        0.87,
        0.7
    ),
    (
        48,
        'Environmental Science',
        'Study of the environment and solutions to environmental problems.',
        NULL,
        0.92,
        0.8
    ),
    (
        49,
        'Digital Transformation',
        'Integration of digital technology into all areas of a business.',
        NULL,
        0.91,
        0.75
    ),
    (
        50,
        'Smart Contracts',
        'Self-executing contracts with the terms of the agreement directly written into code.',
        NULL,
        0.85,
        0.65
    );