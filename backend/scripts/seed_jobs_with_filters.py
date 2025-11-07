#!/usr/bin/env python3
"""
Seed script to populate the database with sample jobs containing filter data.

This script creates 60+ realistic job postings with diverse filter values
to test the advanced search and filter functionality.

Usage:
    python scripts/seed_jobs_with_filters.py
"""
import asyncio
import random
from datetime import datetime, timedelta
from typing import List

# Add parent directory to path for imports
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.models.job import (
    Job,
    WorkType,
    JobType,
    ExperienceLevel,
    CompanySize,
    JobStatus
)
from app.core.config import settings


# Sample data for generating realistic jobs
COMPANIES = [
    # Tech Giants
    {"name": "Google", "rating": 4.5, "size": CompanySize.ENTERPRISE, "industry": "Technology"},
    {"name": "Microsoft", "rating": 4.4, "size": CompanySize.ENTERPRISE, "industry": "Technology"},
    {"name": "Amazon", "rating": 4.2, "size": CompanySize.ENTERPRISE, "industry": "E-commerce"},
    {"name": "Meta", "rating": 4.3, "size": CompanySize.ENTERPRISE, "industry": "Social Media"},
    {"name": "Apple", "rating": 4.5, "size": CompanySize.ENTERPRISE, "industry": "Technology"},
    
    # Mid-size tech
    {"name": "Stripe", "rating": 4.6, "size": CompanySize.LARGE, "industry": "Fintech"},
    {"name": "Airbnb", "rating": 4.4, "size": CompanySize.LARGE, "industry": "Travel"},
    {"name": "Uber", "rating": 4.0, "size": CompanySize.LARGE, "industry": "Transportation"},
    {"name": "Lyft", "rating": 4.1, "size": CompanySize.LARGE, "industry": "Transportation"},
    {"name": "Shopify", "rating": 4.5, "size": CompanySize.LARGE, "industry": "E-commerce"},
    
    # Startups
    {"name": "Figma", "rating": 4.7, "size": CompanySize.MEDIUM, "industry": "Design"},
    {"name": "Notion", "rating": 4.6, "size": CompanySize.MEDIUM, "industry": "Productivity"},
    {"name": "Discord", "rating": 4.5, "size": CompanySize.MEDIUM, "industry": "Communication"},
    {"name": "Coinbase", "rating": 4.2, "size": CompanySize.LARGE, "industry": "Cryptocurrency"},
    {"name": "Robinhood", "rating": 3.9, "size": CompanySize.MEDIUM, "industry": "Fintech"},
    
    # Small companies
    {"name": "Vercel", "rating": 4.6, "size": CompanySize.SMALL, "industry": "Cloud"},
    {"name": "Supabase", "rating": 4.5, "size": CompanySize.STARTUP, "industry": "Database"},
    {"name": "Linear", "rating": 4.7, "size": CompanySize.STARTUP, "industry": "Project Management"},
]

CITIES = [
    {"city": "San Francisco", "state": "CA"},
    {"city": "New York", "state": "NY"},
    {"city": "Seattle", "state": "WA"},
    {"city": "Austin", "state": "TX"},
    {"city": "Boston", "state": "MA"},
    {"city": "Los Angeles", "state": "CA"},
    {"city": "Chicago", "state": "IL"},
    {"city": "Denver", "state": "CO"},
    {"city": "Portland", "state": "OR"},
    {"city": "Miami", "state": "FL"},
    {"city": "Atlanta", "state": "GA"},
    {"city": "Remote", "state": ""},
]

JOB_TITLES = {
    ExperienceLevel.ENTRY: [
        "Junior Software Engineer",
        "Junior Frontend Developer",
        "Associate Product Manager",
        "Junior Data Analyst",
        "Entry-Level Backend Developer",
        "Junior DevOps Engineer",
        "Associate UX Designer",
        "Junior QA Engineer",
    ],
    ExperienceLevel.MID: [
        "Software Engineer",
        "Frontend Developer",
        "Backend Developer",
        "Full-Stack Developer",
        "Product Manager",
        "Data Scientist",
        "DevOps Engineer",
        "UX Designer",
        "QA Engineer",
    ],
    ExperienceLevel.SENIOR: [
        "Senior Software Engineer",
        "Senior Frontend Developer",
        "Senior Backend Developer",
        "Senior Product Manager",
        "Senior Data Scientist",
        "Senior DevOps Engineer",
        "Senior UX Designer",
        "Engineering Manager",
    ],
    ExperienceLevel.LEAD: [
        "Staff Software Engineer",
        "Principal Engineer",
        "Lead Product Manager",
        "Director of Engineering",
        "VP of Engineering",
        "Technical Architect",
        "Lead Data Scientist",
    ],
}

SKILLS_BY_ROLE = {
    "Software Engineer": ["Python", "Java", "Go", "TypeScript", "AWS", "Docker", "Kubernetes"],
    "Frontend Developer": ["React", "TypeScript", "JavaScript", "HTML", "CSS", "Next.js", "Vue.js"],
    "Backend Developer": ["Python", "Java", "Node.js", "PostgreSQL", "MongoDB", "Redis", "GraphQL"],
    "Full-Stack Developer": ["React", "Node.js", "TypeScript", "PostgreSQL", "AWS", "Docker"],
    "Product Manager": ["Product Strategy", "Agile", "User Research", "SQL", "Analytics", "Roadmapping"],
    "Data Scientist": ["Python", "Machine Learning", "TensorFlow", "SQL", "Statistics", "Pandas", "Scikit-learn"],
    "DevOps Engineer": ["AWS", "Kubernetes", "Docker", "Terraform", "CI/CD", "Linux", "Python"],
    "UX Designer": ["Figma", "Sketch", "User Research", "Prototyping", "UI Design", "Usability Testing"],
    "QA Engineer": ["Selenium", "Python", "JavaScript", "Test Automation", "CI/CD", "Manual Testing"],
}

SALARY_RANGES = {
    ExperienceLevel.ENTRY: (60000, 95000),
    ExperienceLevel.MID: (90000, 145000),
    ExperienceLevel.SENIOR: (140000, 220000),
    ExperienceLevel.LEAD: (200000, 350000),
}


def generate_job_description(title: str, company: str, skills: List[str]) -> str:
    """Generate a realistic job description."""
    return f"""
We are looking for a talented {title} to join our team at {company}.

Responsibilities:
- Design, develop, and maintain scalable applications
- Collaborate with cross-functional teams to deliver high-quality software
- Participate in code reviews and mentor junior team members
- Contribute to technical documentation and best practices

Requirements:
- Strong proficiency in {', '.join(skills[:3])}
- Experience with {', '.join(skills[3:5]) if len(skills) > 3 else 'modern development tools'}
- Excellent problem-solving and communication skills
- Bachelor's degree in Computer Science or equivalent experience

Nice to Have:
- Experience with {', '.join(skills[5:]) if len(skills) > 5 else 'cloud platforms and microservices'}
- Open source contributions
- Strong understanding of software design patterns

We offer competitive compensation, comprehensive benefits, and a collaborative work environment.
""".strip()


async def create_sample_jobs():
    """Create sample jobs with filter data."""
    print("🚀 Starting job seeding...")
    
    # Initialize database
    client = AsyncIOMotorClient(settings.mongodb_uri)
    db = client[settings.database_name]
    await init_beanie(database=db, document_models=[Job])
    
    # Clear existing jobs (optional - comment out if you want to keep existing)
    # await Job.find_all().delete()
    # print("🗑️  Cleared existing jobs")
    
    jobs_created = 0
    
    # Generate jobs for each experience level
    for exp_level in ExperienceLevel:
        titles = JOB_TITLES[exp_level]
        
        for _ in range(15):  # 15 jobs per level = 60 total
            # Random selections
            company = random.choice(COMPANIES)
            title = random.choice(titles)
            location = random.choice(CITIES)
            work_type = random.choices(
                [WorkType.REMOTE, WorkType.HYBRID, WorkType.ONSITE],
                weights=[0.4, 0.3, 0.3]
            )[0]
            job_type = random.choices(
                [JobType.FULL_TIME, JobType.PART_TIME, JobType.CONTRACT, JobType.INTERNSHIP],
                weights=[0.7, 0.1, 0.15, 0.05]
            )[0]
            
            # Determine skills based on title
            base_role = None
            for role in SKILLS_BY_ROLE:
                if role.lower() in title.lower():
                    base_role = role
                    break
            
            if not base_role:
                base_role = "Software Engineer"
            
            skills = random.sample(SKILLS_BY_ROLE[base_role], min(5, len(SKILLS_BY_ROLE[base_role])))
            
            # Salary range based on experience level
            salary_range = SALARY_RANGES[exp_level]
            salary_min = random.randint(salary_range[0], (salary_range[0] + salary_range[1]) // 2)
            # Ensure max is at least 20k more than min, but not exceeding range max
            salary_max = min(salary_min + random.randint(20000, 50000), salary_range[1])
            
            # Sometimes omit salary (30% chance)
            if random.random() < 0.3:
                salary_min = None
                salary_max = None
            
            # Easy apply (60% chance)
            easy_apply = random.random() < 0.6
            
            # Posted date - distribute across last 60 days
            days_ago = random.choices(
                [0, 1, 2, 7, 14, 30, 45, 60],
                weights=[0.15, 0.15, 0.15, 0.2, 0.15, 0.1, 0.05, 0.05]
            )[0]
            posted_at = datetime.utcnow() - timedelta(days=days_ago)
            
            # Generate description
            description = generate_job_description(title, company["name"], skills)
            
            # Create job
            job = Job(
                title=title,
                description=description,
                skills=skills,
                employer_id=None,  # System-generated jobs
                status=JobStatus.ACTIVE,
                
                # Location
                location=f"{location['city']}, {location['state']}" if location['state'] else location['city'],
                city=location['city'],
                state=location['state'] or None,
                country="USA",
                
                # Work arrangement
                work_type=work_type,
                job_type=job_type,
                experience_level=exp_level,
                easy_apply=easy_apply,
                
                # Salary
                salary_min=salary_min,
                salary_max=salary_max,
                salary_currency="USD",
                
                # Company
                company_name=company["name"],
                company_rating=company["rating"],
                company_size=company["size"],
                industry=company["industry"],
                
                # Timestamps
                posted_at=posted_at,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            
            await job.insert()
            jobs_created += 1
            
            if jobs_created % 10 == 0:
                print(f"✅ Created {jobs_created} jobs...")
    
    print(f"\n🎉 Successfully seeded {jobs_created} jobs!")
    print(f"\n📊 Summary:")
    print(f"  - Entry Level: ~15 jobs")
    print(f"  - Mid Level: ~15 jobs")
    print(f"  - Senior: ~15 jobs")
    print(f"  - Lead: ~15 jobs")
    print(f"  - Remote jobs: ~40%")
    print(f"  - Jobs with salary: ~70%")
    print(f"  - Easy Apply: ~60%")
    print(f"\n🔍 Test the search API:")
    print(f"  curl 'http://localhost:8000/api/v1/jobs/search?remote_only=true'")
    print(f"  curl 'http://localhost:8000/api/v1/jobs/search?salary_min=100000&experience_levels=senior'")
    print(f"  curl 'http://localhost:8000/api/v1/jobs/filter-options'")
    
    client.close()


if __name__ == "__main__":
    asyncio.run(create_sample_jobs())

