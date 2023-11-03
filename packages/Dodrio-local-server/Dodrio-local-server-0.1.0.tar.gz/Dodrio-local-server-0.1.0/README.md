# Dodrio-local-server

Dodrio-local-server is a local server implemented in Python using Flask. It is designed to receive messages from RabbitMQ and send them to AWS.

## Table of Contents
- [Requirements](#requirements)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [Usage](#usage)
- [Contributing](#contributing)

## Requirements

Make sure you have the following installed:
- Python 3.x
- [pip](https://pip.pypa.io/en/stable/installation/)
- RabbitMQ server
- AWS credentials configured on your system ([AWS CLI Configuration](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html))

## Getting Started

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/Dodrio-local-server.git
    cd Dodrio-local-server
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

Update the configuration in `config.py` file as needed. This may include RabbitMQ connection details, AWS credentials, and any other project-specific settings.

```python
# config.py

RABBITMQ_HOST = "your_rabbitmq_host"
RABBITMQ_PORT = 5672
RABBITMQ_USERNAME = "your_rabbitmq_username"
RABBITMQ_PASSWORD = "your_rabbitmq_password"

AWS_ACCESS_KEY_ID = "your_aws_access_key_id"
AWS_SECRET_ACCESS_KEY = "your_aws_secret_access_key"
AWS_REGION = "your_aws_region"
CLOUD_ENDPOINT = "http://your-cloud-endpoint"

DEVICE_ID = "your_device_id"
```

## Usage

Run the Flask application:

```bash
python app.py
```

This will start the local server. Visit `http://localhost:5000` in your browser to access the application.

## Contributing

Feel free to contribute to this project. Fork the repository, make your changes, and submit a pull request.

