# Reef daily work report

## Installation

First, extract this project in somewhere like `~/`.

Next, run the setup script.

```bash
cd <path/to/project>
chmod +x setup.sh
./setup.sh
```

Then it will setup a daily cronjob that writes the working statistics of the day in a HTML file located in `~/reef/<date>.html`