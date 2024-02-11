# Reef daily activity statistics report

## Installation

First, extract this project in somewhere like `~/`.

Create an ".env" file based on ".env.example" in the project directory and fill the proper values for each fields such as Hubstuff API and SMTP credentials

Next, run the setup script.

```bash
cd <path/to/project>
chmod +x setup.sh
./setup.sh
```

Then it will setup a daily cronjob that writes the working statistics of the given day in a HTML file located in `~/reef/<date>.html`
