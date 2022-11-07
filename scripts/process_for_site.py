import util.logger
import metrics.media_coverage
import metrics.volunteers.process
import metrics.ballot.summarize
import dashboard.community


def main():
    metrics.media_coverage.summarise()
    metrics.volunteers.process.summarise()

    metrics.ballot.summarize.all()

    dashboard.community.process()


if __name__ == '__main__':
    main()
