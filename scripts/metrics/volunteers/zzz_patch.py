from metrics.volunteers.data import load_raw_data, save_raw_data


def patch():
    save_raw_data(load_raw_data())
