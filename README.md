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

## Running Locally

### Prerequisites
- Python 3.8+
- A RapidAPI account with JSearch API subscription (free tier available)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Hassanah-dev006/Web_Infrastructure_Summative.git
   cd Web_Infrastructure_Summative
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Create a `.env` file from the example:
   ```bash
   cp .env.example .env
   ```

4. Edit `.env` and add your RapidAPI key:
   ```
   RAPIDAPI_KEY=your_actual_rapidapi_key
   FLASK_SECRET_KEY=any_random_secret_string
   ```

5. Run the application:
   ```bash
   python app.py
   ```

6. Open http://localhost:5000 in your browser.
