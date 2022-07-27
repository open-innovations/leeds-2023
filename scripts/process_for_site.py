import metrics.media_coverage
import metrics.roadshow_attendees


def main():
    metrics.roadshow_attendees.process_workshop_attendees('W-Mon')
    metrics.media_coverage.summarise()

if __name__ == '__main__':
    main()
