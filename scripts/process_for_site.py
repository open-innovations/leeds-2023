import scripts.metrics.media_coverage.media_coverage
import metrics.volunteers.process
import dashboard.community


def main():
    scripts.metrics.media_coverage.media_coverage.summarise()
    metrics.volunteers.process.summarise()
    dashboard.community.process()


if __name__ == '__main__':
    main()
