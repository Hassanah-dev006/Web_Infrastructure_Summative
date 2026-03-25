# JobScout - Job Search Aggregator

A web application that aggregates job listings from LinkedIn, Indeed, Glassdoor, and other major job boards into a single, searchable interface. Built with Python/Flask and vanilla JavaScript.

## Features

- **Unified Job Search** - Search thousands of jobs across multiple platforms at once
- **Advanced Filtering** - Filter by employment type, date posted, remote-only, and keywords
- **Sorting** - Sort results by relevance, date posted, or salary
- **Salary Estimates** - View estimated salary ranges for any role and location
- **Save Jobs** - Bookmark jobs to review and compare later (stored in browser)
- **Job Details** - View full descriptions, qualifications, responsibilities, and benefits
- **Direct Apply** - Links directly to the original job application page
- **Responsive Design** - Works on desktop, tablet, and mobile devices

## API Used

**JSearch API** (via RapidAPI)
- Documentation: https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch
- Aggregates real job listings from LinkedIn, Indeed, Glassdoor, ZipRecruiter, and more
- Endpoints used: `/search`, `/job-details`, `/estimated-salary`
- Credit: Developed by [letscrape](https://rapidapi.com/letscrape-6bRBa3QguO5) on RapidAPI
