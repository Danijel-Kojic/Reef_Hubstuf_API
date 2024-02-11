# Reef daily activity statistics report


## Features
- Retrieve daily activity statistics of an organization on the given day (yesterday by default) using Reef Hubstaff API
- Output the aggregated statistics in a HTML table format
- Logging to a file system (`/tmp/reef.log` by default in Linux)
- Send the HTML table to the manager via email using SMTP service
- Daily report using cron job
- Simple deployment

## Deployment

For deployment, please refer to [INSTALL.md](INSTALL.md) instruction.