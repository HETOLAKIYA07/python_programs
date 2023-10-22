import calendar
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def remove_extra_zeros(calendar_line):
    day_list = calendar_line.split()
    cleaned_day_list = [day for day in day_list if day != '0' or day == '00']
    return " ".join(cleaned_day_list)

def display_month_calendar(year, month, skip_dates=[]):
    cal = calendar.monthcalendar(year, month)

    for week in cal:
        for i, day in enumerate(week):
            if day == 0:
                continue
            if day in skip_dates:
                week[i] = ''  # Replace the skipped dates
            elif calendar.weekday(year, month, day) == 5:
                week[i] = ' '  # Replace the Sundays

    # Convert the modified monthcalendar back to a string representation
    cal_str = calendar.month(year, month)

    # Replace the original dates with the updated week data
    lines = cal_str.splitlines()
    header = lines[0]
    lines = lines[2:]  # Remove the line containing weekdays

    # Create a list to store the day representations
    day_list = []

    for week in cal:
        week_str = " ".join(str(day) if day != ' ' else '' for day in week)
        # Append week only if it is not empty
        if week_str.strip():
            day_list.append(week_str)

    # Combine all days in a single line
    calendar_line = " ".join(day_list)
    cleaned_calendar_line = remove_extra_zeros(calendar_line)

    return cleaned_calendar_line

def send_email(sender_email, sender_password, receiver_email, subject, body):
    try:
        smtp_server = 'smtp.gmail.com'
        port = 587

        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login(sender_email, sender_password)

        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print("Failed to send email:", str(e))

if __name__ == "__main__":
    year = int(input("Enter the year: "))
    month = int(input("Enter the month (1-12): "))

    skip_dates = []
    while True:
        skip_input = input("Enter a date to skip (0 to finish): ")
        if skip_input == '0':
            break
        skip_dates.append(int(skip_input))

    cleaned_calendar_line = display_month_calendar(year, month, skip_dates)
    print(cleaned_calendar_line)

    share_via_email = input("Do you want to share the calendar via email? (yes/no): ").lower()

    if share_via_email == 'yes':
        sender_email = os.environ.get('SENDER_EMAIL')
        sender_password = os.environ.get('SENDER_PASSWORD')
        receiver_email = os.environ.get('RECEIVER_EMAIL')
        subject = f"attendence for {calendar.month_name[month]} {year}"
        body = f"Here's the attendence for {calendar.month_name[month]} {year}:\n\n{cleaned_calendar_line}"

        if sender_email and sender_password and receiver_email:
            send_email(sender_email, sender_password, receiver_email, subject, body)
        else:
            print("Please set the SENDER_EMAIL, SENDER_PASSWORD, and RECEIVER_EMAIL environment variables.")
