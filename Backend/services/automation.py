from services.alerts import generate_alerts

def run_automation(data):

    alerts = generate_alerts(data)

    # Future: send email / notifications

    return alerts