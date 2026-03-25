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

## Deployment to Web Servers

### Server Details
| Server  | Username | IP Address      | Role           |
|---------|----------|-----------------|----------------|
| Web-01  | ubuntu   | 34.201.51.178   | Web Server     |
| Web-02  | ubuntu   | 54.158.123.226  | Web Server     |
| Lb-01   | ubuntu   | 44.202.34.36    | Load Balancer  |

### Deploying to Web-01 and Web-02

Repeat the following steps on **both** web servers:

1. **SSH into the server:**
   ```bash
   ssh ubuntu@34.201.51.178   # Web-01
   # or
   ssh ubuntu@54.158.123.226  # Web-02
   ```

2. **Install dependencies:**
   ```bash
   sudo apt update
   sudo apt install -y python3 python3-pip python3-venv nginx
   ```

3. **Clone the repository and set up the app:**
   ```bash
   cd /home/ubuntu
   git clone https://github.com/Hassanah-dev006/Web_Infrastructure_Summative.git
   cd Web_Infrastructure_Summative
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Create the `.env` file:**
   ```bash
   nano .env
   ```
   Add the following:
   ```
   RAPIDAPI_KEY=your_rapidapi_key
   FLASK_SECRET_KEY=a_strong_random_secret
   ```

5. **Create a systemd service** for the app to run in the background:
   ```bash
   sudo nano /etc/systemd/system/jobscout.service
   ```
   Add the following content:
   ```ini
   [Unit]
   Description=JobScout Flask App
   After=network.target

   [Service]
   User=ubuntu
   WorkingDirectory=/home/ubuntu/Web_Infrastructure_Summative
   Environment="PATH=/home/ubuntu/Web_Infrastructure_Summative/venv/bin"
   EnvironmentFile=/home/ubuntu/Web_Infrastructure_Summative/.env
   ExecStart=/home/ubuntu/Web_Infrastructure_Summative/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app

   [Install]
   WantedBy=multi-user.target
   ```

6. **Start the service:**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable jobscout
   sudo systemctl start jobscout
   ```

7. **Configure Nginx** as a reverse proxy:
   ```bash
   sudo nano /etc/nginx/sites-available/jobscout
   ```
   Add:
   ```nginx
   server {
       listen 80;
       server_name _;

       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

8. **Enable the site and restart Nginx:**
   ```bash
   sudo ln -s /etc/nginx/sites-available/jobscout /etc/nginx/sites-enabled/
   sudo rm -f /etc/nginx/sites-enabled/default
   sudo nginx -t
   sudo systemctl restart nginx
   ```

9. **Verify** the app is running:
   ```bash
   curl http://localhost
   ```
