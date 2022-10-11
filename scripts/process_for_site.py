import util.logger
import metrics.media_coverage
import metrics.volunteers.process
import metrics.ballot.summarize


def main():
    metrics.media_coverage.summarise()
    metrics.volunteers.process.summarise()

    metrics.ballot.summarize.by_ward()
    metrics.ballot.summarize.by_date()


if __name__ == '__main__':
    main()
