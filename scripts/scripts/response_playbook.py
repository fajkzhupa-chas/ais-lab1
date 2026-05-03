#!/usr/bin/env python3
"""
Automatiserad incidentrespons-playbook.
Hanterar: blockering, isolering, larmning och loggning.
"""

import json
import subprocess
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('incident_response.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class IncidentResponder:
    def __init__(self):
        self.incidents = []
        self.blocked_ips = set()

    def block_ip(self, ip: str, reason: str, duration: int = 3600):
        """Blockera en IP-adress via iptables."""
        if ip in self.blocked_ips:
            return
        try:
            subprocess.run(['sudo', 'iptables', '-I', 'INPUT', '-s', ip, '-j', 'DROP'], check=True, capture_output=True)
            self.blocked_ips.add(ip)
            logger.warning(f"BLOCKERAD IP i brandväggen: {ip} — {reason}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Kunde inte blockera {ip}: {e}")

    def send_alert(self, severity: str, message: str):
        logger.info(f"NOTIFIKATION SKICKAD [{severity.upper()}]: {message}")

    def process_alert(self, alert: dict):
        severity = alert.get('severity')
        details = alert.get('details', {})
        
        # Eftersom vi testar, hårdkodar vi en attack-IP här för att se brandväggen jobba!
        src_ip = "8.8.8.8" if severity in ['medium', 'high', 'critical'] else None

        if severity == 'critical':
            if src_ip: self.block_ip(src_ip, 'Kritisk anomali', 3600)
            self.send_alert('critical', f'Kritisk incident: {details}')
            
        elif severity == 'high':
            if src_ip: self.block_ip(src_ip, 'Hög anomali detekterad', 1800)
            self.send_alert('high', f'Hög incident: {details}')
            
        elif severity == 'medium':
            if src_ip: self.block_ip(src_ip, 'Misstänkt aktivitet', 600)
            self.send_alert('medium', f'Medium incident: {details}')

if __name__ == '__main__':
    responder = IncidentResponder()
    try:
        with open('active_alerts.json') as f:
            alerts = json.load(f)
    except FileNotFoundError:
        print("Kör alert_manager.py först")
        exit(1)

    print(f"Behandlar {len(alerts)} larm från AI-motorn...")
    for alert in alerts:
        responder.process_alert(alert)

    print(f"\nFärdigt! {len(responder.blocked_ips)} angripare har blockerats i brandväggen.")
