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

## Attachment
In the `docs` directory, it has a Postman collection file for Reef Hubstaff API.

## Notice
- In the project description, I am supposed to retrieve the activity statistics information of a given organization.
But the API endpoint for retrieving organziations returns multiple organizations.
So I assumed that we want to retrieve the activity aggregation information of the 1st organization from the retrived list of organizations.
- API endpoints for organization activities returns an array of activities, but each item in the array only contains `starts_at` and `updated_at` fields, but no field like `finishes_at`. So I assumed that `updated_at` is the end time of activity.
- Activities that are retrieved from the API often overlaps, so I had to take this overlap into consideration while calculating total amount of working time.