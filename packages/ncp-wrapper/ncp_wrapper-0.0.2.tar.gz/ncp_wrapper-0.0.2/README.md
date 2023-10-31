# ncp_wrapper - Python Package for Naver Cloud Platform (NCP)

`ncp_wrapper` is a versatile Python package that simplifies interaction with Naver Cloud Platform (NCP) services. It provides easy-to-use wrappers for various NCP functionalities, including sending emails, managing cloud resources, and more.

## Installation

You can install `ncp_wrapper` via pip. Use the following command:

```bash
pip install ncp_wrapper
```




## Features
### 1. Naver Works Email

Send emails using Naver Works (smtp.worksmobile.com). The Email class encapsulates email composition and attachment handling.

```python
from ncp_wrapper.naver_works import Email

# Initialize the Email class with your Naver Works credentials
user_id = "your_email@example.com"
user_password = "your_password"
email_sender = Email(user_id, user_password)

# Compose and send an email
subject = "Hello, World!"
body = "This is a test email sent using ncp_wrapper."
recipient_emails = ["recipient1@example.com", "recipient2@example.com"]
cc = ["cc@example.com"]
bcc = ["bcc@example.com"]
attachments = [("document.pdf", "file"), "image.jpg"]

email_sender.send_email(
    subject=subject,
    body=body,
    recipient_emails=recipient_emails,
    cc=cc,
    bcc=bcc,
    attachments=attachments,
)
```

This code demonstrates how to create an `Email` instance, set the necessary email parameters, and send an email with attachments.

## Documentation

For more details on the `Email` class and its methods, please refer to the source code or the package documentation.

## License

This package is distributed under the MIT License. See the [LICENSE](LICENSE) file for more information.

## Issues and Contributions

If you encounter any issues or have suggestions for improvements, please [open an issue](https://github.com/thecodinglog/ncp/issues). Contributions are welcome through pull requests.

## Credits

This package is developed and maintained by [Jeongjin Kim](https://github.com/thecodinglog/ncp).

```
