import dashboard.community.events
import dashboard.community.residents


def process():
    dashboard.community.events.summarise_events()
    dashboard.community.residents.summarise_activity()
