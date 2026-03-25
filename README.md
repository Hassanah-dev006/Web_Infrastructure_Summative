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

### Configuring HAProxy on Lb-01

1. **SSH into the load balancer:**
   ```bash
   ssh ubuntu@44.202.34.36
   ```

2. **Install HAProxy:**
   ```bash
   sudo apt update
   sudo apt install -y haproxy
   ```

3. **Configure HAProxy:**
   ```bash
   sudo nano /etc/haproxy/haproxy.cfg
   ```
   Add the following at the end of the file:
   ```
   frontend http_front
       bind *:80
       default_backend web_servers

   backend web_servers
       balance roundrobin
       server web-01 34.201.51.178:80 check
       server web-02 54.158.123.226:80 check
   ```

4. **Enable and restart HAProxy:**
   ```bash
   sudo systemctl enable haproxy
   sudo systemctl restart haproxy
   ```

5. **Test the load balancer** by visiting http://44.202.34.36 in your browser.

### Verifying Load Balancing

To confirm traffic is distributed between both servers, you can check Nginx access logs on each web server:
```bash
# On Web-01
sudo tail -f /var/log/nginx/access.log

# On Web-02
sudo tail -f /var/log/nginx/access.log
```

Refresh the load balancer URL multiple times and observe requests appearing on both servers.

## Challenges and Solutions

1. **API Rate Limits**: The JSearch API free tier has limited requests. Implemented a 5-minute in-memory cache to avoid redundant API calls for the same queries.

2. **Data Consistency**: Job listings from different sources have varying data formats. Handled missing fields gracefully with fallback values and conditional rendering in templates.

3. **Secure API Key Management**: Used environment variables via python-dotenv to keep API keys out of source code. The `.gitignore` file excludes `.env` from version control.

## Technologies

- **Backend**: Python 3, Flask, Requests
- **Frontend**: HTML5, CSS3, JavaScript (ES6), Bootstrap 5
- **Deployment**: Gunicorn, Nginx, HAProxy
- **API**: JSearch via RapidAPI
