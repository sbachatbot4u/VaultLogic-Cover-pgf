from models import ComplianceSection, ChatMessage
from typing import List, Dict
import re

# Comprehensive compliance handbook content
COMPLIANCE_HANDBOOK = {
    "sections": [
        ComplianceSection(
            title="SOC 2 Type II Compliance",
            content="""
            VaultLogic maintains SOC 2 Type II certification, demonstrating our commitment to security, availability, processing integrity, confidentiality, and privacy. Our controls are audited annually by independent third-party auditors.

            Key SOC 2 Controls:
            - Access control and user authentication
            - System monitoring and logging
            - Data encryption in transit and at rest
            - Business continuity and disaster recovery
            - Vendor management and risk assessment
            - Change management processes
            - Physical and environmental security

            Our SOC 2 Type II report is available to customers under NDA and demonstrates compliance with AICPA Trust Service Criteria across all five trust service categories.
            """,
            page_number=1,
            subsections=["Access Controls", "Monitoring", "Encryption", "Business Continuity"]
        ),
        ComplianceSection(
            title="GDPR Data Protection Compliance",
            content="""
            VaultLogic is fully compliant with the General Data Protection Regulation (GDPR), ensuring the protection and privacy of personal data for EU residents. Our on-premise deployment model ensures data never leaves your infrastructure.

            GDPR Compliance Features:
            - Data minimization and purpose limitation
            - Lawful basis for processing
            - Right to access, rectification, and erasure
            - Data portability and processing transparency
            - Privacy by design and by default
            - Data Protection Impact Assessments (DPIA)
            - Breach notification procedures

            All personal data processing is conducted in accordance with Article 6 and Article 9 of GDPR, with appropriate technical and organizational measures in place.
            """,
            page_number=2,
            subsections=["Data Rights", "Processing Lawfulness", "Technical Measures", "Organizational Measures"]
        ),
        ComplianceSection(
            title="HIPAA Healthcare Compliance",
            content="""
            VaultLogic supports HIPAA compliance for healthcare organizations processing Protected Health Information (PHI). Our platform includes administrative, physical, and technical safeguards required by HIPAA.

            HIPAA Safeguards Implementation:
            - Administrative safeguards: Security officer designation, workforce training, access management
            - Physical safeguards: Facility access controls, workstation security, device controls
            - Technical safeguards: Access control, audit controls, integrity, transmission security
            - Business Associate Agreements (BAA) available
            - Risk assessment and management procedures
            - Incident response and breach notification

            Our on-premise deployment ensures PHI never leaves your controlled environment, maintaining the highest level of data protection.
            """,
            page_number=3,
            subsections=["Administrative Safeguards", "Physical Safeguards", "Technical Safeguards", "BAA Requirements"]
        ),
        ComplianceSection(
            title="ISO 27001 Information Security",
            content="""
            VaultLogic is ISO 27001 certified, demonstrating our comprehensive approach to information security management. Our Information Security Management System (ISMS) follows international best practices.

            ISO 27001 Implementation:
            - Information security policies and procedures
            - Risk assessment and treatment methodology
            - Security awareness and training programs
            - Incident management and response
            - Business continuity management
            - Supplier relationship security
            - Continuous improvement processes

            Our ISMS is regularly audited and updated to address emerging threats and maintain certification compliance.
            """,
            page_number=4,
            subsections=["ISMS Framework", "Risk Management", "Security Controls", "Continuous Improvement"]
        ),
        ComplianceSection(
            title="Data Encryption and Security",
            content="""
            VaultLogic implements military-grade encryption and security measures to protect sensitive documents and data throughout the entire processing lifecycle.

            Encryption Standards:
            - AES-256 encryption for data at rest
            - TLS 1.3 for data in transit
            - End-to-end encryption for all communications
            - Hardware Security Module (HSM) integration
            - Key management and rotation procedures
            - Zero-knowledge architecture design

            Security Architecture:
            - Network segmentation and firewalls
            - Intrusion detection and prevention
            - Multi-factor authentication
            - Role-based access control (RBAC)
            - Security monitoring and SIEM integration
            """,
            page_number=5,
            subsections=["Encryption Standards", "Key Management", "Network Security", "Access Control"]
        ),
        ComplianceSection(
            title="Audit Logging and Monitoring",
            content="""
            VaultLogic provides comprehensive audit logging and monitoring capabilities to ensure transparency and accountability for all system activities.

            Audit Capabilities:
            - Comprehensive activity logging
            - User access and authentication logs
            - Document processing and query logs
            - System configuration change logs
            - Security event monitoring and alerting
            - Compliance reporting and dashboards
            - Long-term log retention and archival

            Monitoring Features:
            - Real-time security monitoring
            - Anomaly detection and alerting
            - Performance monitoring and optimization
            - Compliance score tracking
            - Automated compliance reporting
            """,
            page_number=6,
            subsections=["Activity Logging", "Security Monitoring", "Compliance Reporting", "Alerting"]
        ),
        ComplianceSection(
            title="Business Continuity and Disaster Recovery",
            content="""
            VaultLogic maintains robust business continuity and disaster recovery procedures to ensure service availability and data protection during adverse events.

            Business Continuity Planning:
            - Recovery Time Objective (RTO): 4 hours
            - Recovery Point Objective (RPO): 1 hour
            - Automated backup and replication
            - Geographic redundancy options
            - Incident response procedures
            - Emergency communication plans
            - Regular testing and validation

            Disaster Recovery Features:
            - Automated failover capabilities
            - Data backup and restoration
            - Infrastructure redundancy
            - Emergency access procedures
            - Vendor and supplier continuity plans
            """,
            page_number=7,
            subsections=["Recovery Objectives", "Backup Procedures", "Failover Systems", "Testing Protocols"]
        ),
        ComplianceSection(
            title="Access Control and Identity Management",
            content="""
            VaultLogic implements comprehensive access control and identity management systems to ensure only authorized users can access sensitive documents and system functions.

            Identity Management Features:
            - Single Sign-On (SSO) integration
            - Multi-factor authentication (MFA)
            - Role-based access control (RBAC)
            - Privileged access management (PAM)
            - Identity lifecycle management
            - Access certification and reviews
            - Just-in-time access provisioning

            Access Control Policies:
            - Principle of least privilege
            - Segregation of duties
            - Regular access reviews and recertification
            - Automated deprovisioning
            - Emergency access procedures
            """,
            page_number=8,
            subsections=["SSO Integration", "Multi-Factor Authentication", "Role Management", "Access Reviews"]
        ),
        ComplianceSection(
            title="Vendor Risk Management",
            content="""
            VaultLogic maintains a comprehensive vendor risk management program to ensure all third-party relationships meet our security and compliance standards.

            Vendor Management Process:
            - Due diligence and risk assessment
            - Security questionnaires and audits
            - Contractual security requirements
            - Ongoing monitoring and reviews
            - Incident response coordination
            - Performance and compliance tracking
            - Vendor lifecycle management

            Risk Assessment Criteria:
            - Data handling and security practices
            - Compliance certifications and audits
            - Financial stability and viability
            - Geographic and regulatory considerations
            - Service level agreement requirements
            """,
            page_number=9,
            subsections=["Due Diligence", "Security Assessment", "Contract Management", "Ongoing Monitoring"]
        ),
        ComplianceSection(
            title="Incident Response and Security Operations",
            content="""
            VaultLogic maintains a 24/7 Security Operations Center (SOC) and comprehensive incident response capabilities to detect, respond to, and recover from security incidents.

            Incident Response Process:
            - Incident detection and classification
            - Initial response and containment
            - Investigation and forensics
            - Eradication and recovery
            - Post-incident review and improvement
            - Customer notification procedures
            - Regulatory reporting requirements

            Security Operations:
            - 24/7 security monitoring
            - Threat intelligence integration
            - Vulnerability management
            - Security awareness training
            - Penetration testing and assessments
            - Security metrics and reporting
            """,
            page_number=10,
            subsections=["Detection", "Response Procedures", "Recovery Process", "Continuous Improvement"]
        )
    ]
}

# Predefined questions and answers for the chat demo
PREDEFINED_QA = [
    ChatMessage(
        question="What SOC 2 controls does VaultLogic implement?",
        answer="VaultLogic implements comprehensive SOC 2 Type II controls including access control and user authentication, system monitoring and logging, data encryption in transit and at rest, business continuity and disaster recovery, vendor management and risk assessment, change management processes, and physical and environmental security. Our controls are audited annually by independent third-party auditors.",
        sources=["SOC 2 Type II Compliance - Page 1"]
    ),
    ChatMessage(
        question="How does VaultLogic ensure GDPR compliance?",
        answer="VaultLogic ensures GDPR compliance through data minimization and purpose limitation, establishing lawful basis for processing, supporting rights to access, rectification, and erasure, enabling data portability and processing transparency, implementing privacy by design and by default, conducting Data Protection Impact Assessments (DPIA), and maintaining breach notification procedures. Our on-premise deployment ensures data never leaves your infrastructure.",
        sources=["GDPR Data Protection Compliance - Page 2"]
    ),
    ChatMessage(
        question="What encryption standards does VaultLogic use?",
        answer="VaultLogic implements military-grade encryption including AES-256 encryption for data at rest, TLS 1.3 for data in transit, end-to-end encryption for all communications, Hardware Security Module (HSM) integration, comprehensive key management and rotation procedures, and zero-knowledge architecture design.",
        sources=["Data Encryption and Security - Page 5"]
    ),
    ChatMessage(
        question="What are VaultLogic's disaster recovery capabilities?",
        answer="VaultLogic maintains robust disaster recovery with a Recovery Time Objective (RTO) of 4 hours and Recovery Point Objective (RPO) of 1 hour. We provide automated backup and replication, geographic redundancy options, incident response procedures, emergency communication plans, automated failover capabilities, and regular testing and validation.",
        sources=["Business Continuity and Disaster Recovery - Page 7"]
    ),
    ChatMessage(
        question="How does VaultLogic handle access control?",
        answer="VaultLogic implements comprehensive access control through Single Sign-On (SSO) integration, multi-factor authentication (MFA), role-based access control (RBAC), privileged access management (PAM), identity lifecycle management, access certification and reviews, and just-in-time access provisioning. We follow the principle of least privilege and segregation of duties.",
        sources=["Access Control and Identity Management - Page 8"]
    ),
    ChatMessage(
        question="What audit logging capabilities does VaultLogic provide?",
        answer="VaultLogic provides comprehensive audit logging including activity logging, user access and authentication logs, document processing and query logs, system configuration change logs, security event monitoring and alerting, compliance reporting and dashboards, and long-term log retention and archival with real-time security monitoring.",
        sources=["Audit Logging and Monitoring - Page 6"]
    )
]

def search_handbook(query: str) -> List[ChatMessage]:
    """
    Search the compliance handbook for relevant information based on the query.
    Returns a list of ChatMessage objects with answers and sources.
    """
    query_lower = query.lower()
    
    # Check predefined Q&A first
    for qa in PREDEFINED_QA:
        if any(keyword in query_lower for keyword in qa.question.lower().split()):
            return [qa]
    
    # Search through handbook sections
    results = []
    for section in COMPLIANCE_HANDBOOK["sections"]:
        title_match = any(word in section.title.lower() for word in query_lower.split())
        content_match = any(word in section.content.lower() for word in query_lower.split())
        
        if title_match or content_match:
            # Extract relevant paragraph
            sentences = section.content.split('.')
            relevant_sentences = [s for s in sentences if any(word in s.lower() for word in query_lower.split())]
            
            if relevant_sentences:
                answer = '. '.join(relevant_sentences[:3]) + '.'
                sources = [f"{section.title} - Page {section.page_number}"]
                
                results.append(ChatMessage(
                    question=query,
                    answer=answer.strip(),
                    sources=sources
                ))
    
    # Default response if no specific match found
    if not results:
        results.append(ChatMessage(
            question=query,
            answer="I couldn't find specific information about that topic in the compliance handbook. Please try rephrasing your question or ask about SOC 2, GDPR, HIPAA, ISO 27001, encryption, access control, audit logging, disaster recovery, vendor management, or incident response.",
            sources=["Compliance Handbook"]
        ))
    
    return results[:1]  # Return top result
