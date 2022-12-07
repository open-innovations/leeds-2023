import dashboard.community


def main():
    # Temporarily removing this cause it's breaking the build
    # metrics.media_coverage.media_coverage.summarise()
    dashboard.community.process()


if __name__ == '__main__':
    main()
